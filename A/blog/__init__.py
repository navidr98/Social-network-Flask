from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '2409754aaf7cb3764fd79d401f9b408b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../blog.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


from blog import routes