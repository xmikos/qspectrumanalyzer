from PyQt6 import QtCore, QtGui, QtWidgets

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
        backend = settings.value("backend", "soapy_power")
        self.deviceEdit.setText(settings.value("device", ""))
        self.lnbSpinBox.setValue(settings.value("lnb_lo", 0, float) / 1e6)
        self.waterfallHistorySizeSpinBox.setValue(settings.value("waterfall_history_size", 100, int))

        try:
            backend_module = getattr(backends, backend)
        except AttributeError:
            backend_module = backends.soapy_power

        # Params migration: move legacy shared params into backend-specific key
        params_key = f"params_{backend}"
        params = settings.value(params_key, None)
        if params is None:
            legacy_params = settings.value("params", None)
            params = legacy_params if legacy_params is not None else backend_module.Info.additional_params
            settings.setValue(params_key, params)
        self.paramsEdit.setText(params)

        # Executable migration: move legacy shared executable into backend-specific key
        exe_key = f"executable_{backend}"
        exe = settings.value(exe_key, None)
        if not exe:
            legacy_exe = settings.value("executable", None)
            exe = legacy_exe if legacy_exe is not None else backend
            settings.setValue(exe_key, exe)
        self.executableEdit.setText(exe)

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

    @QtCore.pyqtSlot()
    def on_executableButton_clicked(self):
        """Open file dialog when button is clicked"""
        filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select executable - QSpectrumAnalyzer"))[0]
        if filename:
            self.executableEdit.setText(filename)

    @QtCore.pyqtSlot()
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

    @QtCore.pyqtSlot()
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

    def _apply_backend_selection(self, backend_name):
        """Apply defaults and stored values for a selected backend in the settings dialog."""
        settings = QtCore.QSettings()
        exe_key = f"executable_{backend_name}"
        exe = settings.value(exe_key, None)
        # If there is no stored executable (or it still points to another backend), reset to backend name
        if not exe or (backend_name != "soapy_power" and exe == "soapy_power"):
            exe = backend_name
            settings.setValue(exe_key, exe)
        self.executableEdit.setText(exe)
        self.deviceEdit.setText("")

        try:
            backend_module = getattr(backends, backend_name)
        except AttributeError:
            backend_module = backends.soapy_power

        params_key = f"params_{backend_name}"
        params = settings.value(params_key, None)
        # Reset to backend defaults when there is nothing stored or when stale soapy defaults leak in
        if params is None or (backend_name != "soapy_power" and params.strip() == backends.soapy_power.Info.additional_params.strip()):
            params = backend_module.Info.additional_params
            settings.setValue(params_key, params)
        self.paramsEdit.setText(params)
        self.deviceHelpButton.setEnabled(bool(backend_module.Info.help_device))
        self.sampleRateSpinBox.setMinimum(backend_module.Info.sample_rate_min / 1e6)
        self.sampleRateSpinBox.setMaximum(backend_module.Info.sample_rate_max / 1e6)
        self.sampleRateSpinBox.setValue(backend_module.Info.sample_rate / 1e6)
        self.bandwidthSpinBox.setMinimum(backend_module.Info.bandwidth_min / 1e6)
        self.bandwidthSpinBox.setMaximum(backend_module.Info.bandwidth_max / 1e6)
        self.bandwidthSpinBox.setValue(backend_module.Info.bandwidth / 1e6)

    @QtCore.pyqtSlot(int)
    @QtCore.pyqtSlot(str)
    def on_backendComboBox_currentIndexChanged(self, value):
        """Change executable when backend is changed"""
        if isinstance(value, int):
            text = self.backendComboBox.itemText(value)
        else:
            text = value
        self._apply_backend_selection(text)

    def accept(self):
        """Save settings when dialog is accepted"""
        settings = QtCore.QSettings()
        backend = self.backendComboBox.currentText()
        settings.setValue("backend", backend)
        settings.setValue(f"executable_{backend}", self.executableEdit.text())
        params_key = f"params_{backend}"
        settings.setValue(params_key, self.paramsEdit.text())
        settings.setValue("device", self.deviceEdit.text())
        settings.setValue("sample_rate", self.sampleRateSpinBox.value() * 1e6)
        settings.setValue("bandwidth", self.bandwidthSpinBox.value() * 1e6)
        settings.setValue("lnb_lo", self.lnbSpinBox.value() * 1e6)
        settings.setValue("waterfall_history_size", self.waterfallHistorySizeSpinBox.value())
        settings.sync()
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
