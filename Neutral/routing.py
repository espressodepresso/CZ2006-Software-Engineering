from flask import render_template, url_for, flash, redirect,request
from Neutral import app
from Neutral.foodreco import RecommendationManager
from Neutral.forms import searchForm
from Neutral.model import FoodRecord
from Neutral.model import FoodDB
from Neutral.entity import Food1

@app.route('/')
def helloworld():
    return 'Hello world'

# @app.route('/foodreco',methods=['POST','GET'])
# def displayFoodReco():
#     names_list = RecommendationManager.readCSV('userselectiondata.csv')
#     if request.method == 'POST':
#         userLikes = (request.form.getlist('mycheckbox'))
#         RecommendationManager.writeUserLikesCSV(userLikes,'userselectiondata.csv')
#         recommendedFoodList = RecommendationManager.recommendFood()
#         return render_template('foodrecoresults.html',food_list= recommendedFoodList)
#     return render_template('foodreco.html',names_list=names_list)


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
    food_list_breakfast = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Breakfast'), FoodRecord.user_id == 1).all()
    food_list_lunch = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Lunch'), FoodRecord.user_id == 1).all()
    food_list_dinner = FoodRecord.query.filter(FoodRecord.foodrecord_meal.contains('Dinner'), FoodRecord.user_id == 1).all()
    return render_template('foodRecord.html', food_list_breakfast = food_list_breakfast, food_list_lunch = food_list_lunch, food_list_dinner = food_list_dinner)


@app.route('/addFoodRecord', methods=['GET', 'POST'])
def displayaddFoodRecord():
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
            
        return render_template('addFoodRecord.html', form=form,foodList=food_item_list)
