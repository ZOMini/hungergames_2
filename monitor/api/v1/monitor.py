from uuid import UUID

from flask import Blueprint
from flask_jwt_extended import jwt_required

from core.app import csrf
from core.config import settings
from services.api_monitor_service import ApiMonitorService

monitor = Blueprint('monitor', __name__)


@monitor.route('/one_link', methods=['POST', ])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
@csrf.exempt
def one_link():
    """
    ---
    post:
      description: Постит одну запись в БД.
      summary: post_one_url
      requestBody:
        content:
          application/json:
            schema: PostUrlSchema
      responses:
        201:
          description: Url posted.
        400:
          description: BAD_REQUEST
        401:
          description: UNAUTHORIZED
        403:
          description: FORBIDDEN
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Monitor
    """
    response = ApiMonitorService.post_one_link()
    return response


@monitor.route('/links', methods=['POST', ])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
@csrf.exempt
def links():
    """
    ---
    post:
      description: Постит набор урлов в БД, из файла zip содержащего csv с урлами.
      summary: post_many_urls
      requestBody:
        content:
          multipart/form-data:
            schema: PostUrlsSchema
      responses:
        202:
          description: Post urls.
        400:
          description: BAD_REQUEST
        401:
          description: UNAUTHORIZED
        403:
          description: FORBIDDEN
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Monitor
    """
    response = ApiMonitorService.post_links()
    return response


@monitor.route('/file_upload/<string:link_id>', methods=['POST', ])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
@csrf.exempt
def file_upload(link_id: UUID):
    """
    ---
    post:
      description: Постит картинку в БД.
      summary: post_image
      parameters:
        - name: link_id
          in: path
          description: id(UUID) ссылки
          required: true
          schema:
            type: string
      requestBody:
        content:
          multipart/form-data:
            schema: PostImageSchema
      responses:
        201:
          description: File appended.
        400:
          description: BAD_REQUEST
        401:
          description: UNAUTHORIZED
        403:
          description: FORBIDDEN
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Monitor
    """
    response = ApiMonitorService.post_image(link_id)
    return response


@monitor.route('/links', methods=['GET', ])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
@csrf.exempt
def get_links():
    """
    ---
    get:
      description: Отдает список урлов с фильтрами и пагинацией.
      summary: Get links
      parameters:
        - name: page
          in: query
          description: Номер страницы
          required: false
          schema:
            type: integer
        - name: size
          in: query
          description: Размер страницы
          required: false
          schema:
            type: integer
        - name: link_id
          in: query
          description: id(UUID) ссылки
          required: false
          schema:
            type: string
        - name: domain_zone
          in: query
          description: Доменная зона.
          required: false
          schema:
            type: string
        - name: available
          in: query
          description: Доступна ли страница.
          required: false
          schema:
            type: bool
      responses:
        200:
          description: List urls.
        400:
          description: BAD_REQUEST
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Monitor
    """
    response = ApiMonitorService.get_urls()
    return response


@monitor.route('/logs', methods=['GET', ])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
@csrf.exempt
def get_logs():
    """
    ---
    get:
      description: Отдает последние логи. Количество строк можно поменять в env.yaml
      summary: Get logs
      responses:
        200:
          description: List logs.
        400:
          description: BAD_REQUEST
        422:
          description: UNPROCESSABLE ENTITY
      security:
        - jwt_key: []
      tags:
        - Monitor
    """
    response = ApiMonitorService.get_logs()
    return response
