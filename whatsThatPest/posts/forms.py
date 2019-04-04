from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

#create form for post creation functionality
#when user uploads new post all the below information is created and stored in database
class PostForm(FlaskForm):
    #this corresponds to the title of the post in the html file
    #the user must provide this detail
    title = StringField('Title', validators=[DataRequired()])
    #corresponds to the content of the post in the html file
    #the user must provide this detail and the field has length of 10 rows
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"rows": 10})
    #this corresponds to the image tag in the html file
    #this filed is optional but the selected image should be of the specified type
    picture = FileField('Add a Picture to your post', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #this corresponds to the submit button
    submit = SubmitField('Post')
