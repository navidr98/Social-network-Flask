from blog import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.username})'
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.title[:20]} - {self.date})'
