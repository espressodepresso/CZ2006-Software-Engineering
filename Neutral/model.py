from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, Column, Float, DateTime
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Neutral import db, login_manager, app
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model): #User info
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Unicode(50), unique = True, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    image = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    healthGoal = db.Column(db.String(120), nullable = False, default = 'Lose 0.5kg in a week')
    FoodRecord = db.relationship("FoodRecord", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)
    WorkoutRecord = db.relationship("WorkoutRecord", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)
    Workout = db.relationship("Workout", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)
    Exercise = db.relationship("Exercise", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)
    Set = db.relationship("Set", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)
    Rep = db.relationship("Rep", backref="User", cascade="all, delete, delete-orphan", passive_deletes=True)

class FoodDB(db.Model): #from food API
    __tablename__ = 'FoodDB'
    food_id = db.Column(db.Integer, primary_key = True)
    food_name = db.Column(db.String(1000), nullable = False)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_fibres = db.Column(db.Float, nullable = False)
    food_saturatedfat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)
    FoodRecord = db.relationship("FoodRecord", backref="FoodDB", cascade="all, delete, delete-orphan", passive_deletes=True)

class FoodRecord(db.Model): #a food record that user eat
    __tablename__ = 'FoodRecord'
    foodrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False)
    foodrecord_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    foodrecord_meal = db.Column(db.String(20), nullable = False, default = 'Breakfast')
    food_id = db.Column(db.Integer, db.ForeignKey('FoodDB.food_id', ondelete='CASCADE'), nullable = False, primary_key = True)
    food_name = db.Column(db.String(1000), nullable = False)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_fibres = db.Column(db.Float, nullable = False)
    food_saturatedfat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)

class ExerciseDB(db.Model): # from exercise API
    __tablename__ = 'ExerciseDB'
    exercise_id = db.Column(db.Integer, primary_key = True)
    exercise_name = db.Column(db.String(100), nullable = False)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_img = db.Column(db.String(1000000), nullable = False)
    exercise_category_primary = db.Column(db.String(1000000), nullable = False)
    exercise_category_secondary = db.Column(db.String(1000000), nullable = True)
    Exercise = db.relationship("Exercise", backref="ExerciseDB", cascade="all, delete", passive_deletes=True)
    Set = db.relationship("Set", backref="ExerciseDB", cascade="all, delete, delete-orphan", passive_deletes=True)
    Rep = db.relationship("Rep", backref="ExerciseDB", cascade="all, delete, delete-orphan", passive_deletes=True)

class WorkoutRecord(db.Model):#workout that user is supposed to do that day
    __tablename__ = 'WorkoutRecord'
    workoutrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False)
    workoutrecord_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    Workout = db.relationship("Workout", backref="WorkoutRecord", cascade="all, delete, delete-orphan", passive_deletes=True)
    Exercise = db.relationship("Exercise", backref="WorkoutRecord", cascade="all, delete, delete-orphan", passive_deletes=True)
    Set = db.relationship("Set", backref="WorkoutRecord", cascade="all, delete, delete-orphan", passive_deletes=True)
    Rep = db.relationship("Rep", backref="WorkoutRecord", cascade="all, delete, delete-orphan", passive_deletes=True)

class Workout(db.Model):#one workout of user
    __tablename__ = 'Workout'
    workout_id = db.Column(db.Integer, primary_key = True)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id', ondelete='CASCADE'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False)
    workout_name = db.Column(db.String(50), nullable = False)
    Exercise = db.relationship("Exercise", backref="Workout", cascade="all, delete, delete-orphan", passive_deletes=True)
    Set = db.relationship("Set", backref="Workout", cascade="all, delete, delete-orphan", passive_deletes=True)
    Rep = db.relationship("Rep", backref="Workout", cascade="all, delete, delete-orphan", passive_deletes=True)

class Exercise(db.Model):#one exercise in workout
    __tablename__ = 'Exercise'
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id', ondelete='CASCADE'), nullable = False, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id', ondelete='CASCADE'), nullable = False, primary_key=True)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id', ondelete='CASCADE'), nullable = False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable = False)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_img = db.Column(db.String(1000000), nullable = False)
    exercise_category_primary = db.Column(db.String(1000000), nullable = False)
    exercise_category_secondary = db.Column(db.String(1000000), nullable = True)
    exercise_caloriesburnt = db.Column(db.Float, nullable = False)
    status = db.Column(db.Boolean, nullable = False, default = False)

class Set(db.Model):#one set in exercise
    __tablename__ = 'Set'
    set_id = db.Column(db.Integer, primary_key = True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id', ondelete='CASCADE'), nullable = False)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id', ondelete='CASCADE'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False)
    set_count = db.Column(db.Integer, nullable = False)
    Rep = db.relationship("Rep", backref="Set", cascade="all, delete, delete-orphan", passive_deletes=True)


class Rep(db.Model):#one in set
    __tablename__ = 'Rep'
    rep_id = db.Column(db.Integer, primary_key = True)
    set_id = db.Column(db.Integer, db.ForeignKey('Set.set_id', ondelete='CASCADE'), nullable = False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id', ondelete='CASCADE'), nullable = False)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id', ondelete='CASCADE'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id', ondelete='CASCADE'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable = False)
    rep_count = db.Column(db.Integer, nullable = False)
    rep_unit = db.Column(db.String(20), nullable = False)#e.g. 50 kg, kg is the desc
    rep_desc = db.Column(db.String(20), nullable = False) #e.g. 50kg, 50 is the desc

