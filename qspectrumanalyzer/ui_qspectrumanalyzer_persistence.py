# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_persistence.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_QSpectrumAnalyzerPersistence(object):
    def setupUi(self, QSpectrumAnalyzerPersistence):
        QSpectrumAnalyzerPersistence.setObjectName(_fromUtf8("QSpectrumAnalyzerPersistence"))
        QSpectrumAnalyzerPersistence.resize(250, 130)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerPersistence)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(QSpectrumAnalyzerPersistence)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.decayFunctionComboBox = QtGui.QComboBox(QSpectrumAnalyzerPersistence)
        self.decayFunctionComboBox.setObjectName(_fromUtf8("decayFunctionComboBox"))
        self.decayFunctionComboBox.addItem(_fromUtf8(""))
        self.decayFunctionComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.decayFunctionComboBox)
        self.label = QtGui.QLabel(QSpectrumAnalyzerPersistence)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.persistenceLengthSpinBox = QtGui.QSpinBox(QSpectrumAnalyzerPersistence)
        self.persistenceLengthSpinBox.setProperty("value", 5)
        self.persistenceLengthSpinBox.setObjectName(_fromUtf8("persistenceLengthSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.persistenceLengthSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerPersistence)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.decayFunctionComboBox)
        self.label.setBuddy(self.persistenceLengthSpinBox)

        self.retranslateUi(QSpectrumAnalyzerPersistence)
        self.decayFunctionComboBox.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerPersistence.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerPersistence.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerPersistence)
        QSpectrumAnalyzerPersistence.setTabOrder(self.decayFunctionComboBox, self.persistenceLengthSpinBox)
        QSpectrumAnalyzerPersistence.setTabOrder(self.persistenceLengthSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerPersistence):
        QSpectrumAnalyzerPersistence.setWindowTitle(_translate("QSpectrumAnalyzerPersistence", "Persistence - QSpectrumAnalyzer", None))
        self.label_2.setText(_translate("QSpectrumAnalyzerPersistence", "Decay function:", None))
        self.decayFunctionComboBox.setItemText(0, _translate("QSpectrumAnalyzerPersistence", "linear", None))
        self.decayFunctionComboBox.setItemText(1, _translate("QSpectrumAnalyzerPersistence", "exponential", None))
        self.label.setText(_translate("QSpectrumAnalyzerPersistence", "Persistence length:", None))

