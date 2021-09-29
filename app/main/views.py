from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User,Post, Comment,Subscriber,Category
from .forms import UpdateProfile, Blog_postForm, CommentForm,SubscriberForm
from .. import db, photos
from ..requests import get_quotes


@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    quote = get_quotes()
    categories = Category.query.all()
    return render_template('index.html', quote = quote,categories = categories,posts = posts)

@main.route('/profile',methods = ['POST','GET'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_pic_path = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Succesfully updated your profile')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    profile_pic_path = url_for('static',filename = 'photos/'+ 'current_user.profile_pic_path') 
    return render_template('profile/profile.html', profile_pic_path=profile_pic_path, form = form)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)

@main.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    post = Post.query.get_or_404(id)
    post_comments = Comment.query.filter_by(post_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment_form.comment.data, author=current_user)
        new_comment.save_comment()

    return render_template('individual.html', post=post, post_comments=post_comments, comment_form=comment_form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    # flash('Your post has been deleted', 'successfully')
    return redirect(url_for('main.index'))


@main.route('/Update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = Blog_postForm()
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been Updated', 'successfully')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.post_title.data = post.title
        form.content.data = post.content
    return render_template('users_blog_posts.html', form=form)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment.form.data, author=current_user)
        new_comment.save_comment()

    return render_template('index.html', comment_form=comment_form)


@main.route('/comment/delete/<comment_id>', methods = ['Post','GET'])
@login_required
def delete_comment(comment_id):
    comments = Comment.query.get(comment_id)
    db.session.delete(comments)
    db.session.commit()
    flash("You have deleted your comment succesfully!")
    return redirect(url_for('main.index'))

@main.route('/subscriber', methods=['GET', 'POST'])
def subscriber():
    subscriber_form = SubscriberForm()
    if subscriber_form.validate_on_submit():
        new_subscriber = Subscriber( email=subscriber_form.email.data)
        new_subscriber.save_subscriber()
        flash('Email has been submitted successfully', 'success')

    return render_template('index.html', subscriber_form=subscriber_form)
@main.route('/post/new', methods=['GET', 'POST'])
def post():
    """
    View Post function that returns the Post page and data
    """
    post_form = Blog_postForm()

    if post_form.validate_on_submit():
        title = post_form.post_title.data
        content = post_form.content.data

        new_post = Post(title=title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.index'))

    title = 'New Post'
    return render_template('blog.html', post_form=post_form)