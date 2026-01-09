from PyQt6 import QtCore, QtWidgets

from qspectrumanalyzer.ui_qspectrumanalyzer_baseline import Ui_QSpectrumAnalyzerBaseline


class QSpectrumAnalyzerBaseline(QtWidgets.QDialog, Ui_QSpectrumAnalyzerBaseline):
    """QSpectrumAnalyzer baseline dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        # Load settings
        settings = QtCore.QSettings()
        self.baselineFileEdit.setText(settings.value("baseline_file", ""))

    @QtCore.pyqtSlot()
    def on_baselineFileButton_clicked(self):
        """Open file dialog when button is clicked"""
        filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select baseline file - QSpectrumAnalyzer"))[0]
        if filename:
            self.baselineFileEdit.setText(filename)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("baseline_file", self.baselineFileEdit.text())
        QtWidgets.QDialog.accept(self)
