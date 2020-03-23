import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, Column, Float, DateTime
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '1e730902dd46e15ee749c371b91cb549'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cz2006software@gmail.com'
app.config['MAIL_PASSWORD'] = 'SoftwareT3sting'
mail = Mail(app)


from Neutral import routing