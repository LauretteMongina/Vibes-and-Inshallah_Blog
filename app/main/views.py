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

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
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
        post.post_title = form.post_title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been Updated', 'successfully')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.post_title.data = post.post_title
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
@login_required
def subscriber():
    subscriber_form = SubscriberForm()
    if subscriber_form.validate_on_submit():
        new_subscriber = Subscriber( email=subscriber_form.email.data)
        new_subscriber.save_subscriber()
        flash('Email has been submitted successfully', 'success')

    return render_template('index.html', subscriber_form=subscriber_form)
@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def post():
    """
    View Post function that returns the Post page and data
    """
    post_form = Blog_postForm()

    if post_form.validate_on_submit():
        post_title = post_form.post_title.data
        content = post_form.content.data
        # user = current_user

        new_post = Post(post_title=post_title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.index'))

    title = 'New Post'
    return render_template('blog.html', title=title, post_form=post_form)