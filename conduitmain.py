import sys
import db_session
from PyQt5.QtWidgets import QApplication, QMainWindow
from cond_main_win import Ui_MainWindow
from tables import Students, Theories, Tasks, StudentsTasks, StudentsTheories
from heapq import merge


class ConduitMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.status = 'Tasks'
        self.loadtable()

    def loadtable(self):
        if self.status == 'Tasks':
            map(lambda x: print(x[0]), session.query(Tasks.task_id).all())
            self.tableWidget.setHorizontalHeaderLabels(['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(map(lambda x: str(x[0]), session.query(Tasks.task_id).all())))
            reader_one = session.query(Students).all()
            for i, row in enumerate(reader_one):
                self.tableWidget.setRowCount(i)
                reader_two = session.query(StudentsTasks.st_mark).filter_by(st_stu_id=row[0])
                for j, elem in enumerate(row + reader_two):
                    self.tableWidget.setItem(i, j, str(elem))
            self.tableWidget.resizeColumnsToContents()




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