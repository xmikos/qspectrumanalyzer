# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_settings_help.ui'
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

class Ui_QSpectrumAnalyzerSettingsHelp(object):
    def setupUi(self, QSpectrumAnalyzerSettingsHelp):
        QSpectrumAnalyzerSettingsHelp.setObjectName(_fromUtf8("QSpectrumAnalyzerSettingsHelp"))
        QSpectrumAnalyzerSettingsHelp.resize(1200, 700)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerSettingsHelp)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.helpTextEdit = QtGui.QPlainTextEdit(QSpectrumAnalyzerSettingsHelp)
        self.helpTextEdit.setUndoRedoEnabled(False)
        self.helpTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.helpTextEdit.setObjectName(_fromUtf8("helpTextEdit"))
        self.verticalLayout.addWidget(self.helpTextEdit)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerSettingsHelp)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QSpectrumAnalyzerSettingsHelp)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerSettingsHelp.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerSettingsHelp.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSettingsHelp)
        QSpectrumAnalyzerSettingsHelp.setTabOrder(self.helpTextEdit, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSettingsHelp):
        QSpectrumAnalyzerSettingsHelp.setWindowTitle(_translate("QSpectrumAnalyzerSettingsHelp", "Help - QSpectrumAnalyzer", None))

