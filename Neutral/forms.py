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

#Defined all the forms and the input data


class searchForm(Form): # Form to search for the food as seen in Search Food
    foodname = StringField('Search Food',validators=[InputRequired()])

class dateForm(Form):
    fooddate = DateField('Select Food Record Date', validators=[InputRequired()], format='%Y-%m-%d')

class RegistrationForm(FlaskForm):  # Form to get the registration details as seen in the Register page
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

    healthGoal = SelectField(label='Health Goals', choices=[('Maintain Weight', 'Maintain Weight'),('Lose 0.25Kg in a week', 'Lose 0.25Kg in a week'), ('Lose 0.5Kg in a week', 'Lose 0.5Kg in a week'), ('Lose 0.75kg in a week', 'Lose 0.75Kg in a week'), ('Lose 1.0Kg in a week', 'Lose 1.0Kg in a week')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username): #To check if username is already used by another user
        user = User.query.filter_by(username=username.data).first()
        if user: #If there is another user using the username already, return error
            raise ValidationError('Username is already taken. Please choose a different username')

    def validate_email(self,email): #To check if the email is registered already
        user = User.query.filter_by(email=email.data).first()
        if user: #If email is registerd already, return error
            raise ValidationError('Email is already registered. Please use a different email.')

class LoginForm(FlaskForm): #Form to log user in as seen in login page
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                              validators=[DataRequired()])  
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm): #Form to allow users to change their account details as seen in Profile page
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
    healthGoal = SelectField(label='Health Goals', choices=[('Maintain Weight', 'Maintain Weight'),('Lose 0.25Kg in a week', 'Lose 0.25Kg in a week'), ('Lose 0.5Kg in a week', 'Lose 0.5Kg in a week'), ('Lose 0.75Kg in a week', 'Lose 0.75Kg in a week'), ('Lose 1.0Kg in a week', 'Lose 1.0Kg in a week')])

    submit = SubmitField('Update')

    def validate_username(self,username):#To check if the username is used by another user already
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose a different username')

    def validate_email(self,email): #To check if the email is registered already
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already registered. Please use a different email.')

class RequestResetForm(FlaskForm): #Form to send the email to user to reset password
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self,email): #To check if the email is registered
        user = User.query.filter_by(email=email.data).first()
        if user is None: #If email is not registered, return error
            raise ValidationError('No account is registered with this email. Please Register.')


class ResetPasswordForm(FlaskForm): #Form to allow users to change their password
    password = PasswordField('Password',
                              validators=[DataRequired()])  
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  EqualTo('password')])
    submit = SubmitField('Reset Password')

