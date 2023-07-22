from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from sqlalchemy import select

from core.app import csrf, db, login_manager
from db.connection_db import db_session
from db.models_db import User
from web import form

web_auth = Blueprint('web_auth', __name__)


@login_manager.user_loader
def loader_user(user_id):
    return db_session.get(User, user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('Authorization needed')
    return redirect(url_for('pages.links'))


@web_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.form.get('password') != request.form.get('confirm'):
                flash('Check password and password confirm.')
            else:
                user = User(email=request.form.get('email'),
                            name=request.form.get('name'),
                            password=request.form.get('password'))
                db.session.add(user)
                db.session.commit()
                flash(f'User - {user.name} created, please login.')
                return redirect(url_for('pages.links'))
        except Exception:
            db.session.rollback()
            flash('Check name, email, password, password confirm')
    return render_template('sign_up.html', form=form.SignupForm())


@web_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        user = db.session.scalar(select(User).filter_by(email=email))
        if not email or not password or not user:
            flash('Check your email and password.')
            # return redirect(url_for('pages.links'))
        if user.check_password(password=password, email=email):
            login_user(user)
            return redirect(url_for('pages.links'))
        flash('Check your email and password.')
    return redirect(url_for('pages.links'))


@web_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.links'))
