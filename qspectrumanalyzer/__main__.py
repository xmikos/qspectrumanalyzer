#!/usr/bin/env python

import sys, subprocess, signal, math, time, pprint

import numpy as np
import pyqtgraph as pg

from PyQt4 import QtCore, QtGui
from qspectrumanalyzer.version import __version__
from qspectrumanalyzer.ui_qspectrumanalyzer_settings import Ui_QSpectrumAnalyzerSettings
from qspectrumanalyzer.ui_qspectrumanalyzer_smooth import Ui_QSpectrumAnalyzerSmooth
from qspectrumanalyzer.ui_qspectrumanalyzer import Ui_QSpectrumAnalyzerMainWindow


# Basic settings
pg.setConfigOptions(antialias=True)

# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)


def smooth(x, window_len=11, window='hanning'):
    """Smooth 1D signal using specified window with given size"""
    x = np.array(x)
    if window_len < 3:
        return x

    if x.size < window_len:
        raise ValueError("Input data length must be greater than window size")

    if window not in ['rectangular', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window must be 'rectangular', 'hanning', 'hamming', 'bartlett' or 'blackman'")

    if window == 'rectangular':
        # Moving average
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)

    s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
    y = np.convolve(w / w.sum(), s, mode='same')

    return y[window_len - 1:-window_len + 1]


class QSpectrumAnalyzerSettings(QtGui.QDialog, Ui_QSpectrumAnalyzerSettings):
    """QSpectrumAnalyzer settings dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.executableEdit.setText(str(settings.value("rtl_power_executable") or "rtl_power"))
        self.waterfallHistorySizeSpinBox.setValue(int(settings.value("waterfall_history_size") or 100))
        self.sampleRateSpinBox.setValue(int(settings.value("sample_rate") or 2560000))

        backend = str(settings.value("backend") or "rtl_power")
        i = self.backendComboBox.findText(backend)
        if i == -1:
            self.backendComboBox.setCurrentIndex(0)
        else:
            self.backendComboBox.setCurrentIndex(i)

    @QtCore.pyqtSlot()
    def on_executableButton_clicked(self):
        """Open file dialog when button is clicked"""
        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select executable - QSpectrumAnalyzer"))
        if filename:
            self.executableEdit.setText(filename)

    @QtCore.pyqtSlot(str)
    def on_backendComboBox_currentIndexChanged(self, text):
        """Change executable when backend is changed"""
        self.executableEdit.setText(text)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("rtl_power_executable", self.executableEdit.text())
        settings.setValue("waterfall_history_size", self.waterfallHistorySizeSpinBox.value())
        settings.setValue("sample_rate", self.sampleRateSpinBox.value())
        settings.setValue("backend", self.backendComboBox.currentText())
        QtGui.QDialog.accept(self)


class QSpectrumAnalyzerSmooth(QtGui.QDialog, Ui_QSpectrumAnalyzerSmooth):
    """QSpectrumAnalyzer smoothing dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.windowLengthSpinBox.setValue(int(settings.value("smooth_length") or 11))

        window_function = str(settings.value("smooth_window") or "hanning")
        i = self.windowFunctionComboBox.findText(window_function)
        if i == -1:
            self.windowFunctionComboBox.setCurrentIndex(0)
        else:
            self.windowFunctionComboBox.setCurrentIndex(i)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("smooth_length", self.windowLengthSpinBox.value())
        settings.setValue("smooth_window", self.windowFunctionComboBox.currentText())
        QtGui.QDialog.accept(self)


class QSpectrumAnalyzerMainWindow(QtGui.QMainWindow, Ui_QSpectrumAnalyzerMainWindow):
    """QSpectrumAnalyzer main window"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Setup rtl_power thread and connect signals
        self.waterfall_history_size = 100
        self.smooth = False
        self.smooth_length = 11
        self.smooth_window = 'hanning'
        self.peak_hold = False
        self.data_counter = 0
        self.data_timestamp = 0
        self.data_peak_hold = None
        self.rtl_power_thread = None
        self.setup_rtl_power_thread()

        # Update UI
        self.create_plot()
        self.create_waterfall()
        self.update_buttons()
        self.load_settings()

    def setup_rtl_power_thread(self):
        """Create rtl_power_thread and connect signals to slots"""
        if self.rtl_power_thread:
            self.stop()

        settings = QtCore.QSettings()
        backend = str(settings.value("backend") or "rtl_power")
        if backend == "rtl_power_fftw":
            self.rtl_power_thread = RtlPowerFftwThread()
        else:
            self.rtl_power_thread = RtlPowerThread()

        self.rtl_power_thread.dataUpdated.connect(self.update_data)
        self.rtl_power_thread.rtlPowerStarted.connect(self.update_buttons)
        self.rtl_power_thread.rtlPowerStopped.connect(self.update_buttons)

    def create_plot(self):
        """Create main spectrum plot"""
        self.posLabel = self.mainPlotLayout.addLabel(row=0, col=0, justify="right")
        self.mainPlotWidget = self.mainPlotLayout.addPlot(row=1, col=0)
        self.mainPlotWidget.showGrid(x=True, y=True)
        self.mainPlotWidget.setLabel("left", "Power", units="dBm")
        self.mainPlotWidget.setLabel("bottom", "Frequency", units="Hz")
        self.mainPlotWidget.setLimits(xMin=0)
        self.mainPlotWidget.showButtons()

        # Create spectrum curve
        self.curve = self.mainPlotWidget.plot()

        # Create peak hold curve
        self.curve_peak_hold = self.mainPlotWidget.plot(pen='r')

        # Create crosshair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.mainPlotWidget.addItem(self.vLine, ignoreBounds=True)
        self.mainPlotWidget.addItem(self.hLine, ignoreBounds=True)
        self.mouseProxy = pg.SignalProxy(self.mainPlotWidget.scene().sigMouseMoved,
                                         rateLimit=60, slot=self.mouse_moved)

    def mouse_moved(self, evt):
        """Update crosshair when mouse is moved"""
        pos = evt[0]
        if self.mainPlotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.mainPlotWidget.vb.mapSceneToView(pos)
            self.posLabel.setText(
                "<span style='font-size: 12pt'>f={:0.3f} MHz, P={:0.3f} dBm</span>".format(mousePoint.x() / 1e6,
                                                                                           mousePoint.y())
            )
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def create_waterfall(self):
        """Create waterfall plot"""
        self.waterfallPlotWidget = self.waterfallPlotLayout.addPlot()
        self.waterfallPlotLayout.addItem(self.waterfallPlotWidget)
        self.waterfallPlotWidget.setLabel("bottom", "Frequency", units="Hz")
        self.waterfallPlotWidget.setLabel("left", "Time")
        self.waterfallPlotWidget.setYRange(-self.waterfall_history_size, 0)
        self.waterfallPlotWidget.setLimits(xMin=0, yMax=0)
        self.waterfallPlotWidget.showButtons()
        #self.waterfallPlotWidget.setAspectLocked(True)
        #self.waterfallPlotWidget.setDownsampling(mode="peak")
        #self.waterfallPlotWidget.setClipToView(True)

        # Link waterfall plot to main plot
        self.mainPlotWidget.setXLink(self.waterfallPlotWidget)

        # Setup histogram widget (for controlling waterfall plot levels and gradients)
        self.waterfallHistogram = pg.HistogramLUTItem()
        self.histogramPlotLayout.addItem(self.waterfallHistogram)
        self.waterfallHistogram.gradient.loadPreset("flame")
        #self.waterfallHistogram.setHistogramRange(-50, 0)
        #self.waterfallHistogram.setLevels(-50, 0)

    def update_buttons(self):
        """Update state of control buttons"""
        self.startButton.setEnabled(not self.rtl_power_thread.alive)
        self.singleShotButton.setEnabled(not self.rtl_power_thread.alive)
        self.stopButton.setEnabled(self.rtl_power_thread.alive)

    def update_data(self, data):
        """Update plots when new data is received"""
        self.data_counter += 1

        # Update waterfall
        self.update_waterfall(data)

        # Update main spectrum plot
        if self.smooth:
            # Apply smoothing to data
            data["y"] = smooth(data["y"],
                               window_len=self.smooth_length,
                               window=self.smooth_window)

        if self.peak_hold:
            if self.data_peak_hold is None:
                self.data_peak_hold = data["y"]
            else:
                # Update peak hold data
                for i, y in enumerate(data["y"]):
                    if y > self.data_peak_hold[i]:
                        self.data_peak_hold[i] = y

        self.update_plot(data)

        # Show number of hops and how much time did the sweep really take
        timestamp = time.time()
        self.show_status(self.tr("Frequency hops: {}   Sweep time: {:.2f} s").format(
            self.rtl_power_thread.params["hops"] or self.tr("N/A"),
            timestamp - self.data_timestamp
        ), timeout=0)
        self.data_timestamp = timestamp

    def update_plot(self, data):
        """Update main spectrum plot"""
        self.curve.setData(data["x"], data["y"])
        if self.peak_hold:
            self.curve_peak_hold.setData(data["x"], self.data_peak_hold)

    def update_waterfall(self, data):
        """Update waterfall plot"""
        # Create waterfall data array and waterfall image on first run
        if self.data_counter == 1:
            self.waterfallImgArray = np.zeros((self.waterfall_history_size, len(data["x"])))
            self.waterfallImg = pg.ImageItem()
            self.waterfallImg.scale((data["x"][-1] - data["x"][0]) / len(data["x"]), 1)
            self.waterfallPlotWidget.clear()
            self.waterfallPlotWidget.addItem(self.waterfallImg)

        # Roll down one and replace leading edge with new data
        self.waterfallImgArray = np.roll(self.waterfallImgArray, -1, axis=0)
        self.waterfallImgArray[-1] = data["y"]
        self.waterfallImg.setImage(self.waterfallImgArray[-self.data_counter:].T,
                                   autoLevels=False, autoRange=False)

        # Move waterfall image to always start at 0
        self.waterfallImg.setPos(data["x"][0],
                                 -self.data_counter if self.data_counter < self.waterfall_history_size
                                 else -self.waterfall_history_size)

        # Link histogram widget to waterfall image on first run
        # (must be done after first data is received or else levels would be wrong)
        if self.data_counter == 1:
            self.waterfallHistogram.setImageItem(self.waterfallImg)

    def load_settings(self):
        """Restore spectrum analyzer settings and window geometry"""
        settings = QtCore.QSettings()
        self.startFreqSpinBox.setValue(float(settings.value("start_freq") or 87.0))
        self.stopFreqSpinBox.setValue(float(settings.value("stop_freq") or 108.0))
        self.binSizeSpinBox.setValue(float(settings.value("bin_size") or 10.0))
        self.intervalSpinBox.setValue(float(settings.value("interval") or 10.0))
        self.gainSpinBox.setValue(int(settings.value("gain") or 0))
        self.ppmSpinBox.setValue(int(settings.value("ppm") or 0))
        self.cropSpinBox.setValue(int(settings.value("crop") or 0))
        self.peakHoldCheckBox.setChecked(int(settings.value("peak_hold") or 0))
        self.smoothCheckBox.setChecked(int(settings.value("smooth") or 0))

        # Restore window geometry
        if settings.value("window_state"):
            self.restoreState(settings.value("window_state"))
        if settings.value("plotsplitter_state"):
            self.plotSplitter.restoreState(settings.value("plotsplitter_state"))

        # Migration from older version of config file
        if int(settings.value("config_version") or 1) < 2:
            # Make tabs from docks when started for first time
            self.tabifyDockWidget(self.settingsDockWidget, self.levelsDockWidget)
            self.settingsDockWidget.raise_()
            self.set_dock_size(self.controlsDockWidget, 0, 0)
            self.set_dock_size(self.frequencyDockWidget, 0, 0)
            # Update config version
            settings.setValue("config_version", 2)

        # Window geometry has to be restored only after show(), because initial
        # maximization doesn't work otherwise (at least not in some window managers on X11)
        self.show()
        if settings.value("window_geometry"):
            self.restoreGeometry(settings.value("window_geometry"))

    def set_dock_size(self, dock, width, height):
        """Ugly hack for resizing QDockWidget (because it doesn't respect minimumSize / sizePolicy set in Designer)
           Link: https://stackoverflow.com/questions/2722939/c-resize-a-docked-qt-qdockwidget-programmatically"""
        old_min_size = dock.minimumSize()
        old_max_size = dock.maximumSize()

        if width >= 0:
            if dock.width() < width:
                dock.setMinimumWidth(width)
            else:
                dock.setMaximumWidth(width)

        if height >= 0:
            if dock.height() < height:
                dock.setMinimumHeight(height)
            else:
                dock.setMaximumHeight(height)

        QtCore.QTimer.singleShot(0, lambda: self.set_dock_size_callback(dock, old_min_size, old_max_size))

    def set_dock_size_callback(self, dock, old_min_size, old_max_size):
        """Return to original QDockWidget minimumSize and maximumSize after running set_dock_size()"""
        dock.setMinimumSize(old_min_size)
        dock.setMaximumSize(old_max_size)

    def save_settings(self):
        """Save spectrum analyzer settings and window geometry"""
        settings = QtCore.QSettings()
        settings.setValue("start_freq", float(self.startFreqSpinBox.value()))
        settings.setValue("stop_freq", float(self.stopFreqSpinBox.value()))
        settings.setValue("bin_size", float(self.binSizeSpinBox.value()))
        settings.setValue("interval", float(self.intervalSpinBox.value()))
        settings.setValue("gain", int(self.gainSpinBox.value()))
        settings.setValue("ppm", int(self.ppmSpinBox.value()))
        settings.setValue("crop", int(self.cropSpinBox.value()))
        settings.setValue("peak_hold", int(self.peakHoldCheckBox.isChecked()))
        settings.setValue("smooth", int(self.smoothCheckBox.isChecked()))

        # Save window geometry
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("plotsplitter_state", self.plotSplitter.saveState())

    def show_status(self, message, timeout=2000):
        """Show message in status bar"""
        self.statusbar.showMessage(message, timeout)

    def start(self, single_shot=False):
        """Start rtl_power thread"""
        settings = QtCore.QSettings()
        self.waterfall_history_size = int(settings.value("waterfall_history_size") or 100)
        self.peak_hold = bool(self.peakHoldCheckBox.isChecked())
        self.smooth = bool(self.smoothCheckBox.isChecked())
        self.smooth_length = int(settings.value("smooth_length") or 11)
        self.smooth_window = str(settings.value("smooth_window") or "hanning")
        self.data_counter = 0
        self.data_peak_hold = None
        self.data_timestamp = time.time()
        if not self.rtl_power_thread.alive:
            self.rtl_power_thread.setup(float(self.startFreqSpinBox.value()),
                                        float(self.stopFreqSpinBox.value()),
                                        float(self.binSizeSpinBox.value()),
                                        interval=float(self.intervalSpinBox.value()),
                                        gain=int(self.gainSpinBox.value()),
                                        ppm=int(self.ppmSpinBox.value()),
                                        crop=int(self.cropSpinBox.value()) / 100.0,
                                        single_shot=single_shot,
                                        sample_rate=int(settings.value("sample_rate") or 2560000))
            self.rtl_power_thread.start()

    def stop(self):
        """Stop rtl_power thread"""
        if self.rtl_power_thread.alive:
            self.rtl_power_thread.stop()

    @QtCore.pyqtSlot()
    def on_startButton_clicked(self):
        self.start()

    @QtCore.pyqtSlot()
    def on_singleShotButton_clicked(self):
        self.start(single_shot=True)

    @QtCore.pyqtSlot()
    def on_stopButton_clicked(self):
        self.stop()

    @QtCore.pyqtSlot(bool)
    def on_peakHoldCheckBox_toggled(self, checked):
        self.peak_hold = checked
        if not checked:
            self.data_peak_hold = None
            self.curve_peak_hold.clear()

    @QtCore.pyqtSlot(bool)
    def on_smoothCheckBox_toggled(self, checked):
        self.smooth = checked
        if self.peak_hold:
            self.data_peak_hold = None
            self.curve_peak_hold.clear()

    @QtCore.pyqtSlot()
    def on_smoothButton_clicked(self):
        dialog = QSpectrumAnalyzerSmooth(self)
        if dialog.exec_():
            settings = QtCore.QSettings()
            self.smooth_length = int(settings.value("smooth_length") or 11)
            self.smooth_window = str(settings.value("smooth_window") or "hanning")
            self.data_peak_hold = None
            self.curve_peak_hold.clear()

    @QtCore.pyqtSlot()
    def on_action_Settings_triggered(self):
        dialog = QSpectrumAnalyzerSettings(self)
        if dialog.exec_():
            self.setup_rtl_power_thread()

    @QtCore.pyqtSlot()
    def on_action_About_triggered(self):
        QtGui.QMessageBox.information(self, self.tr("About - QSpectrumAnalyzer"),
                                      self.tr("QSpectrumAnalyzer {}").format(__version__))

    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    def closeEvent(self, event):
        """Save settings when main window is closed"""
        self.stop()
        self.save_settings()


class RtlPowerBaseThread(QtCore.QThread):
    """Thread which runs rtl_power process"""
    dataUpdated = QtCore.pyqtSignal(object)
    rtlPowerStarted = QtCore.pyqtSignal()
    rtlPowerStopped = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.alive = False
        self.process = None

    def stop(self):
        """Stop rtl_power thread"""
        self.process_stop()
        self.alive = False
        self.wait()

    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, sample_rate=2560000):
        """Setup rtl_power params"""
        raise NotImplementedError

    def process_start(self):
        """Start rtl_power process"""
        raise NotImplementedError

    def process_stop(self):
        """Terminate rtl_power process"""
        if self.process:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
            self.process.wait()
            self.process = None

    def parse_output(self, line):
        """Parse one line of output from rtl_power"""
        raise NotImplementedError

    def run(self):
        """Rtl_power thread main loop"""
        self.process_start()
        self.alive = True
        self.rtlPowerStarted.emit()

        for line in self.process.stdout:
            if not self.alive:
                break
            self.parse_output(line)

        self.process_stop()
        self.alive = False
        self.rtlPowerStopped.emit()


class RtlPowerThread(RtlPowerBaseThread):
    """Thread which runs rtl_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, sample_rate=2560000):
        """Setup rtl_power params"""
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "bin_size": bin_size,
            "interval": interval,
            "hops": 0,
            "gain": gain,
            "ppm": ppm,
            "crop": crop,
            "single_shot": single_shot
        }
        self.databuffer = {}
        self.last_timestamp = ""

        print("rtl_power params:")
        pprint.pprint(self.params)
        print()

    def process_start(self):
        """Start rtl_power process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                str(settings.value("rtl_power_executable") or "rtl_power"),
                "-f", "{}M:{}M:{}k".format(self.params["start_freq"],
                                           self.params["stop_freq"],
                                           self.params["bin_size"]),
                "-i", "{}".format(self.params["interval"]),
                "-p", "{}".format(self.params["ppm"]),
                "-c", "{}".format(self.params["crop"])
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["single_shot"]:
                cmdline.append("-1")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                                            universal_newlines=True)

    def parse_output(self, line):
        """Parse one line of output from rtl_power"""
        line = [col.strip() for col in line.split(",")]
        timestamp = " ".join(line[:2])
        start_freq = int(line[2])
        stop_freq = int(line[3])
        step = float(line[4])
        samples = float(line[5])

        x_axis = list(np.arange(start_freq, stop_freq, step))
        y_axis = [float(y) for y in line[6:]]
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis), use newer version of rtl_power!")
            if len(x_axis) > len(y_axis):
                print("Trimming x_axis...")
                x_axis = x_axis[:len(y_axis)]
            else:
                print("Trimming y_axis...")
                y_axis = y_axis[:len(x_axis)]

        if timestamp != self.last_timestamp:
            self.last_timestamp = timestamp
            self.databuffer = {"timestamp": timestamp,
                               "x": x_axis,
                               "y": y_axis}
        else:
            self.databuffer["x"].extend(x_axis)
            self.databuffer["y"].extend(y_axis)

        # This have to be stupid like this to be compatible with old broken version of rtl_power. Right way is:
        # if stop_freq == self.params["stop_freq"] * 1e6:
        if stop_freq > (self.params["stop_freq"] * 1e6) - step:
            self.dataUpdated.emit(self.databuffer)


class RtlPowerFftwThread(RtlPowerBaseThread):
    """Thread which runs rtl_power_fftw process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, sample_rate=2560000):
        """Setup rtl_power_fftw params"""
        crop = crop * 100
        overlap = crop * 2
        freq_range = stop_freq * 1e6 - start_freq * 1e6
        min_overhang = sample_rate * overlap * 0.01
        hops = math.ceil((freq_range - min_overhang) / (sample_rate - min_overhang))
        overhang = (hops * sample_rate - freq_range) / (hops - 1) if hops > 1 else 0
        bins = math.ceil(sample_rate / (bin_size * 1e3))
        crop_freq = sample_rate * crop * 0.01

        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "freq_range": freq_range,
            "sample_rate": sample_rate,
            "bin_size": bin_size,
            "bins": bins,
            "interval": interval,
            "hops": hops,
            "time": interval / hops,
            "gain": gain * 10,
            "ppm": ppm,
            "crop": crop,
            "overlap": overlap,
            "min_overhang": min_overhang,
            "overhang": overhang,
            "single_shot": single_shot
        }
        self.freqs = [self.get_hop_freq(hop) for hop in range(hops)]
        self.freqs_crop = [(f[0] + crop_freq, f[1] - crop_freq) for f in self.freqs]
        self.databuffer = {"timestamp": [], "x": [], "y": []}
        self.databuffer_hop = {"timestamp": [], "x": [], "y": []}
        self.hop = 0
        self.prev_line = ""

        print("rtl_power_fftw params:")
        pprint.pprint(self.params)
        print()

    def get_hop_freq(self, hop):
        """Get start and stop frequency for particular hop"""
        start_freq = self.params["start_freq"] * 1e6 + (self.params["sample_rate"] - self.params["overhang"]) * hop
        stop_freq = start_freq + self.params["sample_rate"] - (self.params["sample_rate"] / self.params["bins"])
        return (start_freq, stop_freq)

    def process_start(self):
        """Start rtl_power_fftw process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                str(settings.value("rtl_power_executable") or "rtl_power_fftw"),
                "-f", "{}M:{}M".format(self.params["start_freq"],
                                       self.params["stop_freq"]),
                "-b", "{}".format(self.params["bins"]),
                "-t", "{}".format(self.params["time"]),
                "-r", "{}".format(self.params["sample_rate"]),
                "-p", "{}".format(self.params["ppm"]),
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["overlap"] > 0:
                cmdline.extend(["-o", "{}".format(self.params["overlap"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=True)

    def parse_output(self, line):
        """Parse one line of output from rtl_power_fftw"""
        line = line.strip()

        # One empty line => new hop
        if not line and self.prev_line:
            self.hop += 1
            self.databuffer["x"].extend(self.databuffer_hop["x"])
            self.databuffer["y"].extend(self.databuffer_hop["y"])
            self.databuffer_hop = {"timestamp": [], "x": [], "y": []}

        # Two empty lines => new set
        elif not line and not self.prev_line:
            self.hop = 0
            self.dataUpdated.emit(self.databuffer)
            self.databuffer = {"timestamp": [], "x": [], "y": []}

        # Get timestamp for new hop and set
        elif line.startswith("# Acquisition start:"):
            timestamp = line.split(":", 1)[1].strip()
            if not self.databuffer_hop["timestamp"]:
                self.databuffer_hop["timestamp"] = timestamp
            if not self.databuffer["timestamp"]:
                self.databuffer["timestamp"] = timestamp

        # Skip other comments
        elif line.startswith("#"):
            pass

        # Parse frequency and power
        elif line[0].isdigit():
            freq, power = line.split()
            freq, power = float(freq), float(power)
            start_freq, stop_freq = self.freqs_crop[self.hop]

            # Apply cropping
            if freq >= start_freq and freq <= stop_freq:
                # Skip overlapping frequencies
                if not self.databuffer["x"] or freq > self.databuffer["x"][-1]:
                    #print("  {:.3f} MHz".format(freq / 1e6))
                    self.databuffer_hop["x"].append(freq)
                    self.databuffer_hop["y"].append(power)
                else:
                    #print("  Overlapping {:.3f} MHz".format(freq / 1e6))
                    pass
            else:
                #print("  Cropping {:.3f} MHz".format(freq / 1e6))
                pass

        self.prev_line = line


def main():
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("QSpectrumAnalyzer")
    app.setOrganizationDomain("qspectrumanalyzer.eutopia.cz")
    app.setApplicationName("QSpectrumAnalyzer")
    window = QSpectrumAnalyzerMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
