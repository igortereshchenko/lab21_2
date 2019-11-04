from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from uuid import uuid4
from datetime import datetime
from views import SkillForm

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "Users"

    Username = db.Column("username", db.String, primary_key=True)
    Password = db.Column("password", db.String, nullable=False)


class Skills(db.Model):
    __tablename__ = "Skills"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    Vacancy = db.Column("vacancy", db.String)
    CreationDate = db.Column("creationDate", db.TIMESTAMP, default=datetime.now)
    RemoveDate = db.Column("removeDate", db.TIMESTAMP)

    UsernameFk = db.Column("usernameFk", db.String, db.ForeignKey("Users.username"), nullable=False)
    Users = db.relationship("Users", backref=backref('Skills', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return SkillForm(
            Name=self.Name,
            Vacancy=self.Vacancy,
            CreationDate=self.CreationDate,
            RemoveDate=self.RemoveDate
        )

    def map_from(self, form):
        self.Name = form.Name.data
        self.Vacancy = form.Vacancy.data
        self.CreationDate = form.CreationDate.data
        self.RemoveDate = form.RemoveDate.data
