from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='Enter username'), Length(min=3, max=30, message='Username must contain at least for 3 charachters')])
    email = StringField('Email',validators=[DataRequired(), Email(message='Enter valid email like exampel@mail.com')])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=4, max=30, message='Enter password contains 4 charachter at least')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match')])


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=4, max=30)])
    remember = BooleanField('Remember me')