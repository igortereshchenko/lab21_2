from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, StringField, IntegerField

from model import model
from model.colors_type import colors_type


class CarsForm(FlaskForm):
    Model = StringField("model", validators=[validators.DataRequired("Car must have model")])
    Cost = IntegerField("cost", [validators.NumberRange(min=1), validators.DataRequired("Car's cost can't be 0")])
    Number = IntegerField("number", [validators.DataRequired("Number is required")])
    Color = SelectField("color", [validators.DataRequired("Color is required")], choices=colors_type)
    Student_name = SelectField("student_name", validators=[validators.DataRequired()])

    Submit = SubmitField("Save")

    def model(self):
        return model.CarsTable(
            Model=self.Model.data,
            Cost=self.Cost.data,
            Number=self.Number.data,
            Color=self.Color.data,
            StudentCardFk=self.Student_name.data
        )
