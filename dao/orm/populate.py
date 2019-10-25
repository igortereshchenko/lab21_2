from dao.db import PostgresDb
from dao.orm.entities import *

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

# clear all tables in right order
# session.query(OrmFileEditor).delete()
# session.query(OrmFile).delete()
# session.query(OrmUser).delete()

# populate database with new rows

nau = Discipline(discipline_university='nau',
                 discipline_faculty='pp',
                 discipline_name='Mat Analise',
                 discipline_exam=True,
                 discipline_hours_for_semester=10)

# insert into database
session.add_all([nau])

session.commit()
