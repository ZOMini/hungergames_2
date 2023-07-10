import csv
import os
import zipfile
from http import HTTPStatus as HTTP
from typing import Any

from flask import current_app, jsonify, request
from sqlalchemy import select

from app_celery.tasks import post_urls
from core.config import settings
from core.logger import file_logger
from db.connection_db import db_session
from db.models_db import Event, Link


class ApiMonitorService():

    @staticmethod
    def post_one_link():
        try:
            body = request.get_json()
            link_obj = Link(body['url'])
            db_session.add(link_obj)
            db_session.commit()
            file_logger.info('Url - %s added.', link_obj)
            return jsonify(link_obj.get_dict()), HTTP.CREATED
        except Exception as e:
            db_session.rollback()
            return jsonify(e.args), HTTP.BAD_REQUEST

    @staticmethod
    def upload_zip_file() -> str:
        """Валидирует и сохраняет csv из полученного zip файла"""
        try:
            file = request.files['file']
            fileName = file.filename
            if str(fileName).split('.')[1] not in current_app.config['ALLOWED_EXTENSIONS']:
                raise FileNotFoundError('Only zip file.')
            zip_file = zipfile.ZipFile(file)
            if len(zip_file.namelist()) > 1:
                raise FileNotFoundError('Only 1 file in zip.')
            for name in zip_file.namelist():
                file_path = zip_file.extract(name, current_app.config['UPLOAD_FOLDER'])
            zip_file.close()
            return file_path
        except Exception as e:
            current_app.logger.warning(e.args)
            raise e

    @classmethod
    def check_csv_file(cls) -> dict:
        file_path = cls.upload_zip_file()
        result: dict = {'successfully': []}
        with open(file_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')  # type: ignore[union-attr]
            for line_decode in spamreader:
                try:
                    if line_decode[0] in result['successfully']:
                        raise ValueError('Url is duplicate in file.')
                    else:
                        Link(line_decode[0])
                        result['successfully'].append(line_decode[0])
                except Exception as e:
                    result.update({line_decode[0]: e.args})
        os.remove(file_path)
        return result

    @classmethod
    def post_links(cls, api=True):
        # Модифицировал для web и api варианта.
        if api:
            try:
                if 'file' not in request.files:
                    return jsonify('Need file in "form-data" key "file" - value "<*.zip>"'), HTTP.BAD_REQUEST
                result = cls.check_csv_file()
                post_urls.delay(result['successfully'])
                result['successfully'] = len(result['successfully'])
                return jsonify(result), HTTP.ACCEPTED
            except Exception as e:
                return jsonify(e.args), HTTP.BAD_REQUEST
        # Для web варианта.
        result = cls.check_csv_file()
        post_urls.delay(result['successfully'])
        result['successfully'] = len(result['successfully'])
        return result

    @classmethod
    def post_image(cls, link_id):
        try:
            if 'file' not in request.files:
                return jsonify('Need file in "form-data" key "file" - value "<*.jpeg or png or jpg>"'), HTTP.BAD_REQUEST
            file = request.files['file']
            link_obj = db_session.scalar(select(Link).filter(Link.id == link_id).limit(1))
            if not link_obj:
                return jsonify('Link by id not found'), HTTP.NOT_FOUND
            link_obj.filename = file.filename
            link_obj.filedata = file.stream.read()
            db_session.commit()
            file_logger.info('Image for url id - %s added/update.', link_obj.id)
            return jsonify('File appended/updated.'), HTTP.OK
        except Exception as e:
            db_session.rollback()
            return jsonify(e.args), HTTP.BAD_REQUEST


    @classmethod
    def post_image_web(cls, link_id):
        # web вариант
        if 'file' not in request.files:
            raise FileNotFoundError('File not found.')
        file = request.files['file']
        if not file.filename.endswith(('.jpeg', '.jpg', '.png')):
            raise ValueError('Only .jpeg .jpg .png file')
        link_obj = db_session.scalar(select(Link).filter(Link.id == link_id))
        if not link_obj:
            raise ValueError('Link by id not found')
        db_session.add(Event(link_id=link_obj.id, url=link_obj.get_url(), event=f'added image'))
        link_obj.filename = file.filename
        link_obj.filedata = file.stream.read()
        db_session.commit()
        file_logger.info('Image for url id - %s added/update.', link_obj.id)


    @staticmethod
    def filter_dict() -> dict:
        """Парсит и формирует словарь для фильтра в SQL."""
        filter_dict: dict[str, Any] = {}
        _id = request.args.get('id', type=str, default=None)
        suffix = request.args.get('domain_zone', type=str, default=None)
        available = request.args.get('available', type=bool, default=None)
        if _id:
            filter_dict.update({'id': _id})
        if suffix:
            filter_dict.update({'suffix': suffix})
        if available is not None:
            filter_dict.update({'available': available})
        return filter_dict

    @staticmethod
    def convert_list(list_links: list[Link]) -> list:
        """Формирует список для ответа."""
        links: list[dict[str, Any]] = []
        for link in list_links:
            links.append({'id': link.id, 'url': link.get_url(), 'status': link.linkstatus})
        return links

    @classmethod
    def get_urls(cls):
        page = request.args.get('page', type=int, default=0)
        size = request.args.get('size', type=int, default=5)
        filter_dict = cls.filter_dict()
        link_objs = db_session.scalars(select(Link).limit(size)
                                       .offset(page * size).filter_by(**filter_dict)).all()
        links = cls.convert_list(link_objs)
        return jsonify(links), HTTP.OK

    @classmethod
    def get_logs(cls):
        with open(settings.app.logger.file, newline='',
                  encoding=settings.app.logger.encoding) as log_file:
            return jsonify([i.rstrip() for i in list(log_file)[-settings.app.logger.count:]]), HTTP.OK
