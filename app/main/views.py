from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User, BlogPost, Comment,Subscriber,Category
from .forms import UpdateProfile, Blog_postForm, CommentForm,SubscriberForm
from .. import db, photos
from ..requests import get_quotes


@main.route('/')
def index():
    blogs = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    quote = get_quotes()
    categories = Category.query.all()
    return render_template('index.html', quote = quote,categories = categories,blogs=blogs)

@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()


    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image,form=form)


@main.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('users_blog_posts.html', blog_posts=blog_posts, user=user)

@main.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('main.index'))

    return render_template('individual.html',form=form)
@main.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post
    )

@main.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@main.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
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