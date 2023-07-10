from flask import Blueprint
from flask_jwt_extended import jwt_required

from core.app import csrf
from core.config import settings
from services.user_service import UserService

auth = Blueprint('auth', __name__)


@auth.route('/user_create', methods=['POST', ])
@csrf.exempt
def user_create():
    """
    ---
    post:
      description: Создает пользователя в базе.(поля email, password). Идентификация происходит по name, обязательное поле.
      summary: create_user
      requestBody:
        content:
          application/json:
            schema: CreateUserSchema
      responses:
        201:
          description: User created. Login is email
        400:
          description: password != password2 or length < 8  // Wrong email or password or name
        403:
          description: FORBIDDEN
        422:
          description: UNPROCESSABLE ENTITY
      tags:
        - Auth
    """
    response = UserService.create_user()
    return response


@auth.route("/login", methods=['POST', ])
@csrf.exempt
def login():
    """
    ---
    post:
      summary: Возвращает ACCESS token
      description: Принимает логин(email)/пароль, возвращает ACCESS токен.
      requestBody:
        description: Логин и пароль
        content:
          application/json:
            schema: LoginInputSchema
      responses:
        200:
          description: Результат ACCESS token
          content:
            application/json:
              schema: OutputSchema
        400:
          description: Ошибка
          content:
            application/json:
              schema: ErrorSchema
        403:
          description: FORBIDDEN
      tags:
        - Auth
    """
    response = UserService.login()
    return response


@auth.route("/logout", methods=['DELETE', ])
@jwt_required()
@csrf.exempt
def logout():
    """
    ---
    delete:
      summary: Logout (need access token)
      description: Отзывает его access token - помещаяя в redis blocklist.
      responses:
        204:
          description: Access tokens revoked
        400:
          description: BAD REQUEST
        401:
          description: UNAUTHORIZED
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Auth
    """
    response = UserService.logout()
    return response
