from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, IntegerField, DateField
from datetime import date

from model import model


class WorkForm(FlaskForm):
    Position = StringField("position", validators=[validators.DataRequired("Position can't be empty")])
    Salary = IntegerField("salary",
                          validators=[validators.NumberRange(min=1), validators.DataRequired("Salary can't be 0")])
    Start_date = DateField('start_date', format='%d.%m.%Y',
                           validators=[validators.DataRequired()])
    End_date = DateField("end_date", format='%d.%m.%Y',
                         validators=[validators.DataRequired()])

    Submit = SubmitField("Save")

    def validate_on_start_date(self):
        result = super(WorkForm, self).validate()
        if self.Start_date.data == date.today() or self.Start_date.data < date.today():
            return False
        else:
            return result

    def validate_on_end_date(self):
        result = super(WorkForm, self).validate()
        if self.End_date.data < self.Start_date.data:
            return False
        else:
            return result

    def model(self):
        return model.WorkTable(
            Position=self.Position.data,
            Salary=self.Salary.data,
            Start_date=self.Start_date.data,
            End_date=self.End_date.data
        )
