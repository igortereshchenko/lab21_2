import os

from flask import Flask, request, render_template, redirect, url_for

from connecting.credentials import *
from model.model import db, QuestionsTable, AnswerTable, QuestionnaireTable, StudentTable, WorkTable, StudentHasWork, \
    CarsTable
from forms.QuestionForm import QuestionForm
from forms.AnswerForm import AnswerForm
from forms.QuestionnaireForm import QuestionnaireForm
from forms.StudentForm import StudentForm
from forms.WorkForm import WorkForm
from forms.StudentHasWorkForm import StudentHasWorkForm
from forms.CarsForm import CarsForm
from model.vizualization import visualization_data

app = Flask(__name__)
app.secret_key = 'development key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route('/')
def root():
    db.create_all()
    return render_template("main.html")


@app.route('/map')
def map():
    db.create_all()

    student_1 = StudentTable(Student_name='Bob',
                             Student_surname='Bobov')
    student_2 = StudentTable(Student_name='Boba',
                             Student_surname='Bobenko')
    student_3 = StudentTable(Student_name='Bobik',
                             Student_surname='Bobenchuk')

    car_1 = CarsTable(Model='BMW',
                      Cost='1000',
                      Number='123456',
                      Color='Red',
                      StudentCardFk=2
                      )

    car_2 = CarsTable(Model='Audi',
                      Cost='750',
                      Number='987654',
                      Color='Green',
                      StudentCardFk=2
                      )

    car_3 = CarsTable(Model='Nissan',
                      Cost='200',
                      Number='888888',
                      Color='Red',
                      StudentCardFk=3
                      )

    # db.session.add_all([student_1, student_2, student_3])
    db.session.add_all([car_1, car_2, car_3])
    db.session.commit()
    return render_template("main.html")


# Answers table supporting ---------------------------------------------------------------------------------------------

@app.route("/questions")
def questions():
    all_questions = QuestionsTable.query.all()
    return render_template("questions/index.html", questions=all_questions)


@app.route("/questions/new", methods=["GET", "POST"])
def new_question():
    form = QuestionForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("questions/create.html", form=form)
        else:
            question = form.model()
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("questions"))

    return render_template("questions/create.html", form=form)


@app.route("/questions/delete/<uuid>", methods=["POST"])
def delete_question(uuid):
    question = QuestionsTable.query.filter(QuestionsTable.Question_id == uuid).first()
    if question:
        db.session.delete(question)
        db.session.commit()

    return redirect(url_for("questions"))


@app.route("/questions/<uuid>", methods=["GET", "POST"])
def update_question(uuid):
    question = QuestionsTable.query.filter(QuestionsTable.Question_id == uuid).first()
    form = question.filled_form()

    if request.method == "POST":
        if not form.validate():
            return render_template("questions/update.html", form=form)

        question.map_to_form(form)
        db.session.commit()
        return redirect(url_for("questions"))

    return render_template("questions/update.html", form=form)


# Answers table supporting ---------------------------------------------------------------------------------------------

@app.route("/answers")
def answers():
    all_answers = AnswerTable.query.join(QuestionsTable).all()
    return render_template("answers/index.html", answers=all_answers)


@app.route("/answers/new", methods=["GET", "POST"])
def new_answer():
    form = AnswerForm()
    form.Question.choices = [(str(question.Question_id), question.Questions) for question in QuestionsTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("answers/create.html", form=form)
        else:
            answer = form.model()
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for("answers"))

    return render_template("answers/create.html", form=form)


@app.route("/answers/delete/<uuid>", methods=["POST"])
def delete_answer(uuid):
    answer = AnswerTable.query.filter(AnswerTable.Answer_id == uuid).first()
    if answer:
        db.session.delete(answer)
        db.session.commit()

    return redirect(url_for("answers"))


@app.route("/answers/<uuid>", methods=["GET", "POST"])
def update_answer(uuid):
    answer = AnswerTable.query.filter(AnswerTable.Answer_id == uuid).first()
    form = answer.filled_form()
    form.Question.choices = [(str(question.Question_id), question.Questions) for question in QuestionsTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("answers/update.html", form=form)

        answer.map_to_form(form)
        db.session.commit()
        return redirect(url_for("answers"))

    return render_template("answers/update.html", form=form)


@app.route("/questionnaires")
def questionnaires():
    all_questionnaires = QuestionnaireTable.query.join(AnswerTable).all()
    return render_template("questionnaires/index.html", questionnaires=all_questionnaires)


@app.route("/questionnaires/new", methods=["GET", "POST"])
def new_questionnaire():
    form = QuestionnaireForm()
    form.Questions.choices = [(str(question.Question_id), question.Questions) for question in
                              QuestionsTable.query.all()]
    form.Answer_for_question.choices = [(str(answer.Answer_id), answer.Answer_for_question) for answer in
                                        AnswerTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("questionnaires/create.html", form=form)
        else:
            questionnaire = form.model()
            db.session.add(questionnaire)
            db.session.commit()
            return redirect(url_for("questionnaires"))

    return render_template("questionnaires/create.html", form=form)


@app.route("/questionnaires/delete/<uuid>", methods=["POST"])
def delete_questionnaire(uuid):
    questionnaire = QuestionnaireTable.query.filter(QuestionnaireTable.Questionnaire_id == uuid).first()
    if questionnaire:
        db.session.delete(questionnaire)
        db.session.commit()

    return redirect(url_for("questionnaires"))


@app.route("/questionnaires/<uuid>", methods=["GET", "POST"])
def update_questionnaire(uuid):
    questionnaire = QuestionnaireTable.query.filter(QuestionnaireTable.Questionnaire_id == uuid).first()
    form = questionnaire.filled_form()
    form.Questions.choices = [(str(question.Question_id), question.Questions) for question in
                              QuestionsTable.query.all()]
    # form.Answer_for_question.choices = [(str(answer.Answer_id), answer.Answer_for_question) for answer in AnswerTable.query.all()]
    form.Answer_for_question.choices = [
        (str(answer.Answer_id), f"{answer.Answer_for_question} ({answer.Question.Questions})") for answer in
        AnswerTable.query.join(QuestionsTable, AnswerTable.QuestionIdFk == QuestionsTable.Question_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("questionnaires/update.html", form=form)

        questionnaire.map_to_form(form)
        db.session.commit()
        return redirect(url_for("questionnaires"))

    return render_template("questionnaires/update.html", form=form)


@app.route("/students")
def students():
    all_students = StudentTable.query.all()
    return render_template("students/index.html", students=all_students)


@app.route("/students/new", methods=["GET", "POST"])
def new_student():
    form = StudentForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("students/create.html", form=form)
        else:
            student_add = form.model()
            db.session.add(student_add)
            db.session.commit()
            return redirect(url_for("students"))

    return render_template("students/create.html", form=form)


@app.route("/students/delete/<uuid>", methods=["POST"])
def delete_student(uuid):
    student_delete = StudentTable.query.filter(StudentTable.Student_card == uuid).first()
    if student_delete:
        db.session.delete(student_delete)
        db.session.commit()

    return redirect(url_for("students"))


@app.route("/students/<uuid>", methods=["GET", "POST"])
def update_student(uuid):
    student_update = StudentTable.query.filter(StudentTable.Student_card == uuid).first()
    form = student_update.filled_form()

    if request.method == "POST":
        if not form.validate():
            return render_template("students/update.html", form=form)

        student_update.map_to_form(form)
        db.session.commit()
        return redirect(url_for("students"))

    return render_template("students/update.html", form=form)


@app.route("/shows")
def shows():
    all_show = WorkTable.query.all()
    return render_template("shows/index.html", shows=all_show)


@app.route("/shows/new", methods=["GET", "POST"])
def new_show():
    form = WorkForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("shows/create.html", form=form)
        elif not form.validate_on_start_date():
            error_start = "test"
            return render_template("shows/create.html", form=form, error_start=error_start)
        elif not form.validate_on_end_date():
            error_end = "test2"
            return render_template("shows/create.html", form=form, error_end=error_end)
        else:
            show_new = form.model()
            db.session.add(show_new)
            db.session.commit()
            return redirect(url_for("shows"))

    return render_template("shows/create.html", form=form)


@app.route("/shows/delete/<uuid>", methods=["POST"])
def delete_show(uuid):
    show_delete = WorkTable.query.filter(WorkTable.Work_id == uuid).first()
    if show_delete:
        db.session.delete(show_delete)
        db.session.commit()

    return redirect(url_for("shows"))


@app.route("/shows/<uuid>", methods=["GET", "POST"])
def update_show(uuid):
    show_update = WorkTable.query.filter(WorkTable.Work_id == uuid).first()
    form = show_update.filled_form()

    if request.method == "POST":
        if not form.validate():
            return render_template("shows/update.html", form=form)
        elif not form.validate_on_start_date():
            error_start = "test"
            return render_template("shows/update.html", form=form, error_start=error_start)
        elif not form.validate_on_end_date():
            error_end = "test2"
            return render_template("shows/update.html", form=form, error_end=error_end)

        show_update.map_to_form(form)
        db.session.commit()
        return redirect(url_for("shows"))

    return render_template("shows/update.html", form=form)


@app.route("/studentwork")
def studentwork():
    all_studentwork = StudentHasWork.query.join(StudentTable).join(WorkTable).all()
    return render_template("studentwork/index.html", studentworks=all_studentwork)


@app.route("/studentwork/new", methods=["GET", "POST"])
def new_studentwork():
    form = StudentHasWorkForm()
    form.Student_name.choices = [
        (str(student.Student_card), f"{student.Student_name} {student.Student_surname}") for student in
        StudentTable.query.all()]

    form.Position.choices = [(str(position.Work_id), position.Position) for position in
                             WorkTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("questionnaires/create.html", form=form)
        else:
            studentwork = form.model()
            db.session.add(studentwork)
            db.session.commit()
            return redirect(url_for("studentwork"))

    return render_template("studentwork/create.html", form=form)


@app.route("/studentwork/delete/<uuid>", methods=["POST"])
def delete_studentwork(uuid):
    studentwork = StudentHasWork.query.filter(StudentHasWork.Student_work_id == uuid).first()
    if studentwork:
        db.session.delete(studentwork)
        db.session.commit()

    return redirect(url_for("studentwork"))


@app.route("/studentwork/<uuid>", methods=["GET", "POST"])
def update_studentwork(uuid):
    studentwork = StudentHasWork.query.filter(StudentHasWork.Student_work_id == uuid).first()
    form = studentwork.filled_form()
    form.Student_name.choices = [
        (str(student.Student_card), f"{student.Student_name} {student.Student_surname}") for student in
        StudentTable.query.all()]

    form.Position.choices = [(str(position.Work_id), position.Position) for position in
                             WorkTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("studentwork/update.html", form=form)

        studentwork.map_to_form(form)
        db.session.commit()
        return redirect(url_for("studentwork"))

    return render_template("studentwork/update.html", form=form)


@app.route("/show")
def show():
    all_cars = CarsTable.query.join(StudentTable).all()
    return render_template("show/index.html", cars=all_cars)


@app.route("/show/add", methods=["GET", "POST"])
def new_car():
    form = CarsForm()
    form.Student_name.choices = [
        (str(student.Student_card), f"{student.Student_name} {student.Student_surname}") for student in
        StudentTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("show/create.html", form=form)
        else:
            cars = form.model()
            db.session.add(cars)
            db.session.commit()
            return redirect(url_for("show"))

    return render_template("show/create.html", form=form)


@app.route("/show/delete/<uuid>", methods=["POST"])
def delete_car(uuid):
    car = CarsTable.query.filter(CarsTable.Car_id == uuid).first()
    if car:
        db.session.delete(car)
        db.session.commit()

    return redirect(url_for("show"))


@app.route("/show/<uuid>", methods=["GET", "POST"])
def update_car(uuid):
    car = CarsTable.query.filter(CarsTable.Car_id == uuid).first()
    form = car.filled_form()
    form.Student_name.choices = [
        (str(student.Student_card), f"{student.Student_name} {student.Student_surname}") for student in
        StudentTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("show/update.html", form=form)

        car.map_to_form(form)
        db.session.commit()
        return redirect(url_for("show"))

    return render_template("show/update.html", form=form)


@app.route("/bar", methods=["GET"])
def visualization():
    data = visualization_data()

    return render_template("bar.html", students_cars=data)


if __name__ == "__main__":
    app.run(debug=True)
