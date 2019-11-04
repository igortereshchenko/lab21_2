from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField

from model import model
from model.question_types import question_types


class QuestionnaireForm(FlaskForm):
    Type_question = SelectField("type_question", [validators.DataRequired("Type is required")], choices=question_types)
    Questions = SelectField("questions", validators=[validators.DataRequired()])
    Answer_for_question = SelectField("answer_for_question", validators=[validators.DataRequired()])

    Submit = SubmitField("Save")

    def model(self):
        return model.QuestionnaireTable(
            Type_question=self.Type_question.data,
            QuestionIdFk=self.Questions.data,
            AnswerIdFk=self.Answer_for_question.data
        )
