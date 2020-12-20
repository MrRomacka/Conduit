import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from cond_main_win import Ui_MainWindow
import cond_task_win
import sqlite3


class Tasky(QDialog, cond_task_win.Ui_Dialog):
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
        if int(cur.execute('SELECT MAX(task_id) FROM Task').fetchone()[0]) >= int(t_id):
            cur.execute(f'UPDATE Task '
                    f'SET task_id={int(t_id)}, task_number="{t_num}", task_theme="{t_theme}", task_equation="{t_equa}", '
                    f'task_date="{t_date}" WHERE task_id={int(t_id)}')
        else:
            print(f'INSERT INTO Task (task_id, task_number, task_theme, task_equation, task_date)',
                        f'VALUES ({int(t_id)}, "{t_num}", "{t_theme}", "{t_equa}", "{t_date}")')
            cur.execute(f'INSERT INTO Task (task_id, task_number, task_theme, task_equation, task_date) '
                        f'VALUES ({int(t_id)}, "{t_num}", "{t_theme}", "{t_equa}", "{t_date}")')
        db_connection.commit()
        db_connection.close()
        self.close()


class Theoricky(QDialog, cond_task_win.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonSave.clicked.connect(self.__save_task)

    def __save_task(self):
        th_id = self.lineEditId.text()
        th_num = self.lineEditNumber.text()
        th_theme = self.lineEditTheme.text()
        th_equa = self.textEdit.toPlainText()
        db_connection = sqlite3.connect('marks.db')
        cur = db_connection.cursor()
        if int(cur.execute('SELECT MAX(theory_id) FROM Theory').fetchone()[0]) >= int(th_id):
            cur.execute(f'UPDATE Theory '
                        f'SET theory_id={int(th_id)}, theory_num={int(th_num)}, '
                        f'theory_maintheme="{th_theme}", theory_questions="{th_equa}" '
                        f'WHERE theory_id={int(th_id)}')
        else:
            cur.execute(f'INSERT INTO Theory (theory_id, theory_num, theory_maintheme, theory_questions) '
                        f'VALUES ({int(th_id)}, {int(th_num)}, "{th_theme}", "{th_equa}")')
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
        self.actionNew_Task.triggered.connect(self.make_a_task)
        self.actionShow_Theory.triggered.connect(self.reloadtheory)
        self.actionNew_Theory.triggered.connect(self.make_a_theory)

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
            self.code = 'Traditional'

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

        elif self.status == 'Theory' and self.code == 'Traditional':
            db_connection = sqlite3.connect('marks.db')
            cur = db_connection.cursor()
            theoritic = list(map(lambda x: x[0], cur.execute(f'SELECT theory_id '
                                                               f'FROM Theory')))
            title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
                map(lambda x: str(x[0]), cur.execute(f'SELECT theory_id '
                                                               f'FROM Theory')))
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            stu_data = cur.execute(
                f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
                f'FROM Student').fetchall()
            for i, row in enumerate(stu_data):
                reader_two = tuple(
                    map(lambda x: cur.execute(f'SELECT sth_mark '
                                              f'FROM StudentTheory '
                                              f'WHERE sth_stu_id = {i + 1} and sth_theory_id = {x}').fetchone(), theoritic))
                for j, elem in enumerate(row + reader_two):
                    if type(elem) == tuple:
                        elem = list(elem)[0]
                    if elem is None:
                        elem = ''
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

        elif self.status == 'Theory' and self.code == 'Legacy':
            db_connection = sqlite3.connect('marks.db')
            cur = db_connection.cursor()
            theoritic = list(map(lambda x: x[0], cur.execute(f'SELECT theory_id '
                                                               f'FROM Theory')))
            title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
                map(lambda x: str(x[0]), cur.execute(f'SELECT theory_id '
                                                               f'FROM Theory')))
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
                    map(lambda x: cur.execute(f'SELECT sth_mark '
                                              f'FROM StudentTheory '
                                              f'WHERE sth_stu_id = {r_id} and sth_theory_id = {x}').fetchone(), theoritic))
                for j, elem in enumerate(row + reader_two):
                    if type(elem) == tuple:
                        elem = list(elem)[0]
                    if elem is None:
                        elem = ''
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        self.savestatus = True

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
            elif self.status == 'Theory':
                print(self.status)
                try:
                    print('Imtryina')
                    self.cur.execute(f'DELETE FROM StudentTheory '
                                     f'WHERE sth_stu_id = {row + 1} AND sth_theory_id = {col - 4}')
                    print('Imtryina')
                    self.db_connection.commit()
                    self.cur.execute(f'INSERT INTO StudentTheory (sth_stu_id, sth_theory_id, sth_mark) '
                                     f'VALUES ({row + 1}, {col - 4}, {elem})')
                    print('Imtryina')
                    self.db_connection.commit()
                except:
                    print('here')
                    self.cur.execute(f'INSERT INTO StudentTheory (sth_stu_id, sth_theory_id, sth_mark) '
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

    def reloadtheory(self):
        self.status = 'Theory'
        self.savestatus = False
        self.tableWidget.clear()
        db_connection = sqlite3.connect('marks.db')
        cur = db_connection.cursor()
        theoritic = list(map(lambda x: x[0], cur.execute(f'SELECT theory_id '
                                                         f'FROM Theory')))
        title = ['stu_id', 'stu_surname', 'stu_name', 'stu_group', 'stu_legacy'] + list(
            map(lambda x: str(x[0]), cur.execute(f'SELECT theory_id '
                                                 f'FROM Theory')))
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        stu_data = cur.execute(
            f'SELECT stu_id, stu_surname, stu_name, stu_group, stu_legacy '
            f'FROM Student').fetchall()
        for i, row in enumerate(stu_data):
            reader_two = tuple(
                map(lambda x: cur.execute(f'SELECT sth_mark '
                                          f'FROM StudentTheory '
                                          f'WHERE sth_stu_id = {i + 1} and sth_theory_id = {x}').fetchone(), theoritic))
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
            if self.status == 'Tasks':
                taskn = int(self.tableWidget.horizontalHeaderItem(item).text())
                example = Tasky()
                example.lineEditId.setText(str(taskn))
                equals = self.cur.execute(f'SELECT task_number, task_theme, task_equation, task_date '
                                          f'FROM Task '
                                          f'WHERE task_id = {taskn}').fetchone()
                example.lineEditTheme.setText(list(equals)[1])
                example.lineEditDate.setText(list(equals)[3])
                example.lineEditNumber.setText(list(equals)[0])
                example.textEdit.setText(list(equals)[2])
                example.exec_()
            elif self.status == 'Theory':
                theoryn = int(self.tableWidget.horizontalHeaderItem(item).text())
                example = Theoricky()
                example.lineEditId.setText(str(theoryn))
                equals = self.cur.execute(f'SELECT theory_num, theory_maintheme, theory_questions '
                                          f'FROM Theory '
                                          f'WHERE theory_id = {theoryn}').fetchone()
                example.lineEditTheme.setText(list(equals)[1])
                example.lineEditNumber.setText(str(list(equals)[0]))
                example.textEdit.setText(list(equals)[2])
                example.exec_()

    def make_a_task(self):
        id_t = int(self.cur.execute('SELECT MAX(task_id) FROM Task').fetchone()[0]) + 1
        example = Tasky()
        example.lineEditId.setText(str(id_t))
        example.exec_()
        self.loadtable()

    def make_a_theory(self):
        id_th = int(self.cur.execute('SELECT MAX(theory_id) FROM Theory').fetchone()[0]) + 1
        example = Theoricky()
        example.lineEditId.setText(str(id_th))
        example.exec_()
        self.loadtable()


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