# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_persistence.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerPersistence(object):
    def setupUi(self, QSpectrumAnalyzerPersistence):
        QSpectrumAnalyzerPersistence.setObjectName("QSpectrumAnalyzerPersistence")
        QSpectrumAnalyzerPersistence.resize(250, 130)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerPersistence)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(QSpectrumAnalyzerPersistence)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.decayFunctionComboBox = QtWidgets.QComboBox(QSpectrumAnalyzerPersistence)
        self.decayFunctionComboBox.setObjectName("decayFunctionComboBox")
        self.decayFunctionComboBox.addItem("")
        self.decayFunctionComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.decayFunctionComboBox)
        self.label = QtWidgets.QLabel(QSpectrumAnalyzerPersistence)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.persistenceLengthSpinBox = QtWidgets.QSpinBox(QSpectrumAnalyzerPersistence)
        self.persistenceLengthSpinBox.setProperty("value", 5)
        self.persistenceLengthSpinBox.setObjectName("persistenceLengthSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.persistenceLengthSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerPersistence)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.decayFunctionComboBox)
        self.label.setBuddy(self.persistenceLengthSpinBox)

        self.retranslateUi(QSpectrumAnalyzerPersistence)
        self.decayFunctionComboBox.setCurrentIndex(1)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerPersistence.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerPersistence.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerPersistence)
        QSpectrumAnalyzerPersistence.setTabOrder(self.decayFunctionComboBox, self.persistenceLengthSpinBox)
        QSpectrumAnalyzerPersistence.setTabOrder(self.persistenceLengthSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerPersistence):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerPersistence.setWindowTitle(_translate("QSpectrumAnalyzerPersistence", "Persistence - QSpectrumAnalyzer"))
        self.label_2.setText(_translate("QSpectrumAnalyzerPersistence", "Decay function:"))
        self.decayFunctionComboBox.setItemText(0, _translate("QSpectrumAnalyzerPersistence", "linear"))
        self.decayFunctionComboBox.setItemText(1, _translate("QSpectrumAnalyzerPersistence", "exponential"))
        self.label.setText(_translate("QSpectrumAnalyzerPersistence", "Persistence length:"))

