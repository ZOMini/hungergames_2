from flask import request
from sqlalchemy import select

from app_celery.tasks import post_urls
from core.logger import file_logger
from db.connection_db import db_session
from db.models_db import Event, Link
from services.api_monitor_service import ApiMonitorService


class WebMonitorService(ApiMonitorService):

    @classmethod
    def post_links_web(cls):
        result = cls.check_csv_file()
        post_urls.delay(result['successfully'])
        result['successfully'] = len(result['successfully'])
        return result

    @classmethod
    def post_image_web(cls, link_id):
        if 'file' not in request.files:
            raise FileNotFoundError('File not found.')
        file = request.files['file']
        if not file.filename.endswith(('.jpeg', '.jpg', '.png')):
            raise ValueError('Only .jpeg .jpg .png file')
        link_obj = db_session.scalar(select(Link).filter(Link.id == link_id))
        if not link_obj:
            raise ValueError('Link by id not found')
        db_session.add(Event(link_id=link_obj.id, url=link_obj.get_url(), event='added image'))
        link_obj.filename = file.filename
        link_obj.filedata = file.stream.read()
        db_session.commit()
        file_logger.info('Image for url id - %s added/update.', link_obj.id)
