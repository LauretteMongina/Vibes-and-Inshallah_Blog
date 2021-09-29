from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic_path = db.Column(db.String())
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    


    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.username}'
class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'
class Quotes:
    def __init__(self, author, quote):
        self.id = id
        self.author = author
        self.quote = quote

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255),nullable = False)
    content = db.Column(db.Text(), nullable = False)
    comment = db.relationship('Comment',backref='post',lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts

    # get user posts by user id
    @classmethod
    def get_user_posts(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id)
        return blogs
    def get_post(id):
        post = Post.query.filter_by(id=id).first()

    # get post by category
    @classmethod
    def get_post_by_category(cls, category_id):
        blogs = Post.query.filter_by(category_id=category_id)
        return posts

    # get post comments
    def get_comments(self):
        comments = Comment.query.filter_by(Post_id=self.id)
        return comments

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

        
    def __repr__(self):
        return f'Post {self.content}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'),nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comments(cls):
        comments = Comment.query.all()
        return comments
    @classmethod
    def get_comments(cls,post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()

        return comments

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()
    def __repr__(self):
        return f'Comment:{self.comment}'
class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_subscribers(cls):
        subscribers = Subscriber.query.all()
        return subscribers

    def __repr__(self):
        return f'Subscriber {self.email}'