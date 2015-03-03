#!/usr/bin/env python

import sys, csv, subprocess, signal

import numpy as np
import pyqtgraph as pg

from PyQt4 import QtCore, QtGui
from qspectrumanalyzer.version import __version__
from qspectrumanalyzer.ui_qspectrumanalyzer_settings import Ui_QSpectrumAnalyzerSettings
from qspectrumanalyzer.ui_qspectrumanalyzer import Ui_QSpectrumAnalyzerMainWindow


# Basic settings
pg.setConfigOptions(antialias=True)

# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)


class QSpectrumAnalyzerSettings(QtGui.QDialog, Ui_QSpectrumAnalyzerSettings):
    """QSpectrumAnalyzer settings dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.rtlPowerExecutableEdit.setText(str(settings.value("rtl_power_executable") or "rtl_power"))
        self.waterfallHistorySizeSpinBox.setValue(int(settings.value("waterfall_history_size") or 100))

    @QtCore.pyqtSlot()
    def on_rtlPowerExecutableButton_clicked(self):
        """Open file dialog when button is clicked"""
        filename = QtGui.QFileDialog.getOpenFileName(self, "QSpectrumAnalyzer - rtl_power executable")
        if filename:
            self.rtlPowerExecutableEdit.setText(filename)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("rtl_power_executable", self.rtlPowerExecutableEdit.text())
        settings.setValue("waterfall_history_size", self.waterfallHistorySizeSpinBox.value())
        QtGui.QDialog.accept(self)


class QSpectrumAnalyzerMainWindow(QtGui.QMainWindow, Ui_QSpectrumAnalyzerMainWindow):
    """QSpectrumAnalyzer main window"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Setup rtl_power thread and connect signals
        self.waterfall_history_size = 100
        self.datacounter = 0
        self.rtl_power_thread = RtlPowerThread()
        self.rtl_power_thread.dataUpdated.connect(self.update_data)
        self.rtl_power_thread.rtlPowerStarted.connect(self.update_buttons)
        self.rtl_power_thread.rtlPowerStopped.connect(self.update_buttons)

        # Update UI
        self.create_plot()
        self.create_waterfall()
        self.update_buttons()
        self.load_settings()

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
        self.datacounter += 1
        self.update_plot(data)
        self.update_waterfall(data)

    def update_plot(self, data):
        """Update main spectrum plot"""
        self.curve.setData(data["x"], data["y"])

    def update_waterfall(self, data):
        """Update waterfall plot"""
        # Create waterfall data array and waterfall image on first run
        if self.datacounter == 1:
            self.waterfallImgArray = np.zeros((self.waterfall_history_size, len(data["x"])))
            self.waterfallImg = pg.ImageItem()
            self.waterfallImg.scale((data["x"][-1] - data["x"][0]) / len(data["x"]), 1)
            self.waterfallPlotWidget.clear()
            self.waterfallPlotWidget.addItem(self.waterfallImg)

        # Roll down one and replace leading edge with new data
        self.waterfallImgArray = np.roll(self.waterfallImgArray, -1, axis=0)
        self.waterfallImgArray[-1] = data["y"]
        self.waterfallImg.setImage(self.waterfallImgArray[-self.datacounter:].T,
                                   autoLevels=False, autoRange=False)

        # Move waterfall image to always start at 0
        self.waterfallImg.setPos(data["x"][0],
                                 -self.datacounter if self.datacounter < self.waterfall_history_size
                                 else -self.waterfall_history_size)

        # Link histogram widget to waterfall image on first run
        # (must be done after first data is received or else levels would be wrong)
        if self.datacounter == 1:
            self.waterfallHistogram.setImageItem(self.waterfallImg)

    def load_settings(self):
        """Restore spectrum analyzer settings and window geometry"""
        settings = QtCore.QSettings()
        self.startFreqSpinBox.setValue(float(settings.value("start_freq") or 87.0))
        self.stopFreqSpinBox.setValue(float(settings.value("stop_freq") or 108.0))
        self.binSizeSpinBox.setValue(float(settings.value("bin_size") or 10.0))
        self.intervalSpinBox.setValue(int(settings.value("interval") or 10))
        self.gainSpinBox.setValue(int(settings.value("gain") or 0))
        self.ppmSpinBox.setValue(int(settings.value("ppm") or 0))
        self.cropSpinBox.setValue(int(settings.value("crop") or 0))

        if settings.value("window_geometry"):
            self.restoreGeometry(settings.value("window_geometry"))
        if settings.value("window_state"):
            self.restoreState(settings.value("window_state"))
        if settings.value("plotsplitter_state"):
            self.plotSplitter.restoreState(settings.value("plotsplitter_state"))

    def save_settings(self):
        """Save spectrum analyzer settings and window geometry"""
        settings = QtCore.QSettings()
        settings.setValue("start_freq", float(self.startFreqSpinBox.value()))
        settings.setValue("stop_freq", float(self.stopFreqSpinBox.value()))
        settings.setValue("bin_size", float(self.binSizeSpinBox.value()))
        settings.setValue("interval", int(self.intervalSpinBox.value()))
        settings.setValue("gain", int(self.gainSpinBox.value()))
        settings.setValue("ppm", int(self.ppmSpinBox.value()))
        settings.setValue("crop", int(self.cropSpinBox.value()))

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
        self.datacounter = 0
        if not self.rtl_power_thread.alive:
            self.rtl_power_thread.setup(float(self.startFreqSpinBox.value()),
                                        float(self.stopFreqSpinBox.value()),
                                        float(self.binSizeSpinBox.value()),
                                        interval=int(self.intervalSpinBox.value()),
                                        gain=int(self.gainSpinBox.value()),
                                        ppm=int(self.ppmSpinBox.value()),
                                        crop=int(self.cropSpinBox.value()) / 100.0,
                                        single_shot=single_shot)
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

    @QtCore.pyqtSlot()
    def on_action_Settings_triggered(self):
        dialog = QSpectrumAnalyzerSettings(self)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def on_action_About_triggered(self):
        QtGui.QMessageBox.information(self, self.tr("About"), self.tr("QSpectrumAnalyzer {}").format(__version__))

    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    def closeEvent(self, event):
        """Save settings when main window is closed"""
        self.rtl_power_thread.stop()
        self.save_settings()


class RtlPowerThread(QtCore.QThread):
    """Thread which runs rtl_power process"""
    dataUpdated = QtCore.pyqtSignal(object)
    rtlPowerStarted = QtCore.pyqtSignal()
    rtlPowerStopped = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.alive = False
        self.process = None
        self.params = {}
        self.databuffer = {}
        self.last_timestamp = ""

    def stop(self):
        """Stop rtl_power thread"""
        self.process_stop()
        self.alive = False
        self.wait()

    def setup(self, start_freq, stop_freq, bin_size, interval=10,
              gain=-1, ppm=0, crop=0, single_shot=False):
        """Setup rtl_power params"""
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "bin_size": bin_size,
            "interval": interval,
            "gain": gain,
            "ppm": ppm,
            "crop": crop,
            "single_shot": single_shot
        }

    def process_stop(self):
        """Terminate rtl_power process"""
        if self.process:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
            self.process.wait()
            self.process = None

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
        """Parse one preprocessed line of output from rtl_power"""
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
            return self.databuffer

    def run(self):
        """Rtl_power thread main loop"""
        self.process_start()
        self.alive = True
        self.rtlPowerStarted.emit()

        reader = csv.reader(self.process.stdout, skipinitialspace=True,
                            delimiter=",", quoting=csv.QUOTE_NONE)
        for line in reader:
            if not self.alive:
                break
            self.parse_output(line)

        self.process_stop()
        self.alive = False
        self.rtlPowerStopped.emit()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("QSpectrumAnalyzer")
    app.setOrganizationDomain("qspectrumanalyzer.eutopia.cz")
    app.setApplicationName("QSpectrumAnalyzer")
    window = QSpectrumAnalyzerMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
