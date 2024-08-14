from blog import db

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(30), unique=True,nullable=False)
    email = db.column(db.String(45), unique=True, nullable=False)
    password = db.column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.username})'