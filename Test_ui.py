# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton_getFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_getFile.setGeometry(QtCore.QRect(120, 90, 75, 23))
        self.pushButton_getFile.setObjectName("pushButton_getFile")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_getFile.setText(_translate("Dialog", "Get File"))

