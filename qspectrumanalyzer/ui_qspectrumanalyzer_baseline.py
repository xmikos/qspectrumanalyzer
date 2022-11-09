# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_baseline.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_QSpectrumAnalyzerBaseline(object):
    def setupUi(self, QSpectrumAnalyzerBaseline):
        QSpectrumAnalyzerBaseline.setObjectName("QSpectrumAnalyzerBaseline")
        QSpectrumAnalyzerBaseline.resize(500, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpectrumAnalyzerBaseline)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(QSpectrumAnalyzerBaseline)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.baselineFileEdit = QtWidgets.QLineEdit(QSpectrumAnalyzerBaseline)
        self.baselineFileEdit.setObjectName("baselineFileEdit")
        self.horizontalLayout.addWidget(self.baselineFileEdit)
        self.baselineFileButton = QtWidgets.QToolButton(QSpectrumAnalyzerBaseline)
        self.baselineFileButton.setMinimumSize(QtCore.QSize(50, 0))
        self.baselineFileButton.setObjectName("baselineFileButton")
        self.horizontalLayout.addWidget(self.baselineFileButton)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(QSpectrumAnalyzerBaseline)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.baselineFileEdit)

        self.retranslateUi(QSpectrumAnalyzerBaseline)
        self.buttonBox.accepted.connect(QSpectrumAnalyzerBaseline.accept)
        self.buttonBox.rejected.connect(QSpectrumAnalyzerBaseline.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerBaseline)
        QSpectrumAnalyzerBaseline.setTabOrder(self.baselineFileEdit, self.baselineFileButton)

    def retranslateUi(self, QSpectrumAnalyzerBaseline):
        _translate = QtCore.QCoreApplication.translate
        QSpectrumAnalyzerBaseline.setWindowTitle(_translate("QSpectrumAnalyzerBaseline", "Baseline - QSpectrumAnalyzer"))
        self.label.setText(_translate("QSpectrumAnalyzerBaseline", "Baseline &file:"))
        self.baselineFileButton.setText(_translate("QSpectrumAnalyzerBaseline", "..."))

