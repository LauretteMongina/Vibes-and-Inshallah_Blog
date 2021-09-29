from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField,FileField
from wtforms.validators import Required,Email


class UpdateProfile(FlaskForm):
    username = StringField('Enter Your Username', validators=[Required()])
    email = StringField('Email Address', validators=[Required(),Email()])
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    profile_picture = FileField('profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')


class Blog_postForm(FlaskForm):
    post_title = StringField('Title')
    content = TextAreaField('Content', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', validators=[Required()])
    submit = SubmitField('Comment')
    
    
class SubscriberForm(FlaskForm):
    email = TextAreaField('Email', validators=[Required()])
    submit = SubmitField('Submit')  