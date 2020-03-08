from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.templating import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myat secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/')
def charts():
    NutritionData =[30,30,40]
    CalorieData = [17,35,27,11]
    return render_template('login.html', data1= CalorieData, data2=NutritionData)

if __name__ == "__main__":
    app.run(debug=True)