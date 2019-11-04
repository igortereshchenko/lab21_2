from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

from forms.AnswerForm import AnswerForm
from forms.QuestionForm import QuestionForm
from forms.QuestionnaireForm import QuestionnaireForm
from forms.StudentForm import StudentForm
from forms.WorkForm import WorkForm
from forms.StudentHasWorkForm import StudentHasWorkForm
from forms.CarsForm import CarsForm

db = SQLAlchemy()


class QuestionsTable(db.Model):
    __tablename__ = 'questions_table'

    Question_id = db.Column("question_id", db.Integer, primary_key=True)
    Questions = db.Column("questions", db.String, nullable=False)

    def filled_form(self):
        return QuestionForm(Questions=self.Questions)

    def map_to_form(self, form):
        self.Questions = form.Questions.data


class AnswerTable(db.Model):
    __tablename__ = 'answer_table'

    Answer_id = db.Column("answer_id", db.Integer, primary_key=True)
    Answer_for_question = db.Column("answer_for_question", db.String, nullable=False)

    QuestionIdFk = db.Column("question_id_fk", db.Integer, db.ForeignKey("questions_table.question_id"))
    Question = db.relationship("QuestionsTable", backref=backref('children', cascade='all,delete'),
                               passive_deletes=True)

    def filled_form(self):
        return AnswerForm(
            Question=self.QuestionIdFk,
            Answer_for_question=self.Answer_for_question)

    def map_to_form(self, form):
        self.QuestionIdFk = form.Question.data
        self.Answer_for_question = form.Answer_for_question.data


class QuestionnaireTable(db.Model):
    __tablename__ = 'questionnaire_table'
    Questionnaire_id = db.Column("questionnaire_id", db.Integer, primary_key=True)
    Type_question = db.Column("type_question", db.String, nullable=False)

    AnswerIdFk = db.Column("answer_id_fk", db.Integer, db.ForeignKey("answer_table.answer_id"))
    Answer = db.relationship("AnswerTable", backref=backref('children', cascade='all,delete'),
                             passive_deletes=True)
    QuestionIdFk = db.Column("question_id_fk", db.Integer, db.ForeignKey("questions_table.question_id"))
    Question = db.relationship("QuestionsTable", backref=backref('children2', cascade='all,delete'),
                               passive_deletes=True)

    def filled_form(self):
        return QuestionnaireForm(
            Type_question=self.Type_question,
            Question=self.QuestionIdFk,
            Answer=self.AnswerIdFk)

    def map_to_form(self, form):
        self.Type_question = form.Type_question.data
        self.QuestionIdFk = form.Questions.data
        self.AnswerIdFk = form.Answer_for_question.data


class StudentTable(db.Model):
    __tablename__ = 'student_table'
    Student_card = db.Column("student_card", db.Integer, primary_key=True)
    Student_name = db.Column("student_name", db.String, nullable=False)
    Student_surname = db.Column("student_surname", db.String, nullable=False)

    def filled_form(self):
        return StudentForm(
            Student_name=self.Student_name,
            Student_surname=self.Student_surname)

    def map_to_form(self, form):
        self.Student_name = form.Student_name.data
        self.Student_surname = form.Student_surname.data


class WorkTable(db.Model):
    __tablename__ = 'work_table'
    Work_id = db.Column("work_id", db.Integer, primary_key=True)
    Start_date = db.Column("start_date", db.TIMESTAMP, default=datetime.now)
    End_date = db.Column("end_date", db.TIMESTAMP)
    Salary = db.Column("salary", db.Integer, nullable=False)
    Position = db.Column("position", db.String, nullable=False)

    def filled_form(self):
        return WorkForm(
            Position=self.Position,
            Salary=self.Salary,
            Start_date=self.Start_date,
            End_date=self.End_date
        )

    def map_to_form(self, form):
        self.Position = form.Position.data
        self.Salary = form.Salary.data
        self.Start_date = form.Start_date.data
        self.End_date = form.End_date.data


class StudentHasWork(db.Model):
    __tablename__ = 'student_has_work_table'

    Student_work_id = db.Column("student_work_id", db.Integer, primary_key=True)

    StudentCardFk = db.Column("student_card_fk", db.Integer, db.ForeignKey("student_table.student_card"))
    Student = db.relationship("StudentTable", backref=backref('student', cascade='all,delete'),
                              passive_deletes=True)
    WorkIdFk = db.Column("work_id_fk", db.Integer, db.ForeignKey("work_table.work_id"))
    Work = db.relationship("WorkTable", backref=backref('work', cascade='all,delete'),
                           passive_deletes=True)

    def filled_form(self):
        return StudentHasWorkForm(
            Student=self.StudentCardFk,
            Work=self.WorkIdFk)

    def map_to_form(self, form):
        self.StudentCardFk = form.Student_name.data
        self.WorkIdFk = form.Position.data


class CarsTable(db.Model):
    __tablename__ = 'cars_table'

    Car_id = db.Column("student_work_id", db.Integer, primary_key=True)
    Model = db.Column("model", db.String, nullable=False)
    Cost = db.Column("cost", db.Integer, nullable=False)
    Number = db.Column("number", db.Integer, nullable=False)
    Color = db.Column("color", db.String, nullable=False)

    StudentCardFk = db.Column("student_card_fk", db.Integer, db.ForeignKey("student_table.student_card"))
    Student = db.relationship("StudentTable", backref=backref('students_car', cascade='all,delete'),
                              passive_deletes=True)

    def filled_form(self):
        return CarsForm(
            Model=self.Model,
            Cost=self.Cost,
            Number=self.Number,
            Color=self.Color,
            Student=self.StudentCardFk,
        )

    def map_to_form(self, form):
        self.Model = form.Model.data
        self.Cost = form.Cost.data
        self.Number = form.Number.data
        self.Color = form.Color.data
        self.StudentCardFk = form.Student_name.data
