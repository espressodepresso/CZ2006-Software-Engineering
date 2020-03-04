#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Neutral import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable = False)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password_hash = db.Column(db.Unicode(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False) 
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    #healthGoal = 

    #def __repr__(self):
    #    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Workout(db.Model): #stores workouts for each day
    wid = db.Column(db.Integer, primary_key=True)
    date_of_workout = db.Column(db.DateTime, nullable = False, default = datetime.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = 'Not Completed')
    #notes = db.Column(db.Text, nullable = False)

#take from api
class Exercises(db.Model): #all exercises
    esid = db.Column(db.Integer, primary_key=True) 
    exercise_name = db.Column(db.String(50), nullable = False)
    #????

class Exercise(db.Model): # store exercises that are in the workout
    eid = db.Column(db.Integer, primary_key=True) 
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.wid'))
    order_of_exercises = db.Column(db.Integer, unique = True, nullable = False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.esid'))

class Set(db.Model): #shows how many sets of an exercise
    sid = db.Column(db.Integer, primary_key=True) 
    order_of_sets = db.Column(db.Integer, unique = True, nullable = False)
    weight = db.Column(db.Numeric)
    units = db.Column(db.String(6), nullable = False)
    reps = db.Column(db.Integer, nullable = False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.eid'), nullable = False)

class Food(db.Model): #all Food
    fid = db.Column(db.Integer, primary_key=True) 
    food_name = db.Column(db.String(50), nullable = False)
    serving_size = db.Column(db.Float, nullable = False)
    calories = db.Column(db.Float, nullable = False)
    protein = db.Column(db.Float, nullable = False)
    carbo = db.Column(db.Float, nullable = False)
    fat = db.Column(db.Float, nullable = False)
    fibre = db.Column(db.Float, nullable = False)
    sodium = db.Column(db.Float, nullable = False)
    #???

class FoodRecord(db.Model): #stores food for each day
    frid = db.Column(db.Integer, primary_key=True)
    date_of_foodrecord = db.Column(db.DateTime, nullable = False, default = datetime.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    weight = db.Column(db.Float, nullable = False)
    calories = db.Column(db.Float, nullable = False)
    protein = db.Column(db.Float, nullable = False)
    carbo = db.Column(db.Float, nullable = False)
    fat = db.Column(db.Float, nullable = False)
    fibre = db.Column(db.Float, nullable = False)
    sodium = db.Column(db.Float, nullable = False)
    #notes = db.Column(db.Text, nullable = False)


