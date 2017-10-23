# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_average.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerAverage(object):
    def setupUi(self, QSpectrumAnalyzerAverage):
        QSpectrumAnalyzerAverage.setObjectName("QSpectrumAnalyzerAverage")
        QSpectrumAnalyzerAverage.resize(530, 130)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerAverage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(QSpectrumAnalyzerAverage)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.averageSamplesSpinBox = QtWidgets.QSpinBox(QSpectrumAnalyzerAverage)
        self.averageSamplesSpinBox.setMinimum(0)
        self.averageSamplesSpinBox.setMaximum(5000)
        self.averageSamplesSpinBox.setProperty("value", 0)
        self.averageSamplesSpinBox.setObjectName("averageSamplesSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.averageSamplesSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerAverage)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.averageSamplesSpinBox)

        self.retranslateUi(QSpectrumAnalyzerAverage)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerAverage.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerAverage.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerAverage)
        QSpectrumAnalyzerAverage.setTabOrder(self.averageSamplesSpinBox, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerAverage):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerAverage.setWindowTitle(_translate("QSpectrumAnalyzerAverage", "Average - QSpectrumAnalyzer"))
        self.label.setText(_translate("QSpectrumAnalyzerAverage", "Number of samples:"))

