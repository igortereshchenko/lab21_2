from wtforms import StringField, DateTimeField, SubmitField, BooleanField, SelectField, validators
from flask_wtf import FlaskForm
from datetime import datetime
import models


class SkillForm(FlaskForm):
    Name = StringField("Name", [validators.length(3, 10)])
    Vacancy = StringField("Vacancy")
    CreationDate = DateTimeField("Creation date")
    RemoveDate = DateTimeField("Remove date")

    Submit = SubmitField("Save")

    def validate(self):
        validation = super(SkillForm, self).validate()

        if self.CreationDate.data >= datetime.now():
            return False
        else:
            return validation

    def domain(self):
        return models.Skills(
            Name=self.Name.data,
            Vacancy=self.Vacancy.data,
            CreationDate=self.CreationDate.data,
            RemoveDate=self.RemoveDate.data
        )
