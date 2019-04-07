from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from whatsThatPest import db
from whatsThatPest.models import Post
from whatsThatPest.main.forms import BugRecognitionForm
from whatsThatPest.main.utils import save_picture, bug_recognition
from whatsThatPest.models import Bug
from whatsThatPest.Bug import bug_info


#this will create main module for the core functionality of the app
main = Blueprint('main', __name__)

#This connects this Python File to the root directory of our website
#This function is now mapped to the index page of our webpage
#This has to return something to the webpage
@main.route("/")
#define route for index page
#this route is same as root route because the root landing page is same as index page
@main.route("/index")
def index():
    #current_user is imported from flask_login package which contains all the information of current user's session
    #if the user is already logged in then we redirect to the home page 
    if current_user.is_authenticated:
        #redirects the user to the home page after successful authentication
        return redirect(url_for('main.home'))

    #create instance of bug recognition form for initial page
    form = BugRecognitionForm()
    return render_template('index.html', form=form)

#define about route for our story page
@main.route("/about")
def about():
    #this page contains products value propositions
    #and our team's basic information
    return render_template('about.html')

#define home route for home page
@main.route("/home")
#this make sure that the user has successfully logged in before accessing the home page
#this decorater is imported from flask_login
@login_required
def home():
    #create the instance of bug recognition form for the home page defined in the corresponding form.py file
    form = BugRecognitionForm()
    #fetch all the posts from database and order them
    #such that the latest post is comes first
    posts = Post.query.order_by(Post.date_posted.desc())
    post_count = posts.count()
    #display the home page with all the posts and bug recognition form
    return render_template('home.html', form=form, posts=posts, post_count=post_count)

#define the route for bug recognize call
#this route contains the call to ibm's visual recognition service
@main.route("/recognize", methods=['GET','POST'])
#this make sure that the user has successfully logged in before accessing the home page
#this decorater is imported from flask_login
@login_required
def recognize():
    #create the instance of bug recognition form for the home page defined in the corresponding form.py file
    form = BugRecognitionForm()
    #form has validation defined for image extention of jpg and jpeg
    #if image selected has valid extention
    if form.validate_on_submit():
        #if the form contains picture data 
        if form.picture.data:
            #save_picture function is defined in the utils.py file
            #this saves the file in db for later used
            bug_file = save_picture(form.picture.data)
            #bug_recognition function is defined in the utils.py file
            #this file calls the ibm service with the uploaded image and parse the response json and return the name if the bug
            bug_name = bug_recognition(bug_file)
            #bug object is created
            #this object is stored in db
            bug = Bug(name=bug_name, bug_image=bug_file, author=current_user)
            db.session.add(bug)
            db.session.commit()
            #bug information is fetched from the in memory map
            bug_data = bug_info[bug_name]
            image_source = bug_name + ".jpg"
            #we render the bug information page with all the data fetched above
            return render_template('bug_info.html', image_source=image_source, bug_name=bug_name, bug_damage=bug_data.get_damage(), bug_description = bug_data.get_description(), bug_pesticides = bug_data.get_pesticide())
        #if user hit submit button without uploading the image, then error message is displayed
        else:
            flash('No image selected', 'danger')
            return redirect(url_for('main.home'))
    #this functionality is planned for next sprints
    #this helps to call recognize route without logging in from index page itself
    #currently user is informed about 'work in progress'
    elif request.method == 'GET':
        flash('Image recognition without login is not available yet. Kindly upload your image again!', 'info')
        return redirect(url_for('main.home'))
 

