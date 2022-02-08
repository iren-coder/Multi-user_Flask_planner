import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True
    return app


app = create_app()
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)


from app import routes, models, forms
db.create_all()