# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'theorywin.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 380)
        self.lineEditId = QtWidgets.QLineEdit(Dialog)
        self.lineEditId.setGeometry(QtCore.QRect(10, 10, 113, 20))
        self.lineEditId.setObjectName("lineEditId")
        self.lineEditTheme = QtWidgets.QLineEdit(Dialog)
        self.lineEditTheme.setGeometry(QtCore.QRect(10, 40, 380, 31))
        self.lineEditTheme.setObjectName("lineEditTheme")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 380, 261))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(320, 350, 70, 23))
        self.pushButtonSave.setObjectName("pushButtonSave")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonSave.setText(_translate("Dialog", "Save"))