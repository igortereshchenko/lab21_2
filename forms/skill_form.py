from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms import validators


class SkillForm(Form):
    student_name = StringField("student name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])
    student_group = IntegerField("student group: ", [
        validators.DataRequired("Please enter student group.")])
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
    creation_date = StringField("creation date: ", [
        validators.DataRequired("Please enter creation date."),
        validators.number_range(min=2019,message="Date should be after 2019")
    ])

    old_student_name = HiddenField()
    old_student_group = HiddenField()
    old_name = HiddenField()
    old_student_entity = HiddenField()

    submit = SubmitField("Save")
