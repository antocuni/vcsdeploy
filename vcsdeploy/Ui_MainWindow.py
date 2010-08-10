# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/antocuni/pypy/misc/vcsdeploy/vcsdeploy/MainWindow.ui'
#
# Created: Tue Aug 10 16:23:54 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(274, 109)
        self.gridLayout = QtGui.QGridLayout(MainWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(MainWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblCurrentVersion = QtGui.QLabel(MainWindow)
        self.lblCurrentVersion.setObjectName("lblCurrentVersion")
        self.gridLayout.addWidget(self.lblCurrentVersion, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(MainWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cmbUpdateTo = QtGui.QComboBox(MainWindow)
        self.cmbUpdateTo.setFrame(True)
        self.cmbUpdateTo.setObjectName("cmbUpdateTo")
        self.gridLayout.addWidget(self.cmbUpdateTo, 1, 1, 1, 1)
        self.btnUpdate = QtGui.QPushButton(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUpdate.setIcon(icon)
        self.btnUpdate.setObjectName("btnUpdate")
        self.gridLayout.addWidget(self.btnUpdate, 2, 1, 1, 1)
        self.btnQuit = QtGui.QPushButton(MainWindow)
        self.btnQuit.setObjectName("btnQuit")
        self.gridLayout.addWidget(self.btnQuit, 3, 1, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL("clicked()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Update Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Current Version", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCurrentVersion.setText(QtGui.QApplication.translate("MainWindow", "Version ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Update to", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.btnQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

import vcsdeploy_rc
