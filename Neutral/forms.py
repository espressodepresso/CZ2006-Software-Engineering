from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import Form,StringField,validators
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, FloatField, SelectField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Neutral.model import User


class searchForm(Form):
    foodname = StringField('Search Food',validators=[InputRequired()])

class dateForm(Form):
    fooddate = DateField('Select Food Record Date', validators=[InputRequired()], format='%Y-%m-%d')

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                              validators=[DataRequired()])  
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  EqualTo('password')])

    healthGoal = SelectField(label='Health Goals', choices=[('Maintain Weight', 'Maintain Weight'),('Lose 0.5Kg in a week', 'Lose 0.5Kg in a week'), ('Lose 1.0Kg in a week', 'Lose 1.0Kg in a week'), ('Lose 1.5Kg in a week', 'Lose 1.5Kg in a week'), ('Lose 2.0Kg in a week', 'Lose 2.0Kg in a week')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different username')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                              validators=[DataRequired()])  
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    age = IntegerField('Age', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    password = PasswordField('Password',
                              validators=[DataRequired()],widget=PasswordInput(hide_value=False))  
    healthGoal = SelectField(label='Health Goals', choices=[('Maintain Weight', 'Maintain Weight'),('Lose 0.5Kg in a week', 'Lose 0.5Kg in a week'), ('Lose 1.0Kg in a week', 'Lose 1.0Kg in a week'), ('Lose 1.5Kg in a week', 'Lose 1.5Kg in a week'), ('Lose 2.0Kg in a week', 'Lose 2.0Kg in a week')])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose a different username')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already registered. Please use a different email.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account is registered with this email. Please Register.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                              validators=[DataRequired()])  
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  EqualTo('password')])
    submit = SubmitField('Reset Password')

