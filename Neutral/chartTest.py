from flask import Flask, Markup, render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy

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
    def __repr__(self):
        return '<User %r>' % self.user_id


@app.route('/breakdown',methods=['POST','GET'])
def breakdown():
    MealData = [20,40,30,10]
    MealLabels = ['Breakfast', 'Lunch', 'Dinner','Snacks']
    NutritionData =[30,30,40]
    NutritionLabels = ['Carbohydrates','Protein','Fats']
    date='Wednesday, 25 Feb 2020'
    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'Nutrients' in request.form["action"]:
            return render_template('dataBreakdowns.html', values=NutritionData,labels=NutritionLabels, date=date,header='Nutrients')
        elif 'Calories' in request.form["action"]:
            return render_template('dataBreakdowns.html', values=MealData, labels=MealLabels, date=date,header='Calories')
    else:
        return render_template('dataBreakdowns.html', values=NutritionData, labels=NutritionLabels, date=date, header='Nutrients')    

@app.route('/',methods=['POST','GET'])
def nav(): 
    #test_user = User.query.filter(User.username=="test").all()
    #print(type(test_user))
    summary_data=[542,1360]
    exercise_data=[838,400,438]
    values=[80.0,79.0,79.0,77.5,78.0,77.0,77.5]
    return render_template('homepage.html',  data1=summary_data, data2=exercise_data, values=values)


if __name__ == '__main__':
    app.run(debug=True)