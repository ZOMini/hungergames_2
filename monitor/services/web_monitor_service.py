import csv
import logging
import os
import zipfile
from http import HTTPStatus as HTTP
from typing import Any

from flask import current_app, jsonify, request
from sqlalchemy import select

from app_celery.tasks import post_urls
from core.config import settings
from db.connection_db import db_session
from db.models_db import Link
from services.api_monitor_service import ApiMonitorService


class WebMonitorService():

    @staticmethod
    def post_one_link():
        pass

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
    def post_links(cls):
        try:
            if 'file' not in request.files:
                return jsonify('Need file in "form-data" key "file" - value "<*.zip>"'), HTTP.BAD_REQUEST
            result = cls.check_csv_file()
            post_urls.delay(result['successfully'])
            result['successfully'] = len(result['successfully'])
            return jsonify(result), HTTP.ACCEPTED
        except Exception as e:
            return jsonify(e.args), HTTP.BAD_REQUEST

