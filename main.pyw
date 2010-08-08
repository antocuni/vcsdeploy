#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

import makefile
from MainWindow import MainWindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
