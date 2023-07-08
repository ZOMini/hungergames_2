from datetime import timedelta

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from core.config import settings


def create_app():
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'zip'}
    db = SQLAlchemy()
    migrate = Migrate()
    bootstrap = Bootstrap5()
    app = Flask('HungerGames')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['DEBUG'] = settings.app.debug
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.url_sync
    app.config['SECRET_KEY'] = settings.app.flask_secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = settings.app.jwt.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=settings.app.jwt.access_token_expires)
    # bootstrap.init_app(app)
    # db.init_app(app)
    # migrate.init_app(app, db)
    return app, db, migrate, bootstrap


app, db, migrate, bootstrap = create_app()
bootstrap.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)

