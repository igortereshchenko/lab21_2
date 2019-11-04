from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

from model import model


class QuestionForm(FlaskForm):
    Questions = StringField("questions", [validators.DataRequired("Question is required")])

    Submit = SubmitField("Save")

    def model(self):
        return model.QuestionsTable(
            Questions=self.Questions.data
        )
