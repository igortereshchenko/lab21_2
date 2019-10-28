from flask_wtf import Form
from wtforms import SubmitField, HiddenField, IntegerField
from wtforms import validators


class ResultForm(Form):
    duration = IntegerField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.number_range(0)
    ])
    complex = IntegerField("Teacher Name: ", [
        validators.DataRequired("Please enter teacher name."),
        validators.number_range(0, 10)
    ])

    old_name = HiddenField()

    submit = SubmitField("Save")
