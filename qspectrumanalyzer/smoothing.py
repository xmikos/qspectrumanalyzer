from PyQt6 import QtCore, QtWidgets

from qspectrumanalyzer.ui_qspectrumanalyzer_smoothing import Ui_QSpectrumAnalyzerSmoothing


class QSpectrumAnalyzerSmoothing(QtWidgets.QDialog, Ui_QSpectrumAnalyzerSmoothing):
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
        QtWidgets.QDialog.accept(self)
