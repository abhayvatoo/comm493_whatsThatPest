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
    #this corresponds to the submit button
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
    #this field corresponds to the email of the user and the user must provide this detail
    #has a of type email
    email = StringField('Email', validators=[DataRequired(), Email()])
    #this field corresponds to the password of the user and the user must provide this detail
    password = PasswordField('Password', validators=[DataRequired()])
    #this corresponds to the remeber me check button to keep user login even after closling the browser
    #this feature is not currently implemented and will be implemented
    # TODO
    remember = BooleanField('Remember Me')
    #this corresponds to the submit button
    submit = SubmitField('Login')

#create form for updating the user information functionality
class UpdateAccountForm(FlaskForm):
    #this field corresponds to the username and the user must provide this detail
    #has requirement of minimum length of 2 characters and maximum of 20 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    #this field corresponds to the email of the user and the user must provide this detail
    #has a of type email
    email = StringField('Email', validators=[DataRequired(), Email()])
    #this field corresponds to the image for the post and this field is optional
    #the image must be of type jpg, png or jpeg
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #this corresponds to the submit button
    submit = SubmitField('Update')

    #this function check if the username entered by user is not already taken by some other user
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    #this function check if the email entered by user is not already taken by some other user
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

#create form for requesting a token for password reset functionality
class RequestResetForm(FlaskForm):
    #this field corresponds to the email of the user and the user must provide this detail
    #has a of type email
    email = StringField('Email', validators=[DataRequired(), Email()])
    #this corresponds to the submit button
    submit = SubmitField('Request Password Reset')

    #this function check if the email entered by user is a valid user's email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

#create form for reset password functionality
class ResetPasswordForm(FlaskForm):
    #this field corresponds to the password of the user and the user must provide this detail
    password = PasswordField('Password', validators=[DataRequired()])
    #this field corresponds to the password of the user and the user enter the same password as entered previously
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #this corresponds to the submit button
    submit = SubmitField('Reset Password')
