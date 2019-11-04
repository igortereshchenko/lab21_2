from flask import Flask, render_template, request, redirect, url_for
from models import db, Skills, Users
from visualization import visualization_data
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  "postgresql://postgres:140599Artem@127.0.0.1:5432/lab2")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    return "Database created"


@app.route("/map")
def insert():
    db.session.add(Skills(Name="C++", Vacancy="C++ developer", UsernameFk="artemkovtun"))
    db.session.add(Skills(Name="Excel", Vacancy="Manager", UsernameFk="test"))
    db.session.add(Skills(Name="Azure", Vacancy="Cloud master", UsernameFk="test"))
    db.session.commit()
    return "Data inserted"


@app.route("/get")
def get():
    skills = Skills.query.all()
    return render_template("table.html", skills=skills)


@app.route("/update/<uuid>", methods=["GET", "POST"])
def update(uuid):
    schema = Skills.query.filter(Skills.Id == uuid).first()
    form = schema.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("update.html", form=form)

        schema.map_from(form)
        db.session.commit()
        return redirect(url_for("get"))

    return render_template("update.html", form=form)


@app.route("/bar", methods=["GET"])
def visualization():
    data = visualization_data()

    return render_template("visualization.html", user_skills_bar=data)


if __name__ == "__main__":
    app.run(debug=True)
