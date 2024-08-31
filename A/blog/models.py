from blog import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import jdatetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    posts = db.relationship('Post', cascade="all, delete", backref='author', lazy=True)
    comments = db.relationship('Comment', cascade="all, delete", backref='owner', lazy=True)
    replies = db.relationship('Reply', cascade="all, delete", backref='response', lazy=True)
    likes = db.relationship('Like', cascade="all, delete", backref='user', lazy=True)
    follows = db.relationship('Like', cascade="all, delete", backref='flw_user', lazy=True)
   
    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.username})'
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', cascade="all, delete", backref='post', lazy=True)
    likes = db.relationship('Like', cascade="all, delete", backref='like', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.title[:20]} - {self.date})'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rep = db.relationship('Reply',cascade="all, delete", backref='comment', lazy=True)        

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.content[:20]}'


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    text = db.Column(db.Text)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.content[:20]}'

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('current_user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)