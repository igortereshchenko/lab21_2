from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators, ValidationError


class SkillForm(Form):
    name = StringField("name: ", [
        validators.DataRequired("Please enter skill name."),
        validators.Length(0, 100, "Name should be from 0 to 100 symbols")
    ])
    type = StringField("type: ", [
        validators.DataRequired("Please enter skill type."),
    ])
    vacancy = StringField("vacancy: ", [
        validators.DataRequired("Please enter skill vacancy."),
    ])
    def validate_on_submit(form,field):
        if (field.data < '2019-01-01 0:0:0-0'):
            raise ValidationError('Date should be after 2019')
    creation_date = StringField("creation date: ", [
        validators.DataRequired("Please enter creation date."),
        validate_on_submit
    ])



    student_name = HiddenField()
    student_group = HiddenField()
    old_name = HiddenField()

    submit = SubmitField("Save")
