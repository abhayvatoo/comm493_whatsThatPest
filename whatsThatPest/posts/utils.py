import os
import secrets
from PIL import Image
from flask import current_app

#this helper functions stores the image on file system and we pass in the bug image as argument
def save_picture(form_picture):
    #randon hex is generated to prevent the case of two files having same name
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    #picture filename is created using the same extension of the uploaded file and a random hex
    picture_fn = random_hex + f_ext
    #create the path to store the image under static directory
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    #picture is saved on the file system
    i = Image.open(form_picture)
    i.save(picture_path)
    #return the randomly generated file name with extension to be store used later
    return picture_fn
