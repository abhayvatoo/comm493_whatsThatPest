
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from whatsThatPest import mail

#this helper functions stores the image on file system and we pass in the bug image as argument
def save_picture(form_picture):
    #randon hex is generated to prevent the case of two files having same name
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    #picture filename is created using the same extension of the uploaded file and a random hex
    picture_fn = random_hex + f_ext
    #create the path to store the image under static directory
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    #resize the image to 125X125 pixels to save disk space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    #return the randomly generated file name with extension to be store used later
    return picture_fn

# helper function generate token, message of email and send email with steps to reset password
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
