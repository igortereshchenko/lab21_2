from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

from model import model


class StudentForm(FlaskForm):
    Student_name = StringField("student_name", [validators.DataRequired("Name is required")])
    Student_surname = StringField("student_surname", [validators.DataRequired("Surname is required")])

    Submit = SubmitField("Save")

    def model(self):
        return model.StudentTable(
            Student_name=self.Student_name.data,
            Student_surname=self.Student_surname.data
        )
