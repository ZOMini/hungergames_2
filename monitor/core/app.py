from datetime import timedelta

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import settings
from core.logger import init_loggers


def create_app():
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'zip'}
    init_loggers()
    db = SQLAlchemy()
    migrate = Migrate()
    app = Flask('HungerGames')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['DEBUG'] = settings.app.debug
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.url_sync
    app.config['SECRET_KEY'] = settings.app.flask_secret_key
    app.config['JWT_SECRET_KEY'] = settings.app.jwt.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=settings.app.jwt.access_token_expires)
    db.init_app(app)
    migrate.init_app(app, db)
    return app, db, migrate


app, db, migrate = create_app()
bootstrap = Bootstrap5(app)
jwt = JWTManager(app)
