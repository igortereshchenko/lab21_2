from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

from model import model


class AnswerForm(FlaskForm):
    Answer_for_question = StringField("answer_for_question", [validators.DataRequired("Answer is required")])
    Question = SelectField("question", validators=[validators.DataRequired()])

    Submit = SubmitField("Save")

    def model(self):
        return model.AnswerTable(
            QuestionIdFk=self.Question.data,
            Answer_for_question=self.Answer_for_question.data
        )
