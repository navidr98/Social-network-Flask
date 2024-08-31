from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '2409754aaf7cb3764fd79d401f9b408b'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../blog.db'

app.config['SECRET_KEY'] = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi' # Replace with your own secret key
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lez6zEqAAAAAEOsCQYAQS4myQ7U8I_IALpF3jMj' # Replace with your reCAPTCHA site key
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lez6zEqAAAAAMZfC6t6wBXzHFQm7lmNGcUEazR_' # Replace with your reCAPTCHA secret key

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login first'
login_manager.login_message_category = 'info'


from blog import routes