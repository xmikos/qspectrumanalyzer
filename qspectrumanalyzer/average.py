from Qt import QtCore, QtWidgets

from qspectrumanalyzer.ui_qspectrumanalyzer_average import Ui_QSpectrumAnalyzerAverage


class QSpectrumAnalyzerAverage(QtWidgets.QDialog, Ui_QSpectrumAnalyzerAverage):
    """QSpectrumAnalyzer spectrum smoothing dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.averageSamplesSpinBox.setValue(settings.value("average_samples", 0, int))

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("average_samples", self.averageSamplesSpinBox.value())
        QtWidgets.QDialog.accept(self)
