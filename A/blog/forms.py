from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User
from flask_wtf.recaptcha import RecaptchaField
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('نام کاربری',validators=[DataRequired(), Length(min=3, max=30, message='نام کاربری حداقل شامل ۳ حرف باشد')])
    email = StringField('پست الکترونیک',validators=[DataRequired(), Email(message='ایمیل معتبر وارد کنید ')])
    password = PasswordField('رمز عبور',validators=[DataRequired(), Length(min=4, max=30, message='رمز عبور حداقل شامل ۴ حرف باشد')])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password', message='رمز عبور همخوانی ندارد')])
    submit = SubmitField('ثبت نام')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('نام کاربری تکراری است')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("ایمیل تکراری است")


class LoginForm(FlaskForm):
    email = StringField('پست الکترونیک',validators=[DataRequired(), Email(message='پست الکترونیک صحیح وارد کنید')])
    password = PasswordField('رمز ورود',validators=[DataRequired(), Length(min=4, message='رمز عبور حداقل ۴ حرف باشد')])
    remember_me = BooleanField('مرا به خاطر بسپار')
    recaptcha = RecaptchaField()
    submit = SubmitField('ورود')



class EditProfileFrom(FlaskForm):
    username = StringField('نام کاربری',validators=[Length(min=3, max=30, message='نام کاربری حداقل شامل ۳ حرف باشد')])
    email = StringField('پست الکترونیک',validators=[Email(message='پست الکترونیک معتبر وارد کنید ')])
    password = PasswordField('رمز عبور',validators=[Length(max=30, message='رمز عبور حداقل شامل ۴ حرف باشد')])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[EqualTo('password', message='رمز عبور همخوانی ندارد')])
    submit_user = SubmitField('به روز رسانی نام کاربری')
    submit_email = SubmitField('به روز رسانی پست الکترونیک')
    submit_pass = SubmitField('به روز رسانی رمز عبور')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('نام کاربری تکراری است')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("پست الکترونیک تکراری است")
            
class PostForm(FlaskForm):
    title = StringField('موضوع', validators=[DataRequired()])
    content = TextAreaField('محتوا', validators=[DataRequired()])
    submit = SubmitField('ثبت')


class EditPostForm(FlaskForm):
    title = StringField('موضوع', validators=[DataRequired()])
    content = TextAreaField('محتوا', validators=[DataRequired()])
    submit = SubmitField('ویرایش پست')

class CommentForm(FlaskForm):
    content = TextAreaField('نظر')
    submit = SubmitField('ثبت نظر')

class ReplyForm(FlaskForm):
    text = TextAreaField('پاسخ')
    submit = SubmitField('ثبت پاسخ')


class LikeForm(FlaskForm):
    submit = SubmitField('لایک')

class DisLikeForm(FlaskForm):
    submit = SubmitField('دیسلایک')

class SearchForm(FlaskForm):
    title = StringField('Search by Title', validators=[DataRequired(message="بر اساس عنوان ")])
    submit = SubmitField('جستجو')

    