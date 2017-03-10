import os, glob, subprocess

from PyQt4 import QtCore


class BaseInfo:
    """Default device metadata"""
    sample_rate_min = 0
    sample_rate_max = 3200000
    sample_rate = 2560000
    gain_min = -1
    gain_max = 49
    gain = 37
    start_freq_min = 24
    start_freq_max = 2200
    start_freq = 87
    stop_freq_min = 24
    stop_freq_max = 2200
    stop_freq = 108
    bin_size_min = 0
    bin_size_max = 2800
    bin_size = 10
    interval_min = 0
    interval_max = 999
    interval = 10
    ppm_min = -999
    ppm_max = 999
    ppm = 0
    crop_min = 0
    crop_max = 99
    crop = 0
    additional_params = ''

    @classmethod
    def help(cls, executable):
        try:
            p = subprocess.run([executable, '-h'], universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env=dict(os.environ, COLUMNS='125'))
            text = p.stdout
        except OSError:
            text = '{} executable not found!'.format(executable)
        return text


class BasePowerThread(QtCore.QThread):
    """Thread which runs Power Spectral Density acquisition and calculation process"""
    powerThreadStarted = QtCore.pyqtSignal()
    powerThreadStopped = QtCore.pyqtSignal()

    def __init__(self, data_storage, parent=None):
        super().__init__(parent)
        self.data_storage = data_storage
        self.alive = False
        self.process = None

    def stop(self):
        """Stop power process thread"""
        self.process_stop()
        self.alive = False
        self.wait()

    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, device=0, sample_rate=2560000):
        """Setup power process params"""
        raise NotImplementedError

    def process_start(self):
        """Start power process"""
        raise NotImplementedError

    def process_stop(self):
        """Terminate power process"""
        if self.process:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
            self.process.wait()
            self.process = None

    def parse_output(self, line):
        """Parse one line of output from power process"""
        raise NotImplementedError

    def run(self):
        """Power process thread main loop"""
        self.process_start()
        self.alive = True
        self.powerThreadStarted.emit()

        for line in self.process.stdout:
            if not self.alive:
                break
            self.parse_output(line)

        self.process_stop()
        self.alive = False
        self.powerThreadStopped.emit()


# Build list of all backends
_backends_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.splitext(os.path.basename(f))[0] for f in _backends_files
           if os.path.isfile(f) and not os.path.basename(f).startswith("_")]

# Import all backends
from qspectrumanalyzer.backends import *
