import time, sys

from PyQt4 import QtCore
import numpy as np

from qspectrumanalyzer.utils import smooth


class HistoryBuffer:
    """Fixed-size NumPy array ring buffer"""
    def __init__(self, data_size, max_history_size, dtype=float):
        self.data_size = data_size
        self.max_history_size = max_history_size
        self.history_size = 0
        self.counter = 0
        self.buffer = np.empty(shape=(max_history_size, data_size), dtype=dtype)

    def append(self, data):
        """Append new data to ring buffer"""
        self.counter += 1
        if self.history_size < self.max_history_size:
            self.history_size += 1
        self.buffer = np.roll(self.buffer, -1, axis=0)
        self.buffer[-1] = data

    def get_buffer(self):
        """Return buffer stripped to size of actual data"""
        if self.history_size < self.max_history_size:
            return self.buffer[-self.history_size:]
        else:
            return self.buffer

    def __getitem__(self, key):
        return self.buffer[key]


class TaskSignals(QtCore.QObject):
    """Task signals emitter"""
    result = QtCore.pyqtSignal(object)


class Task(QtCore.QRunnable):
    """Threaded task (run it with QThreadPool worker threads)"""
    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()

    def run(self):
        """Run task in worker thread and emit signal with result"""
        #print('Running', self.task, 'in thread', QtCore.QThread.currentThreadId())
        result = self.task(*self.args, **self.kwargs)
        self.signals.result.emit(result)


class DataStorage(QtCore.QObject):
    """Data storage for spectrum measurements"""
    history_updated = QtCore.pyqtSignal(object)
    data_updated = QtCore.pyqtSignal(object)
    data_recalculated = QtCore.pyqtSignal(object)
    average_updated = QtCore.pyqtSignal(object)
    peak_hold_max_updated = QtCore.pyqtSignal(object)
    peak_hold_min_updated = QtCore.pyqtSignal(object)

    def __init__(self, max_history_size=100, parent=None):
        super().__init__(parent)
        self.max_history_size = max_history_size
        self.smooth = False
        self.smooth_length = 11
        self.smooth_window = "hanning"

        # Use only one worker thread because it is not faster
        # with more threads (and memory consumption is much higher)
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        self.reset()

    def reset(self):
        """Reset all data"""
        self.wait()
        self.x = None
        self.history = None
        self.reset_data()

    def reset_data(self):
        """Reset current data"""
        self.wait()
        self.y = None
        self.average_counter = 0
        self.average = None
        self.peak_hold_max = None
        self.peak_hold_min = None

    def start_task(self, fn, *args, **kwargs):
        """Run function asynchronously in worker thread"""
        task = Task(fn, *args, **kwargs)
        self.threadpool.start(task)

    def wait(self):
        """Wait for worker threads to complete all running tasks"""
        self.threadpool.waitForDone()

    def update(self, data):
        """Update data storage"""
        self.average_counter += 1

        if self.x is None:
            self.x = data["x"]

        self.start_task(self.update_history, data.copy())
        self.start_task(self.update_data, data)

    def update_data(self, data):
        """Update main spectrum data (and possibly apply smoothing)"""
        if self.smooth:
            data["y"] = self.smooth_data(data["y"])

        self.y = data["y"]
        self.data_updated.emit(self)

        self.start_task(self.update_average, data)
        self.start_task(self.update_peak_hold_max, data)
        self.start_task(self.update_peak_hold_min, data)

    def update_history(self, data):
        """Update spectrum measurements history"""
        if self.history is None:
            self.history = HistoryBuffer(len(data["y"]), self.max_history_size)

        self.history.append(data["y"])
        self.history_updated.emit(self)

    def update_average(self, data):
        """Update average data"""
        if self.average is None:
            self.average = data["y"].copy()
        else:
            self.average = np.average((self.average, data["y"]), axis=0, weights=(self.average_counter - 1, 1))
            self.average_updated.emit(self)

    def update_peak_hold_max(self, data):
        """Update max. peak hold data"""
        if self.peak_hold_max is None:
            self.peak_hold_max = data["y"].copy()
        else:
            self.peak_hold_max = np.maximum(self.peak_hold_max, data["y"])
            self.peak_hold_max_updated.emit(self)

    def update_peak_hold_min(self, data):
        """Update min. peak hold data"""
        if self.peak_hold_min is None:
            self.peak_hold_min = data["y"].copy()
        else:
            self.peak_hold_min = np.minimum(self.peak_hold_min, data["y"])
            self.peak_hold_min_updated.emit(self)

    def smooth_data(self, y):
        """Apply smoothing function to data"""
        return smooth(y, window_len=self.smooth_length, window=self.smooth_window)

    def set_smooth(self, toggle, length=11, window="hanning", recalculate=False):
        """Toggle smoothing and set smoothing params"""
        if toggle != self.smooth or length != self.smooth_length or window != self.smooth_window:
            self.smooth = toggle
            self.smooth_length = length
            self.smooth_window = window
            if recalculate:
                self.start_task(self.recalculate_data)
            else:
                self.reset_data()

    def recalculate_data(self):
        """Recalculate current data from history"""
        if self.history is None:
            return

        history = self.history.get_buffer()
        if self.smooth:
            self.y = self.smooth_data(history[-1])
            self.average_counter = 0
            self.average = self.y.copy()
            self.peak_hold_max = self.y.copy()
            self.peak_hold_min = self.y.copy()
            for y in history[:-1]:
                self.average_counter += 1
                y = self.smooth_data(y)
                self.average = np.average((self.average, y), axis=0, weights=(self.average_counter - 1, 1))
                self.peak_hold_max = np.maximum(self.peak_hold_max, y)
                self.peak_hold_min = np.minimum(self.peak_hold_min, y)
        else:
            self.y = history[-1]
            self.average_counter = self.history.history_size
            self.average = np.average(history, axis=0)
            self.peak_hold_max = history.max(axis=0)
            self.peak_hold_min = history.min(axis=0)

        self.data_recalculated.emit(self)
        #self.data_updated.emit({"x": self.x, "y": self.y})
        #self.average_updated.emit({"x": self.x, "y": self.average})
        #self.peak_hold_max_updated.emit({"x": self.x, "y": self.peak_hold_max})
        #self.peak_hold_min_updated.emit({"x": self.x, "y": self.peak_hold_min})


class Test:
    """Test data storage performance"""
    def __init__(self, data_size=100000, max_history_size=100):
        self.data_size = data_size
        self.data = {"x": np.arange(data_size),
                     "y": None}
        self.datastorage = DataStorage(max_history_size)

    def run_one(self):
        """Generate random data and update data storage"""
        self.data["y"] = np.random.normal(size=self.data_size)
        self.datastorage.update(self.data)

    def run(self, runs=1000):
        """Run performance test"""
        t = time.time()
        for i in range(runs):
            self.run_one()
        self.datastorage.wait()
        total_time = time.time() - t
        print("Total time:", total_time)
        print("FPS:", runs / total_time)


if __name__ == "__main__":
    test = Test(int(sys.argv[1]), int(sys.argv[2]))
    test.run(int(sys.argv[3]))
