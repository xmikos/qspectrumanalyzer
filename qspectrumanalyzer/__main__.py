#!/usr/bin/env python

import sys, signal, time

from PyQt4 import QtCore, QtGui

from qspectrumanalyzer.version import __version__
from qspectrumanalyzer.backend import RtlPowerThread, RtlPowerFftwThread
from qspectrumanalyzer.plot import SpectrumPlotWidget, WaterfallPlotWidget

from qspectrumanalyzer.ui_qspectrumanalyzer_settings import Ui_QSpectrumAnalyzerSettings
from qspectrumanalyzer.ui_qspectrumanalyzer_smooth import Ui_QSpectrumAnalyzerSmooth
from qspectrumanalyzer.ui_qspectrumanalyzer import Ui_QSpectrumAnalyzerMainWindow

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
        self.prev_data_timestamp = None
        self.rtl_power_thread = None
        self.setup_rtl_power_thread()

        # Create plot widgets and update UI
        self.spectrumPlotWidget = SpectrumPlotWidget(self.mainPlotLayout)
        self.waterfallPlotWidget = WaterfallPlotWidget(self.waterfallPlotLayout, self.histogramPlotLayout)

        # Link waterfall plot to main plot
        self.spectrumPlotWidget.mainPlotWidget.setXLink(self.waterfallPlotWidget.waterfallPlotWidget)

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

    def update_buttons(self):
        """Update state of control buttons"""
        self.startButton.setEnabled(not self.rtl_power_thread.alive)
        self.singleShotButton.setEnabled(not self.rtl_power_thread.alive)
        self.stopButton.setEnabled(self.rtl_power_thread.alive)

    def update_data(self, data):
        """Update plots when new data is received"""
        self.waterfallPlotWidget.update_plot(data)
        self.spectrumPlotWidget.update_plot(data)

        # Show number of hops and how much time did the sweep really take
        timestamp = time.time()
        self.show_status(self.tr("Frequency hops: {}   Sweep time: {:.2f} s").format(
            self.rtl_power_thread.params["hops"] or self.tr("N/A"),
            timestamp - self.prev_data_timestamp
        ), timeout=0)
        self.prev_data_timestamp = timestamp

    def start(self, single_shot=False):
        """Start rtl_power thread"""
        settings = QtCore.QSettings()
        self.prev_data_timestamp = time.time()
        self.waterfallPlotWidget.history_size = int(settings.value("waterfall_history_size") or 100)
        self.waterfallPlotWidget.counter = 0
        self.spectrumPlotWidget.peak_hold = bool(self.peakHoldCheckBox.isChecked())
        self.spectrumPlotWidget.smooth = bool(self.smoothCheckBox.isChecked())
        self.spectrumPlotWidget.smooth_length = int(settings.value("smooth_length") or 11)
        self.spectrumPlotWidget.smooth_window = str(settings.value("smooth_window") or "hanning")
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
        self.spectrumPlotWidget.peak_hold = checked
        if not checked:
            self.spectrumPlotWidget.peak_hold_clear()

    @QtCore.pyqtSlot(bool)
    def on_smoothCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.smooth = checked
        if self.spectrumPlotWidget.peak_hold:
            self.spectrumPlotWidget.peak_hold_clear()

    @QtCore.pyqtSlot()
    def on_smoothButton_clicked(self):
        dialog = QSpectrumAnalyzerSmooth(self)
        if dialog.exec_():
            settings = QtCore.QSettings()
            self.spectrumPlotWidget.smooth_length = int(settings.value("smooth_length") or 11)
            self.spectrumPlotWidget.smooth_window = str(settings.value("smooth_window") or "hanning")
            self.spectrumPlotWidget.peak_hold_clear()

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


def main():
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("QSpectrumAnalyzer")
    app.setOrganizationDomain("qspectrumanalyzer.eutopia.cz")
    app.setApplicationName("QSpectrumAnalyzer")
    window = QSpectrumAnalyzerMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
