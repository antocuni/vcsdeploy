from threading import Thread
from PyQt4 import QtGui, QtCore
from vcsdeploy.Ui_MainWindow import Ui_MainWindow
from vcsdeploy.hg import MercurialLogic


class MainWindow(QtGui.QDialog, Ui_MainWindow):
    def __init__(self, config):
        QtGui.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.logic = MercurialLogic(config)
        self.setupUi(self)
        self.connect(self.btnUpdate, QtCore.SIGNAL("clicked()"), self.do_update)
        self.cmbUpdateTo.setEditable(config.editable_revision)
        self.lblCurrentRevision.setVisible(config.show_revision)
        self.lblCurrentRevisionValue.setVisible(config.show_revision)
        self.init()

    def init(self):
        self.pull_repo()
        self.sync_current_version()
        versions = self.logic.get_list_of_versions()            
        self.cmbUpdateTo.clear()
        self.cmbUpdateTo.addItems(versions)

    def sync_current_version(self):
        current_ver = self.logic.get_current_version()
        current_rev = self.logic.get_current_revision()
        if current_ver is None:
            current_ver = 'Unknown'
        self.lblCurrentVersion.setText(current_ver)
        self.lblCurrentRevisionValue.setText(current_rev)

    def pull_repo(self):
        import time
        app = QtCore.QCoreApplication.instance()
        bar = QtGui.QProgressDialog('Please wait', QtCore.QString(), 0, 0)
        bar.show()
        bar.setRange(0, 0)
        thread = Thread(target=self.logic.pull)
        thread.start()
        app.processEvents()
        while thread.is_alive():
            time.sleep(0.01)
            app.processEvents()

    def do_update(self):
        version = str(self.cmbUpdateTo.currentText())
        self.logic.update_to(version)
        self.sync_current_version()

