# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_smoothing.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerSmoothing(object):
    def setupUi(self, QSpectrumAnalyzerSmoothing):
        QSpectrumAnalyzerSmoothing.setObjectName("QSpectrumAnalyzerSmoothing")
        QSpectrumAnalyzerSmoothing.resize(250, 130)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerSmoothing)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(QSpectrumAnalyzerSmoothing)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.windowFunctionComboBox = QtWidgets.QComboBox(QSpectrumAnalyzerSmoothing)
        self.windowFunctionComboBox.setObjectName("windowFunctionComboBox")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.windowFunctionComboBox)
        self.label_2 = QtWidgets.QLabel(QSpectrumAnalyzerSmoothing)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.windowLengthSpinBox = QtWidgets.QSpinBox(QSpectrumAnalyzerSmoothing)
        self.windowLengthSpinBox.setMinimum(3)
        self.windowLengthSpinBox.setMaximum(1001)
        self.windowLengthSpinBox.setProperty("value", 11)
        self.windowLengthSpinBox.setObjectName("windowLengthSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.windowLengthSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerSmoothing)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.windowFunctionComboBox)
        self.label_2.setBuddy(self.windowLengthSpinBox)

        self.retranslateUi(QSpectrumAnalyzerSmoothing)
        self.windowFunctionComboBox.setCurrentIndex(1)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerSmoothing.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerSmoothing.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSmoothing)
        QSpectrumAnalyzerSmoothing.setTabOrder(self.windowFunctionComboBox, self.windowLengthSpinBox)
        QSpectrumAnalyzerSmoothing.setTabOrder(self.windowLengthSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSmoothing):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerSmoothing.setWindowTitle(_translate("QSpectrumAnalyzerSmoothing", "Smoothing - QSpectrumAnalyzer"))
        self.label.setText(_translate("QSpectrumAnalyzerSmoothing", "&Window function:"))
        self.windowFunctionComboBox.setItemText(0, _translate("QSpectrumAnalyzerSmoothing", "rectangular"))
        self.windowFunctionComboBox.setItemText(1, _translate("QSpectrumAnalyzerSmoothing", "hanning"))
        self.windowFunctionComboBox.setItemText(2, _translate("QSpectrumAnalyzerSmoothing", "hamming"))
        self.windowFunctionComboBox.setItemText(3, _translate("QSpectrumAnalyzerSmoothing", "bartlett"))
        self.windowFunctionComboBox.setItemText(4, _translate("QSpectrumAnalyzerSmoothing", "blackman"))
        self.label_2.setText(_translate("QSpectrumAnalyzerSmoothing", "Window len&gth:"))

