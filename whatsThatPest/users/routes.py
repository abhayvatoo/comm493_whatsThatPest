from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from whatsThatPest import db, bcrypt
from whatsThatPest.models import User, Post
from whatsThatPest.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from whatsThatPest.users.utils import save_picture, send_reset_email

#create user module for the functionality related to user
users = Blueprint('users', __name__)

#define new user registration route for the user to create new user
@users.route("/register", methods=['GET', 'POST'])
def register():
    #if user has already logged in then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #create the instance of new user creation form for the page defined in the corresponding forms.py file
    form = RegistrationForm()
    #form has basic validation defined
    #if the form is valid
    if form.validate_on_submit():
        #encrypyt the password before storing it in database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #creates the user model object
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #upadte the database
        db.session.add(user)
        db.session.commit()
        #success message is flashed on screen
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    #if the form is not valid then the registrartion form is displayed
    return render_template('register.html', title='Register', form=form)

#define login route for the user to login
@users.route("/login", methods=['GET', 'POST'])
def login():
    #if user has already logged in then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #create the instance of login form for the page defined in the corresponding forms.py file
    form = LoginForm()
    #form has basic validation defined
    #if the form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #if user has entered correct email and password combination
        #then user is allowed to access the home page
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        #else error message is displayed
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    #if the form is not valid then the login form is displayed
    return render_template('login.html', title='Login', form=form)

#define logut route for the user to logut
@users.route("/logout")
def logout():
    #this method is imported from flask_login module and it handles all the steps to logout the user
    logout_user()
    return redirect(url_for('main.index'))

#define account route for the user to upadte the profile information
@users.route("/account", methods=['GET', 'POST'])
#this make sure that the user has successfully logged in before accessing the this page
#this decorater is imported from flask_login
@login_required
def account():
    #create the instance of upadte account form for the page defined in the corresponding forms.py file
    form = UpdateAccountForm()
    #form has basic validation defined
    #if the form is valid then the information is upadted and success message is displayed
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    #for the case of GET request the form is dipslyed with prefilled the information of the current user
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    #if nither the form is valid on submit nor a GET request then update info form is displayed again
    return render_template('account.html', title='Account', profile_image=profile_image, form=form)

#define reset password route for the user to reset the password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #if user has already logged in then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #create the instance of reset password form for the page defined in the corresponding forms.py file
    form = RequestResetForm()
    #if the email entered by the user is valid email and the user exists in the database
    #then reset password instructions are emailed to the given email address
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    #if the form is not valid then the reset password form is displayed
    return render_template('reset_request.html', title='Reset Password', form=form)

#define reset password route with token as a parameter for the user to reset the password
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #if user has already logged in then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #the input token is validated using the helper method
    user = User.verify_reset_token(token)
    #if the token is invalid then warning message is displayed and reset password form is displayed for new request
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    #otherwise new password form is displayed
    form = ResetPasswordForm()
     #form has basic validation defined and if the form is valid
    if form.validate_on_submit():
        #entered password is encryted
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        #database is upadted
        db.session.commit()
        #success message is displayed
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    #if the form is not valid then the new password form is displayed
    return render_template('reset_token.html', title='Reset Password', form=form)
