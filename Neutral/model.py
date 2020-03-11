from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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
    

class FoodDB(db.Model): #from food API
    __tablename__ = 'FoodDB'
    food_id = db.Column(db.Integer, primary_key = True)
    food_name = db.Column(db.String(50), nullable = False, unique = True)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)

class FoodRecord(db.Model): #a food record that user eat
    __tablename__ = 'FoodRecord'
    foodrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    foodrecord_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    foodrecord_meal = db.Column(db.String(20), nullable = False, default = 'Breakfast')
    user = db.relationship("User")

class Food(db.Model): #individual food eaten by user
    __tablename__ = 'Food'
    food_id = db.Column(db.Integer, db.ForeignKey('FoodDB.food_id'), nullable = False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False, primary_key=True)
    foodrecord_id = db.Column(db.Integer, db.ForeignKey('FoodRecord.foodrecord_id'), nullable = False, primary_key=True)
    food_name = db.Column(db.Float, nullable = False)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)
    fooddb = db.relationship("FoodDB")
    user = db.relationship("User")
    foodrecord = db.relationship("FoodRecord")

class ExerciseDB(db.Model): # from exercise API
    __tablename__ = 'ExerciseDB'
    exercise_id = db.Column(db.Integer, primary_key = True)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_caloriesburnt = db.Column(db.Float, nullable = False)

class WorkoutRecord(db.Model):#workout that user is supposed to do that day
    __tablename__ = 'WorkoutRecord'
    workoutrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    workoutrecord_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    User = db.relationship("User")

class Workout(db.Model):#one workout of user
    __tablename__ = 'Workout'
    workout_id = db.Column(db.Integer, primary_key = True)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    workout_name = db.Column(db.String(50), nullable = False)
    workoutrecord = db.relationship("WorkoutRecord")
    user = db.relationship("User")

class Exercise(db.Model):#one exercise in workout
    __tablename__ = 'Exercise'
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id'), nullable = False, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id'), nullable = False, primary_key=True)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False, primary_key=True)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_caloriesburnt = db.Column(db.Float, nullable = False)
    status = db.Column(db.Boolean, nullable = False, default = False)
    exercisedb = db.relationship("ExerciseDB")
    workout = db.relationship("Workout")
    workoutrecord = db.relationship("WorkoutRecord")
    user = db.relationship("User")

class Set(db.Model):#one set in exercise
    __tablename__ = 'Set'
    set_id = db.Column(db.Integer, primary_key = True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id'), nullable = False)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    set_count = db.Column(db.Integer, nullable = False)
    exercisedb = db.relationship("ExerciseDB")
    workout = db.relationship("Workout")
    workoutrecord = db.relationship("WorkoutRecord")
    user = db.relationship("User")

class Rep(db.Model):#one in set
    __tablename__ = 'Rep'
    rep_id = db.Column(db.Integer, primary_key = True)
    set_id = db.Column(db.Integer, db.ForeignKey('Set.set_id'), nullable = False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id'), nullable = False)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    rep_count = db.Column(db.Integer, nullable = False)
    rep_unit = db.Column(db.String(20), nullable = False)#e.g. 50 kg, kg is the desc
    rep_desc = db.Column(db.String(20), nullable = False) #e.g. 50kg, 50 is the desc
    Set = db.relationship("Set")
    exercisedb = db.relationship("ExerciseDB")
    workout = db.relationship("Workout")
    workoutrecord = db.relationship("WorkoutRecord")
    user = db.relationship("User")
