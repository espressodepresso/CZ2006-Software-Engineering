#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Neutral import db

class User(db.Model): #User info
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
    food_id = db.Column(db.Integer, primary_key = True)
    food_name = db.Column(db.String(50), nullable = False, unique = True)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)

class FoodRecord(db.Model): #a food record that user eat
    foodrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    foodrecord_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    foodrecord_meal = db.Column(db.String(20), nullable = False, default = 'Breakfast')

class Food(db.Model): #individual food eaten by user
    food_id = db.Column(db.Integer, db.ForeignKey('FoodDB.food_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    foodrecord_id = db.Column(db.Integer, db.ForeignKey('FoodRecord.foodrecord_id'), nullable = False)
    food_name = db.Column(db.Float, nullable = False)
    food_calories = db.Column(db.Float, nullable = False)
    food_protein = db.Column(db.Float, nullable = False)
    food_carb = db.Column(db.Float, nullable = False)
    food_fat = db.Column(db.Float, nullable = False)
    food_sodium = db.Column(db.Float, nullable = False)
    serving_size = db.Column(db.Float, nullable = False)

class ExerciseDB(db.Model): # from exercise API
    exercise_id = db.Column(db.Integer, primary_key = True)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_caloriesburnt = db.Column(db.Float, nullable = False)

class WorkoutRecord(db.Model):#workout that user is supposed to do that day
    workoutrecord_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    workoutrecord_date = b.Column(db.DateTime, nullable = False, default = datetime.now())

class Workout(db.Model):#one workout of user
    workout_id = db.Column(db.Integer, primary_key = True)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    workout_name = db.Column(db.String(50), nullable = False)

class Exercise(db.Model):#one exercise in workout
    exercise_id = db.Column(db.Integer, db.ForeignKey('ExerciseDB.exercise_id'), nullable = False)
    workout_id = db.Column(db.Integer, db.ForeignKey('Workout.workout_id'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    exercise_desc = db.Column(db.String(1000000), nullable = False)
    exercise_caloriesburnt = db.Column(db.Float, nullable = False)
    status = db.Column(db.Boolean, nullable = False, default = False)

class Set(db.Model):#one set in exercise
    set_id = db.Column(db.Integer, primary_key = True)
    exercise_id = db.Column(db.Integer, ForeignKey('ExerciseDB.exercise_id'), nullable = False)
    workout_id = db.Column(db.Integer, ForeignKey('Workout.workout_id'), nullable = False)
    workoutrecord_id = db.column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    set_count = db.column(db.Integer, nullable = False)

class Rep(db.Model):#one in set
    rep_id = db.Column(db.Integer, primary_key = True)
    set_id = db.Column(db.Integer, ForeignKey('Set.set_id'), nullable = False)
    exercise_id = db.Column(db.Integer, ForeignKey('ExerciseDB.exercise_id'), nullable = False)
    workout_id = db.Column(db.Integer, ForeignKey('Workout.workout_id'), nullable = False)
    workoutrecord_id = db.Column(db.Integer, db.ForeignKey('WorkoutRecord.workoutrecord_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    rep_count = db.Column(db.Integer, nullable = False)
    rep_unit = db.Coloumn(db.String(20), nullable = False)#e.g. 50 kg, kg is the desc
    rep_desc = db.Column(db.String(20), nullable = False) #e.g. 50kg, 50 is the desc
