from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from whatsThatPest.config import Config

#initialize the databse
db = SQLAlchemy()
#initialize the encrytion for the storage of passwords
bcrypt = Bcrypt()
#creates the instance of the login manager with required configurations
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
#initialze the mailer for the application
mail = Mail()

#this function is used by run.py function which creates tg=he instance of the application
#all the required cofiguratoins are loaded from the config.py file
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #imports all the below packages
    from whatsThatPest.users.routes import users
    from whatsThatPest.posts.routes import posts
    from whatsThatPest.main.routes import main
    from whatsThatPest.errors.handlers import errors
    #register all the below packages
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
