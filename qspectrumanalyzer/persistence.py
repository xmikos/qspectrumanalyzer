from PyQt6 import QtCore, QtWidgets

from qspectrumanalyzer.ui_qspectrumanalyzer_persistence import Ui_QSpectrumAnalyzerPersistence


class QSpectrumAnalyzerPersistence(QtWidgets.QDialog, Ui_QSpectrumAnalyzerPersistence):
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
        QtWidgets.QDialog.accept(self)
