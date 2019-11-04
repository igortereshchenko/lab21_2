from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms import validators


class SkillForm(Form):
    student_name = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])
    student_group = IntegerField("Group: ", [
        validators.DataRequired("Please enter student Group.")])
    name = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(0, 100, "Name should be from 0 to 100 symbols")
    ])
    type = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
    ])
    vacancy = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
    ])
    creation_date = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.number_range(min=2019,message="Date should be after 2019")
    ])

    old_student_name = HiddenField()
    old_student_group = HiddenField()
    old_name = HiddenField()
    old_vacancy = HiddenField()
    old_creation_date = HiddenField()
    old_student_entity = HiddenField()

    submit = SubmitField("Save")
