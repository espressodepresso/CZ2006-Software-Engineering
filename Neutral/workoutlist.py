import sqlalchemy
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from Neutral.model import ExerciseDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

def PrimaryexerciseList():
    priexercises_list =list()
    for exercises in db.session.query(ExerciseDB.exercise_category_primary).distinct():
        priexercises_list.append(exercises)
    return priexercises_list

def ChestList():
    chestlist=list()
    alllist = select([ExerciseDB.exercise_name]).where(ExerciseDB.exercise_category_primary == "chest")
    for row in db.session.execute(alllist):
        chestlist.append(row)
    return chestlist

def TricepsList():
    tlist=list()
    alllist = select([ExerciseDB.exercise_name]).where(ExerciseDB.exercise_category_primary == "triceps")
    for row in db.session.execute(alllist):
        tlist.append(row)
    return tlist


