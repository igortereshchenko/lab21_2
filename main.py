from flask import Flask, render_template, request, redirect, url_for

from dao.orm.entities import *
from forms.discipline_form import DisciplineForm
from forms.student_form import StudentForm
from forms.teacher_form import TeacherForm

from dao.db import PostgresDb
app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

@app.route('/ai', methods=['GET'])
def ai():
    skill_obj = Skill(
        student_name='Mozgovoy Nikita',
        student_group = 61,
        name = 'OOP basic',
        type = 'OOP',
        vacancy = 'C++ developer',
        creation_date = '2019-06-22 19:10:25-07'
    )
    db = PostgresDb()
    db.sqlalchemy_session.add(skill_obj)
    db.sqlalchemy_session.commit()
    return render_template('index.html')

# @app.route('/show',methods=['GET'])
# def show():
#     db = PostgresDb()
#
#     result = db.sqlalchemy_session.query(Result).all()
#
#     return render_template('result.html', results=result)

@app.route('/teacher', methods=['GET'])
def index_teacher():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).all()

    return render_template('teacher.html', teachers=result)


@app.route('/new_teacher', methods=['GET', 'POST'])
def new_teacher():
    form = TeacherForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")
        else:
            teacher_obj = Teacher(
                name=form.name.data,
                degree=form.degree.data
            )
            db = PostgresDb()
            db.sqlalchemy_session.add(teacher_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))

    return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")


@app.route('/edit_teacher', methods=['GET', 'POST'])
def edit_teacher():
    form = TeacherForm()

    if request.method == 'GET':

        name = request.args.get('name')
        db = PostgresDb()
        teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == name).one()

        # fill form and send to user
        form.name.data = teacher_obj.name
        form.degree.data = teacher_obj.degree
        form.old_name.data = teacher_obj.name
        return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")

    else:
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="Edit teacher",
                                   action="edit_teacher")
        else:
            db = PostgresDb()
            # find professor

            teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == form.old_name.data).one()

            # update fields from form data
            teacher_obj.name = form.name.data
            teacher_obj.degree = form.degree.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))


@app.route('/delete_teacher')
def delete_teacher():
    name = request.args.get('name')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_teacher'))


# END PROFESSOR ORIENTED QUERIES --------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/student', methods=['GET'])
def index_student():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Student).all()

    return render_template('student.html', students=result)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            student_obj = Student(
                name=form.name.data,
                sgroup=form.group.data
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()

    if request.method == 'GET':

        name, group = request.args.get('name'), int(request.args.get('group'))
        db = PostgresDb()
        student = db.sqlalchemy_session.query(Student).filter(Student.name == name, Student.sgroup == group).one()

        # fill form and send to student
        form.name.data = student.name
        form.group.data = student.sgroup
        form.old_name.data = student.name
        form.old_group.data = student.sgroup
        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

    else:

        if not form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            db = PostgresDb()
            # find student
            student = db.sqlalchemy_session.query(Student).filter(Student.name == form.old_name.data,
                                                                  Student.sgroup == form.old_group.data).one()

            # update fields from form data
            student.name = form.name.data
            student.sgroup = form.group.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    name, group = request.args.get('name'), int(request.args.get('group'))

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Student).filter(Student.name == name, Student.sgroup == group).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_student'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# DISCIPLINE ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/discipline', methods=['GET'])
def index_discipline():
    db = PostgresDb()

    discipline = db.sqlalchemy_session.query(Discipline).all()

    return render_template('discipline.html', disciplines=discipline)


@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    form = DisciplineForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="New discipline",
                                   action="new_discipline")
        else:
            discipline_obj = Discipline(
                name=form.name.data,
                teacher_name=form.teacher_name.data
            )

            db = PostgresDb()

            a = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == form.teacher_name.data).all()
            if not a:
                return render_template('discipline_form.html', form=form, form_name="New discipline",
                                       action="new_discipline")
            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    form = DisciplineForm()

    if request.method == 'GET':
        name = request.args.get('name')

        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        discipline = db.sqlalchemy_session.query(Discipline).filter(
            Discipline.name == name).one()

        a = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == discipline.teacher_name).all()
        if not a:
            return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                   action="edit_discipline")
        # fill form and send to discipline
        form.teacher_name.data = discipline.teacher_name
        form.name.data = discipline.name
        form.old_name.data = discipline.name
        return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

    else:

        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                   action="edit_discipline")
        else:
            db = PostgresDb()
            # find discipline
            discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.name == form.old_name.data,).one()

            # update fields from form data
            discipline.name = form.name.data
            discipline.teacher_name = form.teacher_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    name = request.args.get('name')
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Discipline).filter(
        Discipline.name == name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_discipline'))


# END DISCIPLINE ORIENTED QUERIES -----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
