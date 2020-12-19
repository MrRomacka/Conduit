import sys
import db_session
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from cond_main_win import Ui_MainWindow
from cond_task_win import Ui_Dialog
#from tables import Students, Theories, Tasks, StudentsTasks, StudentsTheories
from heapq import merge
import sqlite3

class Tasky(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonSave.clicked.connect(self.__save_task)

    def __save_task(self):
        t_id = self.lineEditId.text()
        t_num = self.lineEditNumber.text()
        t_theme = self.lineEditTheme.text()
        t_equa = self.textEdit.toPlainText()
        t_date = self.lineEditDate.text()
        db_connection = sqlite3.connect('marks.db')
        cur = db_connection.cursor()
        cur.execute(f'UPDATE Task '
                    f'SET task_id={int(t_id)}, task_number="{t_num}", task_theme="{t_theme}", task_equation="{t_equa}", '
                    f'task_date="{t_date}" WHERE task_id={int(t_id)}')
        db_connection.commit()
        db_connection.close()
        self.close()


class ConduitMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.status = 'Tasks'
        self.code = 'Nothing'
        self.loadtable()
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.header_clicked)
        self.db_connection = sqlite3.connect('marks.db')
        self.cur = self.db_connection.cursor()
        self.tableWidget.itemChanged.connect(self.save_table)
        self.actionShow_Task.triggered.connect(self.reloadtask)
        #self.actionShow_Theory.triggered.connect(self.reloadtheory)

    def save_table(self, item):
        if self.savestatus:
            col = item.column()
            row = item.row()
            elem = float(self.tableWidget.item(row, col).text())
            if col < 5:
                print(row, col)
            elif self.status == 'Tasks':
                try:
                    print('Imtryina')
                    self.cur.execute(f'DELETE FROM StudentTask '
                                     f'WHERE st_stu_id = {row + 1} AND st_task_id = {col - 4}')
                    print('Imtryina')
                    self.db_connection.commit()
                    self.cur.execute(f'INSERT INTO StudentTask (st_stu_id, st_task_id, st_mark) '
                                     f'VALUES ({row + 1}, {col - 4}, {elem})')
                    print('Imtryina')
                    self.db_connection.commit()
                except:
                    print('Here')
                    self.cur.execute(f'INSERT INTO StudentTask (st_stu_id, st_task_id, st_mark) '
                                     f'VALUES ({row + 1}, {col - 4}, {elem})')
            self.db_connection.commit()
        else:
            pass

    def reloadtask(self):
        self.status = 'Tasks'
        self.savestatus = False
        self.tableWidget.clear()
        db_connection = sqlite3.connect('marks.db')
        cur = db_connection.cursor()
        tasky_lucky = list(map(lambda x: x[0], cur.execute(f'SELECT task_id '
                                                           f'FROM Task')))
        title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
            map(lambda x: str(x[0]), cur.execute(f'SELECT task_id '
                                                 f'FROM Task')))
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        stu_data = cur.execute(
            f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
            f'FROM Student').fetchall()
        for i, row in enumerate(stu_data):
            reader_two = tuple(
                map(lambda x: cur.execute(f'SELECT st_mark '
                                          f'FROM StudentTask '
                                          f'WHERE st_stu_id = {i + 1} and st_task_id = {x}').fetchone(), tasky_lucky))
            for j, elem in enumerate(row + reader_two):
                if type(elem) == tuple:
                    elem = list(elem)[0]
                if elem is None:
                    elem = ''
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.savestatus = True

    def header_clicked(self, item):
        if item == 4:
            self.code = 'Legacy'
            self.loadtable()
        elif item == 0:
            self.code = 'Traditional'
            self.loadtable()
        elif item >= 5:
            taskn = int(self.tableWidget.horizontalHeaderItem(item).text())
            example = Tasky()
            example.lineEditId.setText(str(taskn))
            equals = self.cur.execute(f'SELECT task_number, task_theme, task_equation, task_date '
                                      f'FROM Task '
                                      f'WHERE task_id = {taskn}').fetchone()
            print(equals[0])
            example.lineEditTheme.setText(list(equals)[1])
            example.lineEditDate.setText(list(equals)[3])
            example.lineEditNumber.setText(list(equals)[0])
            example.textEdit.setText(list(equals)[2])
            example.exec_()


    def loadtable(self):
        self.tableWidget.clear()
        self.savestatus = False
        if self.status == 'Tasks' and self.code == 'Nothing':
            db_connection = sqlite3.connect('marks.db')
            cur = db_connection.cursor()
            tasky_lucky = list(map(lambda x: x[0], cur.execute(f'SELECT task_id '
                                                               f'FROM Task')))
            title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
                map(lambda x: str(x[0]), cur.execute(f'SELECT task_id '
                                                     f'FROM Task')))
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            stu_data = cur.execute(
                f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
                f'FROM Student').fetchall()
            for i, row in enumerate(stu_data):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                reader_two = tuple(
                    map(lambda x: cur.execute(f'SELECT st_mark '
                                              f'FROM StudentTask '
                                              f'WHERE st_stu_id = {i + 1} and st_task_id = {x}').fetchone(), tasky_lucky))
                for j, elem in enumerate(row + reader_two):
                    if type(elem) == tuple:
                        elem = list(elem)[0]
                    if elem is None:
                        elem = ''
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        if self.status == 'Tasks' and self.code == 'Traditional':
            db_connection = sqlite3.connect('marks.db')
            cur = db_connection.cursor()
            tasky_lucky = list(map(lambda x: x[0], cur.execute(f'SELECT task_id '
                                                               f'FROM Task')))
            title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
                map(lambda x: str(x[0]), cur.execute(f'SELECT task_id '
                                                     f'FROM Task')))
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            stu_data = cur.execute(
                f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
                f'FROM Student').fetchall()
            for i, row in enumerate(stu_data):
                reader_two = tuple(
                    map(lambda x: cur.execute(f'SELECT st_mark '
                                              f'FROM StudentTask '
                                              f'WHERE st_stu_id = {i + 1} and st_task_id = {x}').fetchone(), tasky_lucky))
                for j, elem in enumerate(row + reader_two):
                    if type(elem) == tuple:
                        elem = list(elem)[0]
                    if elem is None:
                        elem = ''
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        elif self.status == 'Tasks' and self.code == 'Legacy':
            db_connection = sqlite3.connect('marks.db')
            cur = db_connection.cursor()
            tasky_lucky = list(map(lambda x: x[0], cur.execute(f'SELECT task_id '
                                                               f'FROM Task')))
            title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
                map(lambda x: str(x[0]), cur.execute(f'SELECT task_id '
                                                     f'FROM Task')))
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            stu_data = cur.execute(
                f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
                f'FROM Student '
                f'ORDER BY stu_legacy').fetchall()
            for i, row in enumerate(stu_data):
                r_id = list(cur.execute(f'SELECT stu_id '
                                        f'FROM Student '
                                        f'WHERE stu_legacy = {i+1}'))[0][0]
                reader_two = tuple(
                    map(lambda x: cur.execute(f'SELECT st_mark '
                                              f'FROM StudentTask '
                                              f'WHERE st_stu_id = {r_id} and st_task_id = {x}').fetchone(), tasky_lucky))
                for j, elem in enumerate(row + reader_two):
                    if type(elem) == tuple:
                        elem = list(elem)[0]
                    if elem is None:
                        elem = ''
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        self.savestatus = True



def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys._excepthook = sys.excepthook

sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConduitMain()
    ex.show()
    sys.exit(app.exec_())