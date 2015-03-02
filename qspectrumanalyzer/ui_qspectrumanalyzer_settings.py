# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_settings.ui'
#
# Created: Mon Mar  2 23:12:42 2015
#      by: PyQt4 UI code generator 4.11.3
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
        QSpectrumAnalyzerSettings.resize(500, 150)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerSettings)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rtlPowerExecutableEdit = QtGui.QLineEdit(QSpectrumAnalyzerSettings)
        self.rtlPowerExecutableEdit.setObjectName(_fromUtf8("rtlPowerExecutableEdit"))
        self.horizontalLayout.addWidget(self.rtlPowerExecutableEdit)
        self.rtlPowerExecutableButton = QtGui.QToolButton(QSpectrumAnalyzerSettings)
        self.rtlPowerExecutableButton.setObjectName(_fromUtf8("rtlPowerExecutableButton"))
        self.horizontalLayout.addWidget(self.rtlPowerExecutableButton)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(QSpectrumAnalyzerSettings)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.waterfallHistorySizeSpinBox = QtGui.QSpinBox(QSpectrumAnalyzerSettings)
        self.waterfallHistorySizeSpinBox.setMinimum(1)
        self.waterfallHistorySizeSpinBox.setMaximum(10000000)
        self.waterfallHistorySizeSpinBox.setProperty("value", 100)
        self.waterfallHistorySizeSpinBox.setObjectName(_fromUtf8("waterfallHistorySizeSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.waterfallHistorySizeSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QSpectrumAnalyzerSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSettings)
        QSpectrumAnalyzerSettings.setTabOrder(self.rtlPowerExecutableEdit, self.rtlPowerExecutableButton)
        QSpectrumAnalyzerSettings.setTabOrder(self.rtlPowerExecutableButton, self.waterfallHistorySizeSpinBox)
        QSpectrumAnalyzerSettings.setTabOrder(self.waterfallHistorySizeSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSettings):
        QSpectrumAnalyzerSettings.setWindowTitle(_translate("QSpectrumAnalyzerSettings", "QSpectrumAnalyzer - Settings", None))
        self.label.setText(_translate("QSpectrumAnalyzerSettings", "Rtl_power executable:", None))
        self.rtlPowerExecutableEdit.setText(_translate("QSpectrumAnalyzerSettings", "rtl_power", None))
        self.rtlPowerExecutableButton.setText(_translate("QSpectrumAnalyzerSettings", "...", None))
        self.label_2.setText(_translate("QSpectrumAnalyzerSettings", "Waterfall history size:", None))

