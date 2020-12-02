import sys
import db_session
from PyQt5.QtWidgets import QApplication, QMainWindow
from cond_main_win import Ui_MainWindow


class ConduitMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadtable()

    def loadtable(self):
        if self.status == 'Tasks':



def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys._excepthook = sys.excepthook

sys.excepthook = exception_hook

db_session.global_init('marks.db')
session = db_session.create_session()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConduitMain()
    ex.show()
    sys.exit(app.exec_())