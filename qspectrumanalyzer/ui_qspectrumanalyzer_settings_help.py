# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_settings_help.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerSettingsHelp(object):
    def setupUi(self, QSpectrumAnalyzerSettingsHelp):
        QSpectrumAnalyzerSettingsHelp.setObjectName("QSpectrumAnalyzerSettingsHelp")
        QSpectrumAnalyzerSettingsHelp.resize(1200, 700)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerSettingsHelp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.helpTextEdit = QtWidgets.QPlainTextEdit(QSpectrumAnalyzerSettingsHelp)
        self.helpTextEdit.setUndoRedoEnabled(False)
        self.helpTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.helpTextEdit.setObjectName("helpTextEdit")
        self.verticalLayout.addWidget(self.helpTextEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerSettingsHelp)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QSpectrumAnalyzerSettingsHelp)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerSettingsHelp.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerSettingsHelp.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSettingsHelp)
        QSpectrumAnalyzerSettingsHelp.setTabOrder(self.helpTextEdit, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSettingsHelp):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerSettingsHelp.setWindowTitle(_translate("QSpectrumAnalyzerSettingsHelp", "Help - QSpectrumAnalyzer"))

