from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_basicauth import BasicAuth
from flask_mail import Mail
import os
from dotenv import load_dotenv

app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
basic_auth = BasicAuth(app)
login = LoginManager(app)
admin_ = Admin(app, name='ProRakAbd BLOGS',url='/admin', template_mode='bootstrap3')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = 'bd7058f90e8ecdd78eace726b01a4de6'
app.config['BASIC_AUTH_USERNAME'] = os.getenv('ADMIN_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('ADMIN_PASSWORD')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

login.login_view = 'users.login'
login.login_message_category = 'info'
mail= Mail(app)

from blog_app.users.routes import users
from blog_app.posts.routes import posts
from blog_app.main.routes import main
from blog_app.admin.admin import admin_con
from blog_app.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(admin_con)
app.register_blueprint(errors)