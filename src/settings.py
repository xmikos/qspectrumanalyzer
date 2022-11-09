from Qt import QtCore, QtGui, QtWidgets

from qspectrumanalyzer import backends

from qspectrumanalyzer.ui_qspectrumanalyzer_settings import Ui_QSpectrumAnalyzerSettings
from qspectrumanalyzer.ui_qspectrumanalyzer_settings_help import Ui_QSpectrumAnalyzerSettingsHelp


class QSpectrumAnalyzerSettings(QtWidgets.QDialog, Ui_QSpectrumAnalyzerSettings):
    """QSpectrumAnalyzer settings dialog"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)
        self.params_help_dialog = None
        self.device_help_dialog = None

        # Load settings
        settings = QtCore.QSettings()
        self.executableEdit.setText(settings.value("executable", "soapy_power"))
        self.deviceEdit.setText(settings.value("device", ""))
        self.lnbSpinBox.setValue(settings.value("lnb_lo", 0, float) / 1e6)
        self.waterfallHistorySizeSpinBox.setValue(settings.value("waterfall_history_size", 100, int))

        backend = settings.value("backend", "soapy_power")
        try:
            backend_module = getattr(backends, backend)
        except AttributeError:
            backend_module = backends.soapy_power

        self.paramsEdit.setText(settings.value("params", backend_module.Info.additional_params))
        self.deviceHelpButton.setEnabled(bool(backend_module.Info.help_device))

        self.sampleRateSpinBox.setMinimum(backend_module.Info.sample_rate_min / 1e6)
        self.sampleRateSpinBox.setMaximum(backend_module.Info.sample_rate_max / 1e6)
        self.sampleRateSpinBox.setValue(settings.value("sample_rate", backend_module.Info.sample_rate, float) / 1e6)

        self.bandwidthSpinBox.setMinimum(backend_module.Info.bandwidth_min / 1e6)
        self.bandwidthSpinBox.setMaximum(backend_module.Info.bandwidth_max / 1e6)
        self.bandwidthSpinBox.setValue(settings.value("bandwidth", backend_module.Info.bandwidth, float) / 1e6)

        self.backendComboBox.blockSignals(True)
        self.backendComboBox.clear()
        for b in sorted(backends.__all__):
            self.backendComboBox.addItem(b)

        i = self.backendComboBox.findText(backend)
        if i == -1:
            self.backendComboBox.setCurrentIndex(0)
        else:
            self.backendComboBox.setCurrentIndex(i)
        self.backendComboBox.blockSignals(False)

    @QtCore.Slot()
    def on_executableButton_clicked(self):
        """Open file dialog when button is clicked"""
        filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select executable - QSpectrumAnalyzer"))[0]
        if filename:
            self.executableEdit.setText(filename)

    @QtCore.Slot()
    def on_paramsHelpButton_clicked(self):
        """Open additional parameters help dialog when button is clicked"""
        try:
            backend_module = getattr(backends, self.backendComboBox.currentText())
        except AttributeError:
            backend_module = backends.soapy_power

        self.params_help_dialog = QSpectrumAnalyzerSettingsHelp(
            backend_module.Info.help_params(self.executableEdit.text()),
            parent=self
        )

        self.params_help_dialog.show()
        self.params_help_dialog.raise_()
        self.params_help_dialog.activateWindow()

    @QtCore.Slot()
    def on_deviceHelpButton_clicked(self):
        """Open device help dialog when button is clicked"""
        try:
            backend_module = getattr(backends, self.backendComboBox.currentText())
        except AttributeError:
            backend_module = backends.soapy_power

        self.device_help_dialog = QSpectrumAnalyzerSettingsHelp(
            backend_module.Info.help_device(self.executableEdit.text(), self.deviceEdit.text()),
            parent=self
        )

        self.device_help_dialog.show()
        self.device_help_dialog.raise_()
        self.device_help_dialog.activateWindow()

    @QtCore.Slot(str)
    def on_backendComboBox_currentIndexChanged(self, text):
        """Change executable when backend is changed"""
        self.executableEdit.setText(text)
        self.deviceEdit.setText("")

        try:
            backend_module = getattr(backends, text)
        except AttributeError:
            backend_module = backends.soapy_power

        self.paramsEdit.setText(backend_module.Info.additional_params)
        self.deviceHelpButton.setEnabled(bool(backend_module.Info.help_device))
        self.sampleRateSpinBox.setMinimum(backend_module.Info.sample_rate_min / 1e6)
        self.sampleRateSpinBox.setMaximum(backend_module.Info.sample_rate_max / 1e6)
        self.sampleRateSpinBox.setValue(backend_module.Info.sample_rate / 1e6)
        self.bandwidthSpinBox.setMinimum(backend_module.Info.bandwidth_min / 1e6)
        self.bandwidthSpinBox.setMaximum(backend_module.Info.bandwidth_max / 1e6)
        self.bandwidthSpinBox.setValue(backend_module.Info.bandwidth / 1e6)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        settings.setValue("backend", self.backendComboBox.currentText())
        settings.setValue("executable", self.executableEdit.text())
        settings.setValue("params", self.paramsEdit.text())
        settings.setValue("device", self.deviceEdit.text())
        settings.setValue("sample_rate", self.sampleRateSpinBox.value() * 1e6)
        settings.setValue("bandwidth", self.bandwidthSpinBox.value() * 1e6)
        settings.setValue("lnb_lo", self.lnbSpinBox.value() * 1e6)
        settings.setValue("waterfall_history_size", self.waterfallHistorySizeSpinBox.value())
        QtWidgets.QDialog.accept(self)


class QSpectrumAnalyzerSettingsHelp(QtWidgets.QDialog, Ui_QSpectrumAnalyzerSettingsHelp):
    """QSpectrumAnalyzer settings help dialog"""
    def __init__(self, text, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

        monospace_font = QtGui.QFont('monospace')
        monospace_font.setStyleHint(QtGui.QFont.Monospace)
        self.helpTextEdit.setFont(monospace_font)
        self.helpTextEdit.setPlainText(text)
