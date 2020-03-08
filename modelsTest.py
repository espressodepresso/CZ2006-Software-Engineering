from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yeehaw.db'
db = SQLAlchemy(app)   


@app.route('/', methods=['POST', 'GET'])
def display():
    return render_template('display.html')
