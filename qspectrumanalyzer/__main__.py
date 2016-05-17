#!/usr/bin/env python

import sys, signal, time

from PyQt4 import QtCore, QtGui

from qspectrumanalyzer.version import __version__
from qspectrumanalyzer.backend import RtlPowerThread, RtlPowerFftwThread
from qspectrumanalyzer.data import DataStorage
from qspectrumanalyzer.plot import SpectrumPlotWidget, WaterfallPlotWidget
from qspectrumanalyzer.utils import color_to_str, str_to_color

from qspectrumanalyzer.ui_qspectrumanalyzer_settings import Ui_QSpectrumAnalyzerSettings
from qspectrumanalyzer.ui_qspectrumanalyzer_smooth import Ui_QSpectrumAnalyzerSmooth
from qspectrumanalyzer.ui_qspectrumanalyzer_persistence import Ui_QSpectrumAnalyzerPersistence
from qspectrumanalyzer.ui_qspectrumanalyzer_colors import Ui_QSpectrumAnalyzerColors
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
        self.executableEdit.setText(settings.value("rtl_power_executable", "rtl_power"))
        self.waterfallHistorySizeSpinBox.setValue(settings.value("waterfall_history_size", 100, int))
        self.sampleRateSpinBox.setValue(settings.value("sample_rate", 2560000, int))

        backend = settings.value("backend", "rtl_power")
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
    """QSpectrumAnalyzer spectrum smoothing dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.windowLengthSpinBox.setValue(settings.value("smooth_length", 11, int))

        window_function = settings.value("smooth_window", "hanning")
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


class QSpectrumAnalyzerPersistence(QtGui.QDialog, Ui_QSpectrumAnalyzerPersistence):
    """QSpectrumAnalyzer spectrum persistence dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.persistenceLengthSpinBox.setValue(settings.value("persistence_length", 5, int))

        decay_function = settings.value("persistence_decay", "exponential")
        i = self.decayFunctionComboBox.findText(decay_function)
        if i == -1:
            self.decayFunctionComboBox.setCurrentIndex(0)
        else:
            self.decayFunctionComboBox.setCurrentIndex(i)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("persistence_length", self.persistenceLengthSpinBox.value())
        settings.setValue("persistence_decay", self.decayFunctionComboBox.currentText())
        QtGui.QDialog.accept(self)


class QSpectrumAnalyzerColors(QtGui.QDialog, Ui_QSpectrumAnalyzerColors):
    """QSpectrumAnalyzer colors dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.mainColorButton.setColor(str_to_color(settings.value("main_color", "255, 255, 0, 255")))
        self.peakHoldMaxColorButton.setColor(str_to_color(settings.value("peak_hold_max_color", "255, 0, 0, 255")))
        self.peakHoldMinColorButton.setColor(str_to_color(settings.value("peak_hold_min_color", "0, 0, 255, 255")))
        self.averageColorButton.setColor(str_to_color(settings.value("average_color", "0, 255, 255, 255")))
        self.persistenceColorButton.setColor(str_to_color(settings.value("persistence_color", "0, 255, 0, 255")))

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("main_color", color_to_str(self.mainColorButton.color()))
        settings.setValue("peak_hold_max_color", color_to_str(self.peakHoldMaxColorButton.color()))
        settings.setValue("peak_hold_min_color", color_to_str(self.peakHoldMinColorButton.color()))
        settings.setValue("average_color", color_to_str(self.averageColorButton.color()))
        settings.setValue("persistence_color", color_to_str(self.persistenceColorButton.color()))
        QtGui.QDialog.accept(self)


class QSpectrumAnalyzerMainWindow(QtGui.QMainWindow, Ui_QSpectrumAnalyzerMainWindow):
    """QSpectrumAnalyzer main window"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Create plot widgets and update UI
        self.spectrumPlotWidget = SpectrumPlotWidget(self.mainPlotLayout)
        self.waterfallPlotWidget = WaterfallPlotWidget(self.waterfallPlotLayout, self.histogramPlotLayout)

        # Link main spectrum plot to waterfall plot
        self.spectrumPlotWidget.plot.setXLink(self.waterfallPlotWidget.plot)

        # Setup rtl_power thread and connect signals
        self.prev_data_timestamp = None
        self.data_storage = None
        self.rtl_power_thread = None
        self.setup_rtl_power_thread()

        self.update_buttons()
        self.load_settings()

    def setup_rtl_power_thread(self):
        """Create rtl_power_thread and connect signals to slots"""
        if self.rtl_power_thread:
            self.stop()

        settings = QtCore.QSettings()
        self.data_storage = DataStorage(max_history_size=settings.value("waterfall_history_size", 100, int))
        self.data_storage.data_updated.connect(self.update_data)
        self.data_storage.data_updated.connect(self.spectrumPlotWidget.update_plot)
        self.data_storage.data_updated.connect(self.spectrumPlotWidget.update_persistence)
        self.data_storage.data_recalculated.connect(self.spectrumPlotWidget.recalculate_plot)
        self.data_storage.data_recalculated.connect(self.spectrumPlotWidget.recalculate_persistence)
        self.data_storage.history_updated.connect(self.waterfallPlotWidget.update_plot)
        self.data_storage.average_updated.connect(self.spectrumPlotWidget.update_average)
        self.data_storage.peak_hold_max_updated.connect(self.spectrumPlotWidget.update_peak_hold_max)
        self.data_storage.peak_hold_min_updated.connect(self.spectrumPlotWidget.update_peak_hold_min)

        backend = settings.value("backend", "rtl_power")
        if backend == "rtl_power_fftw":
            self.rtl_power_thread = RtlPowerFftwThread(self.data_storage)
        else:
            self.rtl_power_thread = RtlPowerThread(self.data_storage)

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
        self.startFreqSpinBox.setValue(settings.value("start_freq", 87.0, float))
        self.stopFreqSpinBox.setValue(settings.value("stop_freq", 108.0, float))
        self.binSizeSpinBox.setValue(settings.value("bin_size", 10.0, float))
        self.intervalSpinBox.setValue(settings.value("interval", 10.0, float))
        self.gainSpinBox.setValue(settings.value("gain", 0, int))
        self.ppmSpinBox.setValue(settings.value("ppm", 0, int))
        self.cropSpinBox.setValue(settings.value("crop", 0, int))
        self.mainCurveCheckBox.setChecked(settings.value("main_curve", 1, int))
        self.peakHoldMaxCheckBox.setChecked(settings.value("peak_hold_max", 0, int))
        self.peakHoldMinCheckBox.setChecked(settings.value("peak_hold_min", 0, int))
        self.averageCheckBox.setChecked(settings.value("average", 0, int))
        self.smoothCheckBox.setChecked(settings.value("smooth", 0, int))
        self.persistenceCheckBox.setChecked(settings.value("persistence", 0, int))

        # Restore window state
        if settings.value("window_state"):
            self.restoreState(settings.value("window_state"))
        if settings.value("plotsplitter_state"):
            self.plotSplitter.restoreState(settings.value("plotsplitter_state"))

        # Migration from older version of config file
        if settings.value("config_version", 1, int) < 2:
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
        settings.setValue("start_freq", self.startFreqSpinBox.value())
        settings.setValue("stop_freq", self.stopFreqSpinBox.value())
        settings.setValue("bin_size", self.binSizeSpinBox.value())
        settings.setValue("interval", self.intervalSpinBox.value())
        settings.setValue("gain", self.gainSpinBox.value())
        settings.setValue("ppm", self.ppmSpinBox.value())
        settings.setValue("crop", self.cropSpinBox.value())
        settings.setValue("main_curve", int(self.mainCurveCheckBox.isChecked()))
        settings.setValue("peak_hold_max", int(self.peakHoldMaxCheckBox.isChecked()))
        settings.setValue("peak_hold_min", int(self.peakHoldMinCheckBox.isChecked()))
        settings.setValue("average", int(self.averageCheckBox.isChecked()))
        settings.setValue("smooth", int(self.smoothCheckBox.isChecked()))
        settings.setValue("persistence", int(self.persistenceCheckBox.isChecked()))

        # Save window state and geometry
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

    def update_data(self, data_storage):
        """Update GUI when new data is received"""
        # Show number of hops and how much time did the sweep really take
        timestamp = time.time()
        sweep_time = timestamp - self.prev_data_timestamp
        self.prev_data_timestamp = timestamp

        self.show_status(
            self.tr("Frequency hops: {} | Sweep time: {:.2f} s | FPS: {:.2f}").format(
                self.rtl_power_thread.params["hops"] or self.tr("N/A"),
                sweep_time,
                1 / sweep_time
            ),
            timeout=0
        )

    def start(self, single_shot=False):
        """Start rtl_power thread"""
        settings = QtCore.QSettings()
        self.prev_data_timestamp = time.time()

        self.data_storage.reset()
        self.data_storage.set_smooth(
            bool(self.smoothCheckBox.isChecked()),
            settings.value("smooth_length", 11, int),
            settings.value("smooth_window", "hanning"),
            recalculate=False
        )

        self.waterfallPlotWidget.history_size = settings.value("waterfall_history_size", 100, int)
        self.waterfallPlotWidget.clear_plot()

        self.spectrumPlotWidget.main_curve = bool(self.mainCurveCheckBox.isChecked())
        self.spectrumPlotWidget.main_color = str_to_color(settings.value("main_color", "255, 255, 0, 255"))
        self.spectrumPlotWidget.peak_hold_max = bool(self.peakHoldMaxCheckBox.isChecked())
        self.spectrumPlotWidget.peak_hold_max_color = str_to_color(settings.value("peak_hold_max_color", "255, 0, 0, 255"))
        self.spectrumPlotWidget.peak_hold_min = bool(self.peakHoldMinCheckBox.isChecked())
        self.spectrumPlotWidget.peak_hold_min_color = str_to_color(settings.value("peak_hold_min_color", "0, 0, 255, 255"))
        self.spectrumPlotWidget.average = bool(self.averageCheckBox.isChecked())
        self.spectrumPlotWidget.average_color = str_to_color(settings.value("average_color", "0, 255, 255, 255"))
        self.spectrumPlotWidget.persistence = bool(self.persistenceCheckBox.isChecked())
        self.spectrumPlotWidget.persistence_length = settings.value("persistence_length", 5, int)
        self.spectrumPlotWidget.persistence_decay = settings.value("persistence_decay", "exponential")
        self.spectrumPlotWidget.persistence_color = str_to_color(settings.value("persistence_color", "0, 255, 0, 255"))
        self.spectrumPlotWidget.clear_plot()
        self.spectrumPlotWidget.clear_peak_hold_max()
        self.spectrumPlotWidget.clear_peak_hold_min()
        self.spectrumPlotWidget.clear_average()
        self.spectrumPlotWidget.clear_persistence()

        if not self.rtl_power_thread.alive:
            self.rtl_power_thread.setup(float(self.startFreqSpinBox.value()),
                                        float(self.stopFreqSpinBox.value()),
                                        float(self.binSizeSpinBox.value()),
                                        interval=float(self.intervalSpinBox.value()),
                                        gain=int(self.gainSpinBox.value()),
                                        ppm=int(self.ppmSpinBox.value()),
                                        crop=int(self.cropSpinBox.value()) / 100.0,
                                        single_shot=single_shot,
                                        sample_rate=settings.value("sample_rate", 2560000, int))
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
    def on_mainCurveCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.main_curve = checked
        if self.spectrumPlotWidget.curve.xData is None:
            self.spectrumPlotWidget.update_plot(self.data_storage)
        self.spectrumPlotWidget.curve.setVisible(checked)

    @QtCore.pyqtSlot(bool)
    def on_peakHoldMaxCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.peak_hold_max = checked
        if self.spectrumPlotWidget.curve_peak_hold_max.xData is None:
            self.spectrumPlotWidget.update_peak_hold_max(self.data_storage)
        self.spectrumPlotWidget.curve_peak_hold_max.setVisible(checked)

    @QtCore.pyqtSlot(bool)
    def on_peakHoldMinCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.peak_hold_min = checked
        if self.spectrumPlotWidget.curve_peak_hold_min.xData is None:
            self.spectrumPlotWidget.update_peak_hold_min(self.data_storage)
        self.spectrumPlotWidget.curve_peak_hold_min.setVisible(checked)

    @QtCore.pyqtSlot(bool)
    def on_averageCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.average = checked
        if self.spectrumPlotWidget.curve_average.xData is None:
            self.spectrumPlotWidget.update_average(self.data_storage)
        self.spectrumPlotWidget.curve_average.setVisible(checked)

    @QtCore.pyqtSlot(bool)
    def on_persistenceCheckBox_toggled(self, checked):
        self.spectrumPlotWidget.persistence = checked
        if self.spectrumPlotWidget.persistence_curves[0].xData is None:
            self.spectrumPlotWidget.recalculate_persistence(self.data_storage)
        for curve in self.spectrumPlotWidget.persistence_curves:
            curve.setVisible(checked)

    @QtCore.pyqtSlot(bool)
    def on_smoothCheckBox_toggled(self, checked):
        settings = QtCore.QSettings()
        self.data_storage.set_smooth(
            checked,
            settings.value("smooth_length", 11, int),
            settings.value("smooth_window", "hanning"),
            recalculate=True
        )

    @QtCore.pyqtSlot()
    def on_smoothButton_clicked(self):
        dialog = QSpectrumAnalyzerSmooth(self)
        if dialog.exec_():
            settings = QtCore.QSettings()
            self.data_storage.set_smooth(
                bool(self.smoothCheckBox.isChecked()),
                settings.value("smooth_length", 11, int),
                settings.value("smooth_window", "hanning"),
                recalculate=True
            )

    @QtCore.pyqtSlot()
    def on_persistenceButton_clicked(self):
        prev_persistence_length = self.spectrumPlotWidget.persistence_length
        dialog = QSpectrumAnalyzerPersistence(self)
        if dialog.exec_():
            settings = QtCore.QSettings()
            persistence_length = settings.value("persistence_length", 5, int)
            self.spectrumPlotWidget.persistence_length = persistence_length
            self.spectrumPlotWidget.persistence_decay = settings.value("persistence_decay", "exponential")

            # If only decay function has been changed, just reset colors
            if persistence_length == prev_persistence_length:
                self.spectrumPlotWidget.set_colors()
            else:
                self.spectrumPlotWidget.recalculate_persistence(self.data_storage)

    @QtCore.pyqtSlot()
    def on_colorsButton_clicked(self):
        dialog = QSpectrumAnalyzerColors(self)
        if dialog.exec_():
            settings = QtCore.QSettings()
            self.spectrumPlotWidget.main_color = str_to_color(settings.value("main_color", "255, 255, 0, 255"))
            self.spectrumPlotWidget.peak_hold_max_color = str_to_color(settings.value("peak_hold_max_color", "255, 0, 0, 255"))
            self.spectrumPlotWidget.peak_hold_min_color = str_to_color(settings.value("peak_hold_min_color", "0, 0, 255, 255"))
            self.spectrumPlotWidget.average_color = str_to_color(settings.value("average_color", "0, 255, 255, 255"))
            self.spectrumPlotWidget.persistence_color = str_to_color(settings.value("persistence_color", "0, 255, 0, 255"))
            self.spectrumPlotWidget.set_colors()

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
