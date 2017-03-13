# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_smooth.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerSmooth(object):
    def setupUi(self, QSpectrumAnalyzerSmooth):
        QSpectrumAnalyzerSmooth.setObjectName("QSpectrumAnalyzerSmooth")
        QSpectrumAnalyzerSmooth.resize(250, 130)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerSmooth)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(QSpectrumAnalyzerSmooth)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.windowFunctionComboBox = QtWidgets.QComboBox(QSpectrumAnalyzerSmooth)
        self.windowFunctionComboBox.setObjectName("windowFunctionComboBox")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.windowFunctionComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.windowFunctionComboBox)
        self.label_2 = QtWidgets.QLabel(QSpectrumAnalyzerSmooth)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.windowLengthSpinBox = QtWidgets.QSpinBox(QSpectrumAnalyzerSmooth)
        self.windowLengthSpinBox.setMinimum(3)
        self.windowLengthSpinBox.setMaximum(1001)
        self.windowLengthSpinBox.setProperty("value", 11)
        self.windowLengthSpinBox.setObjectName("windowLengthSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.windowLengthSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerSmooth)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.windowFunctionComboBox)
        self.label_2.setBuddy(self.windowLengthSpinBox)

        self.retranslateUi(QSpectrumAnalyzerSmooth)
        self.windowFunctionComboBox.setCurrentIndex(1)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerSmooth.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerSmooth.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerSmooth)
        QSpectrumAnalyzerSmooth.setTabOrder(self.windowFunctionComboBox, self.windowLengthSpinBox)
        QSpectrumAnalyzerSmooth.setTabOrder(self.windowLengthSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerSmooth):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerSmooth.setWindowTitle(_translate("QSpectrumAnalyzerSmooth", "Smoothing - QSpectrumAnalyzer"))
        self.label.setText(_translate("QSpectrumAnalyzerSmooth", "&Window function:"))
        self.windowFunctionComboBox.setItemText(0, _translate("QSpectrumAnalyzerSmooth", "rectangular"))
        self.windowFunctionComboBox.setItemText(1, _translate("QSpectrumAnalyzerSmooth", "hanning"))
        self.windowFunctionComboBox.setItemText(2, _translate("QSpectrumAnalyzerSmooth", "hamming"))
        self.windowFunctionComboBox.setItemText(3, _translate("QSpectrumAnalyzerSmooth", "bartlett"))
        self.windowFunctionComboBox.setItemText(4, _translate("QSpectrumAnalyzerSmooth", "blackman"))
        self.label_2.setText(_translate("QSpectrumAnalyzerSmooth", "Window len&gth:"))

