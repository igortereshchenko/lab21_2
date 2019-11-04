from wtforms import StringField, DateTimeField, SubmitField, BooleanField, SelectField, validators
from flask_wtf import FlaskForm
import models


class SkillForm(FlaskForm):
    Name = StringField("Name")
    Vacancy = StringField("Vacancy")
    CreationDate = DateTimeField("Creation date")
    RemoveDate = DateTimeField("Remove date")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Skills(
            Name=self.Name.data,
            Vacancy=self.Vacancy.data,
            CreationDate=self.CreationDate.data,
            RemoveDate=self.RemoveDate.data
        )
