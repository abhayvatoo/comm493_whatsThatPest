from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from whatsThatPest import db, login_manager
from flask_login import UserMixin

#this function is used for loading the current user's information from database
#it uses login_manager module imported from flask_login in whatsThatPest __init__.py file
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#this class represnts the user table of the database
#db.model is used for the object relational mapping
#all the attributes of this class are the coulmn of the user table
class User(db.Model, UserMixin):
    #this is auto generated id for each user which acts as a primary key and is of type integer
    id = db.Column(db.Integer, primary_key=True)
    #this represents the username cloumn and it should be unique, not null and can be maximum of 20 character long
    username = db.Column(db.String(20), unique=True, nullable=False)
    #this represents email column and it should be unique, not null and can be maximum of 120 character long 
    email = db.Column(db.String(120), unique=True, nullable=False)
    #this represents the column to store the profile image's name
    #it has a default value of 'default.jpg' and it is not null and can be maximum of 20 character long
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    #this represents password column, it should not be null and maximum of 60 character long
    password = db.Column(db.String(60), nullable=False)
    #this corresponds to the post which the user has added
    #the db relationship is used for one to many relationship i.e. a single user can have multiple post
    posts = db.relationship('Post', backref='author', lazy=True)
    #this corresponds to the bug which the user has identified using ibm service
    #this information is stored in db for keeping a track of each user's service usage
    #the db relationship is used for one to many relationship i.e. a single user can have multiple  bug info
    bugs = db.relationship('Bug', backref='author', lazy=True)

    #this function is used for generating a token which is valid for 1800 seconds for reset password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    #this is a static method which verfies if the token used by the owner is valid
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    #this function is used by python for printing the object is this class on command line
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"

#this class represnts the post table of the database
#db.model is used for the object relational mapping
#all the attributes of this class are the coulmn of the post table
class Post(db.Model):
    #this represents auto generated id for each post which acts as a primary key and is of type integer
    id = db.Column(db.Integer, primary_key=True)
    #this represents the title column for the post and it cannot be null
    title = db.Column(db.String(100), nullable=False)
    #this represents the date column to store the timestamp of the post and it cannot be null
    #it has a default value of current time i.e. the time when the user add a new post
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #this represents the content column to store the content of the post and it cannot be null
    content = db.Column(db.Text, nullable=False)
    #this column is the mapping of the relationship with the user table
    #the user's table id couln is the foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #this stores the file name of the post image uploaded by the user and it is an optional field
    post_image = db.Column(db.String(20))

    #this function is used by python for printing the object is this class on command line
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#this class represnts the bug table of the database
#db.model is used for the object relational mapping
#all the attributes of this class are the coulmn of the bug table
class Bug(db.Model):
    #this is auto generated id for each bug which acts as a primary key and is of type integer
    id = db.Column(db.Integer, primary_key=True)
     #this represents the title name for the bug identified and it cannot be null
    name = db.Column(db.String(100), nullable=False)
    #this represents the date column to store the timestamp of the post and it cannot be null
    #it has a default value of current time i.e. the time when the user add a new post
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #this column is the mapping of the relationship with the user table
    #the user's table id couln is the foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #this stores the file name of the bug image uploaded by the user and it cannot be null
    bug_image = db.Column(db.String(20), nullable=False)

    #this function is used by python for printing the object is this class on command line
    def __repr__(self):
        return f"Bug('{self.name}', '{self.date_posted}')"
