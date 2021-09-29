from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    username = StringField('Enter Your Username', validators=[Required()])

    bio = TextAreaField('Tell us about you.', validators=[Required()])
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