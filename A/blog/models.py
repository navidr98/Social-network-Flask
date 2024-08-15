from blog import db
from sqlalchemy import Column
from blog import db, login_manager


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.username})'