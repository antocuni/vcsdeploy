from PyQt4 import QtGui, QtCore
from Ui_MainWindow import Ui_MainWindow

class MainWindow(QtGui.QDialog, Ui_MainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connect(self.btnUpdate, QtCore.SIGNAL("clicked()"), self.message)

    def message(self):
        print "Hello, world!"
