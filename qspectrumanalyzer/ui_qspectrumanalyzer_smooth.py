# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_smooth.ui'
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

class Ui_QSpectrumAnalyzerSmooth(object):
    def setupUi(self, QSpectrumAnalyzerSmooth):
        QSpectrumAnalyzerSmooth.setObjectName(_fromUtf8("QSpectrumAnalyzerSmooth"))
        QSpectrumAnalyzerSmooth.resize(250, 130)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerSmooth)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(QSpectrumAnalyzerSmooth)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.windowFunctionComboBox = QtGui.QComboBox(QSpectrumAnalyzerSmooth)
        self.windowFunctionComboBox.setObjectName(_fromUtf8("windowFunctionComboBox"))
        self.windowFunctionComboBox.addItem(_fromUtf8(""))
        self.windowFunctionComboBox.addItem(_fromUtf8(""))
        self.windowFunctionComboBox.addItem(_fromUtf8(""))
        self.windowFunctionComboBox.addItem(_fromUtf8(""))
        self.windowFunctionComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.windowFunctionComboBox)
        self.label_2 = QtGui.QLabel(QSpectrumAnalyzerSmooth)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.windowLengthSpinBox = QtGui.QSpinBox(QSpectrumAnalyzerSmooth)
        self.windowLengthSpinBox.setMinimum(3)
        self.windowLengthSpinBox.setMaximum(1001)
        self.windowLengthSpinBox.setProperty("value", 11)
        self.windowLengthSpinBox.setObjectName(_fromUtf8("windowLengthSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.windowLengthSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerSmooth)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.windowFunctionComboBox)
        self.label_2.setBuddy(self.windowLengthSpinBox)

        self.retranslateUi(QSpectrumAnalyzerSmooth)
        self.windowFunctionComboBox.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerSmooth.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerSmooth.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSmooth)
        QSpectrumAnalyzerSmooth.setTabOrder(self.windowFunctionComboBox, self.windowLengthSpinBox)
        QSpectrumAnalyzerSmooth.setTabOrder(self.windowLengthSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSmooth):
        QSpectrumAnalyzerSmooth.setWindowTitle(_translate("QSpectrumAnalyzerSmooth", "Smoothing - QSpectrumAnalyzer", None))
        self.label.setText(_translate("QSpectrumAnalyzerSmooth", "&Window function:", None))
        self.windowFunctionComboBox.setItemText(0, _translate("QSpectrumAnalyzerSmooth", "rectangular", None))
        self.windowFunctionComboBox.setItemText(1, _translate("QSpectrumAnalyzerSmooth", "hanning", None))
        self.windowFunctionComboBox.setItemText(2, _translate("QSpectrumAnalyzerSmooth", "hamming", None))
        self.windowFunctionComboBox.setItemText(3, _translate("QSpectrumAnalyzerSmooth", "bartlett", None))
        self.windowFunctionComboBox.setItemText(4, _translate("QSpectrumAnalyzerSmooth", "blackman", None))
        self.label_2.setText(_translate("QSpectrumAnalyzerSmooth", "Window len&gth:", None))

