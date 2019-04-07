import os
import secrets
from PIL import Image
from flask import current_app
from watson_developer_cloud import VisualRecognitionV3
import json


#this helper functions stores the image on file system and we pass in the bug image as argument
def save_picture(bug_picture):
    #randon hex is generated to prevent the case of two files having same name
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(bug_picture.filename)
    #picture filename is created using the same extension of the uploaded file and a random hex
    picture_fn = random_hex + f_ext
    #create the path to store the image under static directory
    picture_path = os.path.join(current_app.root_path, 'static/bug_pics', picture_fn)
    #picture is saved on the file system
    i = Image.open(bug_picture)
    i.save(picture_path)
    #return the randomly generated file name with extension to be store used later
    return picture_fn

#this helper function invokes the ibm watson visual recognition api and we pass in the bug image as argument
def bug_recognition(bug_image):
    #this is the constructor of the Visual Recognition method pre-defined by ibm
    #we pass the api in this constructor
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='KGSz0-fDoeCCyQQLQeWtfXro_RgjEa0PK44S5FPHNlU5')
    #generate the full path of the bug image file which is earlier stored in the file system by the above helper function
    bug_path = os.path.join(current_app.root_path, 'static/bug_pics', bug_image)
    #load that image and pass it to ibm
    with open(bug_path, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
            classifier_ids='PestRecognitionModel_39839098').result
    #try to parse the response json and return the recognized bug and return unknown if the service is not able to identify the bug
    try:
        return classes['images'][0]['classifiers'][0]['classes'][0]['class']
    except:
        return 'unknown'
