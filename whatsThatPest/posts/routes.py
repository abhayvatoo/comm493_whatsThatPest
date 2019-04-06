from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from whatsThatPest import db
from whatsThatPest.models import Post
from whatsThatPest.posts.forms import PostForm
from whatsThatPest.posts.utils import save_picture

#create posts module for the functionality related to user posts
posts = Blueprint('posts', __name__)

#define new post route for the page to create new post
@posts.route("/post/new", methods=['GET', 'POST'])
#this make sure that the user has successfully logged in before accessing the new post page
#this decorater is imported from flask_login
@login_required
def new_post():
    #create the instance of new post creation form for the page defined in the corresponding forms.py file
    form = PostForm()
    #form has basic validation defined
    #if the form is valid
    if form.validate_on_submit():
        #if user has uploaded the picture for the post then it will stored in database
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post = Post(title=form.title.data, content=form.content.data, author=current_user, post_image=picture_file)
        #otherwise only the title and content is stored
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        #the post object created above is committed to database
        db.session.add(post)
        db.session.commit()
        #success message is flashed after successful creation if post
        #user is redirected to home page where the user can see the new post
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    #if the form is not valid then the new post form is displayed
    return render_template('create_post.html', title='New Post', form=form)

#define delete post route
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
#this make sure that the user has successfully logged in before accessing the new post page
#this decorater is imported from flask_login
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    #the post with the given id is deleted from the database
    db.session.delete(post)
    db.session.commit()
    #success message is flashed after successful creation if post
    #user is redirected to home page where the user can see the remaining posts
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
