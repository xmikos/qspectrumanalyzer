from PyQt6 import QtCore, QtWidgets

from qspectrumanalyzer.utils import color_to_str, str_to_color

from qspectrumanalyzer.ui_qspectrumanalyzer_colors import Ui_QSpectrumAnalyzerColors


class QSpectrumAnalyzerColors(QtWidgets.QDialog, Ui_QSpectrumAnalyzerColors):
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
        self.baselineColorButton.setColor(str_to_color(settings.value("baseline_color", "255, 0, 255, 255")))

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("main_color", color_to_str(self.mainColorButton.color()))
        settings.setValue("peak_hold_max_color", color_to_str(self.peakHoldMaxColorButton.color()))
        settings.setValue("peak_hold_min_color", color_to_str(self.peakHoldMinColorButton.color()))
        settings.setValue("average_color", color_to_str(self.averageColorButton.color()))
        settings.setValue("persistence_color", color_to_str(self.persistenceColorButton.color()))
        settings.setValue("baseline_color", color_to_str(self.baselineColorButton.color()))
        QtWidgets.QDialog.accept(self)
