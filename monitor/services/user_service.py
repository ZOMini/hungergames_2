from http import HTTPStatus as HTTP

from flask import Response, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt
from sqlalchemy.sql import select

from core.config import settings
from core.logger import file_logger
from db.connection_db import db_session
from db.connection_redis import jwt_redis_blocklist
from db.models_db import User


class UserService():

    @classmethod
    def create_user(cls) -> tuple[Response, HTTP]:
        try:
            body = request.get_json()
            name = body['name']
            email = body['email']
            password = body['password']
            password2 = body['password2']
            if password and password2 and name and email and password == password2:
                user = User(name=name,
                            email=email,
                            password=password)
                db_session.add(user)
                db_session.commit()
                file_logger.info('User created - %s', user.id)
                return jsonify('User created. Login is email.'), HTTP.CREATED
            else:
                return jsonify('check query or password != password2 or length password < 8'), HTTP.BAD_REQUEST
        except Exception as e:
            db_session.rollback()
            return jsonify(msg="Wrong email or password or name",
                           err=e.args), HTTP.BAD_REQUEST

    @classmethod
    def login(cls) -> tuple[Response, HTTP]:
        body = request.get_json()
        if 'email' not in body or 'password' not in body:
            return jsonify("Not email or password"), HTTP.BAD_REQUEST
        email = body['email']
        password = body['password']
        user = db_session.scalar(select(User).filter(User.email == email).limit(1))
        if not user or not user.check_password(password, email):
            file_logger.info('Login fail: email(login) - %s ', email)
            return jsonify("Wrong email or password"), HTTP.UNAUTHORIZED
        access_token = create_access_token(identity=user)
        file_logger.info('Login successful: user_id - %s ', user.id)
        return jsonify(access_token=access_token), HTTP.CREATED

    @classmethod
    def logout(cls) -> tuple[Response, HTTP]:
        try:
            jti = get_jwt()['jti']
            user_id = get_jwt()['sub']
            jwt_redis_blocklist.set(jti, '', ex=settings.app.jwt.access_token_expires)
            file_logger.info('Logout successful: user_id - %s', user_id)
            return jsonify(), HTTP.NO_CONTENT
        except Exception as e:
            return jsonify(msg='Error, see body',
                           err=e.args), HTTP.BAD_REQUEST
