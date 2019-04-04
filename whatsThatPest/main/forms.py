from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

#create form for bug recognition functionality. when user uploads bug image it will be stored as data in the 'picture' field of this form
class BugRecognitionForm(FlaskForm):
    #this corresponds to the image tag in the html file
    #this filed is optional but the selected image should be of the specified type
    picture = FileField('Upload bug picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #this corresponds to the submit button
    submit = SubmitField('Recognize!')