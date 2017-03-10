# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_settings.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QSpectrumAnalyzerSettings(object):
    def setupUi(self, QSpectrumAnalyzerSettings):
        QSpectrumAnalyzerSettings.setObjectName(_fromUtf8("QSpectrumAnalyzerSettings"))
        QSpectrumAnalyzerSettings.resize(600, 310)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerSettings)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.backendComboBox = QtGui.QComboBox(QSpectrumAnalyzerSettings)
        self.backendComboBox.setObjectName(_fromUtf8("backendComboBox"))
        self.backendComboBox.addItem(_fromUtf8(""))
        self.backendComboBox.addItem(_fromUtf8(""))
        self.backendComboBox.addItem(_fromUtf8(""))
        self.backendComboBox.addItem(_fromUtf8(""))
        self.backendComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.backendComboBox)
        self.label = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.executableEdit = QtGui.QLineEdit(QSpectrumAnalyzerSettings)
        self.executableEdit.setObjectName(_fromUtf8("executableEdit"))
        self.horizontalLayout.addWidget(self.executableEdit)
        self.executableButton = QtGui.QToolButton(QSpectrumAnalyzerSettings)
        self.executableButton.setObjectName(_fromUtf8("executableButton"))
        self.horizontalLayout.addWidget(self.executableButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_5 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.deviceEdit = QtGui.QLineEdit(QSpectrumAnalyzerSettings)
        self.deviceEdit.setObjectName(_fromUtf8("deviceEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.deviceEdit)
        self.label_4 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.sampleRateSpinBox = QtGui.QSpinBox(QSpectrumAnalyzerSettings)
        self.sampleRateSpinBox.setMinimum(0)
        self.sampleRateSpinBox.setMaximum(25000000)
        self.sampleRateSpinBox.setSingleStep(10000)
        self.sampleRateSpinBox.setProperty("value", 2560000)
        self.sampleRateSpinBox.setObjectName(_fromUtf8("sampleRateSpinBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.sampleRateSpinBox)
        self.label_2 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.waterfallHistorySizeSpinBox = QtGui.QSpinBox(QSpectrumAnalyzerSettings)
        self.waterfallHistorySizeSpinBox.setMinimum(1)
        self.waterfallHistorySizeSpinBox.setMaximum(10000000)
        self.waterfallHistorySizeSpinBox.setProperty("value", 100)
        self.waterfallHistorySizeSpinBox.setObjectName(_fromUtf8("waterfallHistorySizeSpinBox"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.waterfallHistorySizeSpinBox)
        self.label_6 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.paramsEdit = QtGui.QLineEdit(QSpectrumAnalyzerSettings)
        self.paramsEdit.setObjectName(_fromUtf8("paramsEdit"))
        self.horizontalLayout_3.addWidget(self.paramsEdit)
        self.helpButton = QtGui.QToolButton(QSpectrumAnalyzerSettings)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout_3.addWidget(self.helpButton)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.backendComboBox)
        self.label.setBuddy(self.executableEdit)
        self.label_5.setBuddy(self.deviceEdit)
        self.label_4.setBuddy(self.sampleRateSpinBox)
        self.label_2.setBuddy(self.waterfallHistorySizeSpinBox)
        self.label_6.setBuddy(self.paramsEdit)

        self.retranslateUi(QSpectrumAnalyzerSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSettings)
        QSpectrumAnalyzerSettings.setTabOrder(self.backendComboBox, self.executableEdit)
        QSpectrumAnalyzerSettings.setTabOrder(self.executableEdit, self.executableButton)
        QSpectrumAnalyzerSettings.setTabOrder(self.executableButton, self.deviceEdit)
        QSpectrumAnalyzerSettings.setTabOrder(self.deviceEdit, self.paramsEdit)
        QSpectrumAnalyzerSettings.setTabOrder(self.paramsEdit, self.helpButton)
        QSpectrumAnalyzerSettings.setTabOrder(self.helpButton, self.sampleRateSpinBox)
        QSpectrumAnalyzerSettings.setTabOrder(self.sampleRateSpinBox, self.waterfallHistorySizeSpinBox)
        QSpectrumAnalyzerSettings.setTabOrder(self.waterfallHistorySizeSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSettings):
        QSpectrumAnalyzerSettings.setWindowTitle(_translate("QSpectrumAnalyzerSettings", "Settings - QSpectrumAnalyzer", None))
        self.label_3.setText(_translate("QSpectrumAnalyzerSettings", "&Backend:", None))
        self.backendComboBox.setItemText(0, _translate("QSpectrumAnalyzerSettings", "soapy_power", None))
        self.backendComboBox.setItemText(1, _translate("QSpectrumAnalyzerSettings", "rx_power", None))
        self.backendComboBox.setItemText(2, _translate("QSpectrumAnalyzerSettings", "rtl_power_fftw", None))
        self.backendComboBox.setItemText(3, _translate("QSpectrumAnalyzerSettings", "rtl_power", None))
        self.backendComboBox.setItemText(4, _translate("QSpectrumAnalyzerSettings", "hackrf_sweep", None))
        self.label.setText(_translate("QSpectrumAnalyzerSettings", "E&xecutable:", None))
        self.executableEdit.setText(_translate("QSpectrumAnalyzerSettings", "soapy_power", None))
        self.executableButton.setText(_translate("QSpectrumAnalyzerSettings", "...", None))
        self.label_5.setText(_translate("QSpectrumAnalyzerSettings", "&Device:", None))
        self.label_4.setText(_translate("QSpectrumAnalyzerSettings", "Sa&mple rate:", None))
        self.label_2.setText(_translate("QSpectrumAnalyzerSettings", "&Waterfall history size:", None))
        self.label_6.setText(_translate("QSpectrumAnalyzerSettings", "Additional &parameters:", None))
        self.helpButton.setText(_translate("QSpectrumAnalyzerSettings", "?", None))

