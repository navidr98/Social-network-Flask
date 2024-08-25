from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User
from flask_wtf.recaptcha import RecaptchaField
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=30, message='Username must be between 3 and 30 characters long')])
    email = StringField('Email',validators=[DataRequired(), Email(message='Enter valid email like exampel@mail.com')])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=4, max=30, message='Enter password contains 4 charachter at least')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exists")


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email(message='Enter valid email like exampel@mail.com')])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=4, max=30, message='Enter password contains 4 charachter at least')])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')



class EditProfileFrom(FlaskForm):
    username = StringField('Username',validators=[Length(min=3, max=30, message='Username must be between 3 and 30 characters long')])
    email = StringField('Email',validators=[Email(message='Enter valid email like exampel@mail.com')])
    password = PasswordField('New Password',validators=[Length(max=30, message='Enter password contains 4 charachter at least')])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Password must match')])
    submit_user = SubmitField('Update Username')
    submit_email = SubmitField('Update Email')
    submit_pass = SubmitField('Update Password')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email already exists")
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Edit Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment')
    submit = SubmitField('Add Comment')