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


