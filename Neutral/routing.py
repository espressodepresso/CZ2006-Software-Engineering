from flask import render_template, url_for, flash, redirect,request
from Neutral import app
from Neutral.foodreco import RecommendationManager



@app.route('/')
def helloworld():
    return 'Hello world'
@app.route('/foodreco',methods=['POST','GET'])
def displayFoodReco():
    names_list = RecommendationManager.readCSV('userselectiondata.csv')
    if request.method == 'POST':
        userLikes = (request.form.getlist('mycheckbox'))
        RecommendationManager.writeUserLikesCSV(userLikes,'userselectiondata.csv')
        recommendedFoodList = RecommendationManager.recommendFood()
        return render_template('foodrecoresults.html',food_list= recommendedFoodList)
    return render_template('foodreco.html',names_list=names_list)

