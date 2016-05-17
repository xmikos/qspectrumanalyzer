# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qspectrumanalyzer/qspectrumanalyzer_colors.ui'
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

class Ui_QSpectrumAnalyzerColors(object):
    def setupUi(self, QSpectrumAnalyzerColors):
        QSpectrumAnalyzerColors.setObjectName(_fromUtf8("QSpectrumAnalyzerColors"))
        QSpectrumAnalyzerColors.resize(232, 260)
        self.verticalLayout = QtGui.QVBoxLayout(QSpectrumAnalyzerColors)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(QSpectrumAnalyzerColors)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.mainColorButton = ColorButton(QSpectrumAnalyzerColors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainColorButton.sizePolicy().hasHeightForWidth())
        self.mainColorButton.setSizePolicy(sizePolicy)
        self.mainColorButton.setObjectName(_fromUtf8("mainColorButton"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.mainColorButton)
        self.label_4 = QtGui.QLabel(QSpectrumAnalyzerColors)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.peakHoldMaxColorButton = ColorButton(QSpectrumAnalyzerColors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peakHoldMaxColorButton.sizePolicy().hasHeightForWidth())
        self.peakHoldMaxColorButton.setSizePolicy(sizePolicy)
        self.peakHoldMaxColorButton.setObjectName(_fromUtf8("peakHoldMaxColorButton"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.peakHoldMaxColorButton)
        self.label_6 = QtGui.QLabel(QSpectrumAnalyzerColors)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.peakHoldMinColorButton = ColorButton(QSpectrumAnalyzerColors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peakHoldMinColorButton.sizePolicy().hasHeightForWidth())
        self.peakHoldMinColorButton.setSizePolicy(sizePolicy)
        self.peakHoldMinColorButton.setObjectName(_fromUtf8("peakHoldMinColorButton"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.peakHoldMinColorButton)
        self.label_5 = QtGui.QLabel(QSpectrumAnalyzerColors)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.averageColorButton = ColorButton(QSpectrumAnalyzerColors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.averageColorButton.sizePolicy().hasHeightForWidth())
        self.averageColorButton.setSizePolicy(sizePolicy)
        self.averageColorButton.setObjectName(_fromUtf8("averageColorButton"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.averageColorButton)
        self.label_3 = QtGui.QLabel(QSpectrumAnalyzerColors)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.persistenceColorButton = ColorButton(QSpectrumAnalyzerColors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.persistenceColorButton.sizePolicy().hasHeightForWidth())
        self.persistenceColorButton.setSizePolicy(sizePolicy)
        self.persistenceColorButton.setObjectName(_fromUtf8("persistenceColorButton"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.persistenceColorButton)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(QSpectrumAnalyzerColors)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.mainColorButton)
        self.label_4.setBuddy(self.peakHoldMaxColorButton)
        self.label_6.setBuddy(self.peakHoldMinColorButton)
        self.label_5.setBuddy(self.averageColorButton)
        self.label_3.setBuddy(self.persistenceColorButton)

        self.retranslateUi(QSpectrumAnalyzerColors)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QSpectrumAnalyzerColors.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QSpectrumAnalyzerColors.reject)
        QtCore.QMetaObject.connectSlotsByName(QSpectrumAnalyzerColors)
        QSpectrumAnalyzerColors.setTabOrder(self.mainColorButton, self.peakHoldMaxColorButton)
        QSpectrumAnalyzerColors.setTabOrder(self.peakHoldMaxColorButton, self.peakHoldMinColorButton)
        QSpectrumAnalyzerColors.setTabOrder(self.peakHoldMinColorButton, self.averageColorButton)
        QSpectrumAnalyzerColors.setTabOrder(self.averageColorButton, self.persistenceColorButton)
        QSpectrumAnalyzerColors.setTabOrder(self.persistenceColorButton, self.buttonBox)

    def retranslateUi(self, QSpectrumAnalyzerColors):
        QSpectrumAnalyzerColors.setWindowTitle(_translate("QSpectrumAnalyzerColors", "Colors - QSpectrumAnalyzer", None))
        self.label_2.setText(_translate("QSpectrumAnalyzerColors", "Main curve color:", None))
        self.mainColorButton.setText(_translate("QSpectrumAnalyzerColors", "...", None))
        self.label_4.setText(_translate("QSpectrumAnalyzerColors", "Max. peak hold color:", None))
        self.peakHoldMaxColorButton.setText(_translate("QSpectrumAnalyzerColors", "...", None))
        self.label_6.setText(_translate("QSpectrumAnalyzerColors", "Min. peak hold color:", None))
        self.peakHoldMinColorButton.setText(_translate("QSpectrumAnalyzerColors", "...", None))
        self.label_5.setText(_translate("QSpectrumAnalyzerColors", "Average color:", None))
        self.averageColorButton.setText(_translate("QSpectrumAnalyzerColors", "...", None))
        self.label_3.setText(_translate("QSpectrumAnalyzerColors", "Persistence color:", None))
        self.persistenceColorButton.setText(_translate("QSpectrumAnalyzerColors", "...", None))

from pyqtgraph import ColorButton
