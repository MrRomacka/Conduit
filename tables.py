from db_session import SqlAlchemyBase
import sqlalchemy as sa


class Students(SqlAlchemyBase):
    __tablename__ = 'Student'
    stu_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    stu_surname = sa.Column(sa.String)
    stu_name = sa.Column(sa.String)
    stu_group = sa.Column(sa.String)
    stu_legacy = sa.Column(sa.Integer)
    stu_procent = sa.Column(sa.Integer)
    stu_finmark = sa.Column(sa.Integer)


class Tasks(SqlAlchemyBase):
    __tablename__ = 'Task'
    task_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task_number = sa.Column(sa.String)
    task_equation = sa.Column(sa.String)
    task_percent = sa.Column(sa.Integer)
    task_date = sa.Column(sa.String)
    task_type = sa.Column(sa.String)


class Theories(SqlAlchemyBase):
    __tablename__ = 'Theory'
    theory_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    theory_maintheme = sa.Column(sa.String)
    theory_questions = sa.Column(sa.String)
    theory_percent = sa.Column(sa.String)


class StudentsTasks(SqlAlchemyBase):
    st_stu_id = sa.Column(sa.Integer, foreign_key='Student.stu_id')
    st_task_id = sa.Column(sa.Integer, foreign_key='Task.task_id')
    st_mark = sa.Column(sa.Integer)


class StudentsTheories(SqlAlchemyBase):
    sth_stu_id = sa.Column(sa.Integer, foreign_key='Student.stu_id')
    sth_theory_id = sa.Column(sa.Integer, foreign_key='Theory.theory_id')
    sth_quenum = sa.Column(sa.Integer)
    sth_mark = sa.Column(sa.Integer)