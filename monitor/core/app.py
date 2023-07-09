from datetime import timedelta

from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from turbo_flask import Turbo

from core.config import settings


def create_app():
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'zip'}
    db = SQLAlchemy()
    migrate = Migrate()
    bootstrap = Bootstrap5()
    turbo = Turbo()
    app = Flask('HungerGames')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['DEBUG'] = settings.app.debug
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.url_sync
    app.config['SECRET_KEY'] = settings.app.flask_secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = settings.app.jwt.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=settings.app.jwt.access_token_expires)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    return app, db, migrate, bootstrap, turbo


app, db, migrate, bootstrap, turbo = create_app()
bootstrap.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
turbo.init_app(app)


# Error handlers
@app.errorhandler(500)
def error_500(e):
    if request.path.startswith('/api/'):
        return jsonify(message='Internal Server Error'), 500
    return render_template('500.html'), 500

@app.errorhandler(400)
def error_400(e):
    if request.path.startswith('/api/'):
        return jsonify(message='Bad request'), 400
    return render_template('400.html'), 400

@app.errorhandler(404)
def error_404(e):
    if request.path.startswith('/api/'):
        return jsonify(message='Not found'), 404
    return render_template('404.html'), 404
