from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from whatsThatPest.models import User

#create form for sign up functionality
#a new user is created after submitting this form
class RegistrationForm(FlaskForm):
    #this field corresponds to the username and the user must provide this detail
    #has requirement of minimum length of 2 characters and maximum of 20 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    #this field corresponds to the email of the user and the user must provide this detail
    #has a of type email
    email = StringField('Email', validators=[DataRequired(), Email()])
    #this field corresponds to the password of the user and the user must provide this detail
    password = PasswordField('Password', validators=[DataRequired()])
    #this field corresponds to the password of the user and the user enter the same password as entered previously
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #this corresponds to the submit 
    submit = SubmitField('Sign Up')

    #this function check if the username entered by user is not already taken by some other user
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    #this function check if the email entered by user is not already taken by some other user
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

#create form for login functionality
#user can login after submitting this form
class LoginForm(FlaskForm):
    #this field corresponds to the email 
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
