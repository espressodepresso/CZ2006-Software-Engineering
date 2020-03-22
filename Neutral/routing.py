import secrets
from datetime import datetime
from PIL import Image
import os
from flask import render_template, url_for, flash, redirect,request
from Neutral import app, db, bcrypt, mail
from Neutral.foodreco import RecommendationManager
from Neutral.model import FoodRecord,FoodDB,db,ExerciseDB,User
from Neutral.entity import Food1
from Neutral.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, searchForm, dateForm
from Neutral.workoutlist import ChestList, TricepsList, PrimaryexerciseList
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import func, update, delete


@app.route('/')  # what we write in the browser - route to home page
@app.route('/home')
def home():
    summary_data=[542,1360]
    exercise_data=[838,400,438]
    values=[80.0,79.0,79.0,77.5,78.0,77.0,77.5]
    return render_template('home.html',  data1=summary_data, data2=exercise_data, values=values)
    
@app.route('/foodreco',methods=['POST','GET'])
def displayFoodReco():
    names_list = RecommendationManager.readCSV('userselectiondata.csv')
    if request.method == 'POST':
        userLikes = (request.form.getlist('mycheckbox'))
        RecommendationManager.writeUserLikesCSV(userLikes,'userselectiondata.csv')
        recommendedFoodList = RecommendationManager.recommendFood()
        return render_template('foodrecoresults.html',food_list= recommendedFoodList)
    return render_template('foodreco.html',names_list=names_list)


@app.route('/searchfood', methods=['GET', 'POST'])
def displaySearchFood():
    food_item_list = []
    form = searchForm(request.form)
    if request.method == 'POST' and form.validate():
        foodToBeSearched = form.foodname.data
        # convert user entered data into lowercase
        editedfoodToBeSearched = foodToBeSearched.lower()
        # find in FoodDB
        results = FoodDB.query.filter(FoodDB.food_name.contains(editedfoodToBeSearched)).all()

        if results is not None:
            for result in results:
                splitted_result = result.food_name.split(", ")
                # only display the result if first word of the food name contains the searched food name
                if editedfoodToBeSearched in splitted_result[0]:
                    # create a food object from entity.py
                    food_item = Food1(result.food_id,result.food_name,round(result.food_calories,2),round(result.food_protein,2),round(result.food_carb,2),round(result.food_fat,2),round(result.food_fibres,2),round(result.food_saturatedfat,2),round(result.food_sodium,2))
                    food_item_list.append(food_item)
    return render_template('searchFood.html', form=form,foodList=food_item_list)


@app.route('/foodRecord', methods=['GET', 'POST'])
def displayFoodRecord():
    
    form = dateForm(request.form)
    breakfast = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Breakfast'), FoodRecord.user_id == 1).all()
    lunch = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Lunch'), FoodRecord.user_id == 1).all()
    dinner = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Dinner'), FoodRecord.user_id == 1).all()
    snack = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Snack'), FoodRecord.user_id == 1).all()
    
    food_list_breakfast = []
    food_list_lunch = []
    food_list_dinner = []
    food_list_snack = []

    if request.method == 'POST' and form.validate():
        dateToBeSearched = form.fooddate.data
    else:
        dateToBeSearched = datetime.now().date()
    for i in breakfast:
        print(i.foodrecord_date)
        if i.foodrecord_date.date() == dateToBeSearched:
            food_list_breakfast.append(i);
    for i in lunch:
        if i.foodrecord_date.date() == dateToBeSearched:
            food_list_lunch.append(i);
    for i in dinner:
        if i.foodrecord_date.date() == dateToBeSearched:
            food_list_dinner.append(i);
    for i in snack:
        if i.foodrecord_date.date() == dateToBeSearched:
            food_list_snack.append(i);        
    return render_template('foodRecord.html', form = form, food_list_breakfast = food_list_breakfast, food_list_lunch = food_list_lunch, food_list_dinner = food_list_dinner, food_list_snack=food_list_snack)


@app.route('/addFoodRecord/<meal>', methods=['GET', 'POST'])
def displayaddFoodRecord(meal):
    food_item_list = []
    form = searchForm(request.form)
    if request.method == 'POST' and form.validate():
            foodToBeSearched = form.foodname.data
            # convert user entered data into lowercase
            editedfoodToBeSearched = foodToBeSearched.lower()
            # find in FoodDB
            results = FoodDB.query.filter(FoodDB.food_name.contains(editedfoodToBeSearched)).all()

            if results is not None:
                for result in results:
                    splitted_result = result.food_name.split(", ")
                    # only display the result if first word of the food name contains the searched food name
                    if editedfoodToBeSearched in splitted_result[0]:
                        # create a food object from entity.py
                        food_item = Food1(result.food_id,result.food_name,round(result.food_calories,2),round(result.food_protein,2),round(result.food_carb,2),round(result.food_fat,2),round(result.food_fibres,2),round(result.food_saturatedfat,2),round(result.food_sodium,2))
                        food_item_list.append(food_item)
            
    return render_template('addFoodRecord.html', form=form, foodList=food_item_list, meal=meal)

@app.route("/addfoodprocess/<food_name>/<food_calories>/<food_carb>/<food_fat>/<food_saturatedfat>/<food_protein>/<food_sodium>/<food_fibres>/<food_meal>", methods=['GET', 'POST'])
def addfood(food_name,food_calories,food_carb,food_fat,food_saturatedfat,food_protein,food_sodium,food_fibres,food_meal):
    food_calories = float(food_calories)
    food_carb = float(food_carb)
    food_fat = float(food_fat)
    food_saturatedfat = float(food_saturatedfat)
    food_protein = float(food_protein)
    food_sodium = float(food_sodium)
    food_fibres = float(food_fibres)
    maxid = db.session.query(func.max(FoodRecord.foodrecord_id)).scalar()
    maxid = maxid + 1
    food= FoodDB.query.filter(FoodDB.food_name.contains(food_name)).one()
    food_id = food.food_id
    fr = FoodRecord(serving_size = 1, foodrecord_id =maxid, user_id = 1, food_id = food_id, food_name = food_name, food_calories = food_calories, food_carb = food_carb, food_fat = food_fat, food_saturatedfat= food_saturatedfat, food_protein = food_protein, food_sodium = food_sodium, food_fibres = food_fibres, foodrecord_meal = food_meal)
    db.session.add(fr)
    db.session.commit()
    return redirect(url_for('displayFoodRecord'))

@app.route("/editfoodrecord/<id>/<calories>/<carb>/<fat>/<sat>/<protein>/<sodium>/<fibres>", methods=['GET','POST'])
def editfoodrecord(id,calories,carb,fat,sat,protein,sodium,fibres):
    user_id = 1
    calories = float(calories)
    carb = float(carb)
    fat = float(fat)
    sat = float(sat)
    protein = float(protein)
    sodium = float(sodium)
    fibres = float(fibres)

    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_calories: calories})
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_carb:carb})
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_fat:fat })
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_saturatedfat:sat })
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_protein:protein })
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_sodium:sodium })
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id, FoodRecord.user_id == user_id).update({FoodRecord.food_fibres:fibres })
    db.session.commit()

    return redirect(url_for('displayFoodRecord'))

@app.route("/deletefoodrecord/<id>", methods=['GET','POST'])
def deletefoodrecord(id):
    db.session.query(FoodRecord).filter(FoodRecord.foodrecord_id == id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('displayFoodRecord'))

@app.route("/quickaddfoodprocess/<food_name>/<food_calories>/<food_carb>/<food_fat>/<food_saturatedfat>/<food_protein>/<food_sodium>/<food_fibres>/<food_meal>", methods=['GET', 'POST'])
def quickaddfood(food_name,food_calories,food_carb,food_fat,food_saturatedfat,food_protein,food_sodium,food_fibres,food_meal):
    food_calories = float(food_calories)
    food_carb = float(food_carb)
    food_fat = float(food_fat)
    food_saturatedfat = float(food_saturatedfat)
    food_protein = float(food_protein)
    food_sodium = float(food_sodium)
    food_fibres = float(food_fibres)
    maxrecordid = db.session.query(func.max(FoodRecord.foodrecord_id)).scalar()
    maxrecordid = maxrecordid + 1
    maxfoodid = db.session.query(func.max(FoodDB.food_id)).scalar()
    maxfoodid = maxfoodid + 1

    fooddb = FoodDB(food_id=maxfoodid, food_name=food_name, food_calories = food_calories, food_protein= food_protein, food_carb = food_carb, food_fat=food_fat,food_fibres=food_fibres, food_saturatedfat=food_saturatedfat, food_sodium=food_sodium,serving_size=1)
    fr = FoodRecord(serving_size = 1, foodrecord_id =maxrecordid, user_id = 1, food_id = maxfoodid, food_name = food_name, food_calories = food_calories, food_carb = food_carb, food_fat = food_fat, food_saturatedfat= food_saturatedfat, food_protein = food_protein, food_sodium = food_sodium, food_fibres = food_fibres, foodrecord_meal = food_meal)
    db.session.add(fr)
    db.session.add(fooddb)
    db.session.commit()
    return redirect(url_for('displayFoodRecord'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, 
                    password=hashed_pw,
                    age=form.age.data,
                    height=form.height.data,
                    weight=form.weight.data,
                    healthGoal=form.healthGoal.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to login.',
              'success')  # message, category of message
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.age = form.age.data
            current_user.height = form.height.data
            current_user.weight = form.weight.data
            current_user.healthGoal = form.healthGoal.data
            current_user.password = form.password.data
            db.session.commit()
            flash('Your Account has been updated!', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.healthGoal.data = current_user.healthGoal
        form.password.data = current_user.password
        image = url_for(
        'static', filename='profile_pics/' + current_user.image)

    return render_template('account.html', title='Account', image=image, form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): #enter email to request password reset
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset password', form = form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token. Please enter your email again.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/diary',methods=['POST','GET'])
def diary():
    MealData = [20,40,30,10]
    MealLabels = ['Breakfast', 'Lunch', 'Dinner','Snacks']
    for i in range(len(MealLabels)):
        MealLabels[i] = MealLabels[i] + ' ' + str(MealData[i]) +'%'
    NutritionData =[30,30,40]
    NutritionLabels = ['Carbohydrates','Protein','Fats']
    for i in range(len(NutritionLabels)):
        NutritionLabels[i] = NutritionLabels[i] + ' ' + str(NutritionData[i]) +'%'
    date='Wednesday, 25 Feb 2020'
    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'Nutrients' in request.form["action"]:
            return render_template('diary.html', values=NutritionData,labels=NutritionLabels, date=date,header='Nutrients')
        elif 'Calories' in request.form["action"]:
            return render_template('diary.html', values=MealData, labels=MealLabels, date=date,header='Calories')
    else:
        return render_template('diary.html', values=NutritionData, labels=NutritionLabels, date=date, header='Nutrients')    

@app.route("/workoutlist")
def addexercises():
    raw_data_1 = PrimaryexerciseList()
    priexercises1 = [item[0] for item in raw_data_1]
    raw_data_2 = ChestList()
    clist = [item[0] for item in raw_data_2]
    raw_data_3 = TricepsList()
    tlist = [item[0] for item in raw_data_3]
    return render_template('workoutlist.html', title='Workout List', exercisedb=priexercises1, chestlist=clist, tricepslist=tlist)