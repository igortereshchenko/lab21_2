from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField

from model import model


class StudentHasWorkForm(FlaskForm):
    Student_name = SelectField("student_name", validators=[validators.DataRequired()])
    Position = SelectField("position", validators=[validators.DataRequired()])

    Submit = SubmitField("Save")

    def model(self):
        return model.StudentHasWork(
            StudentCardFk=self.Student_name.data,
            WorkIdFk=self.Position.data
        )
