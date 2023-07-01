import logging

from app_celery.celery import app
from core.logger import init_loggers
from db.connection_db import db_session
from db.models_db import Link


@app.task
def post_urls(urls: list):
    init_loggers()
    list_objs: list[Link] = []
    for link in urls:
        list_objs.append(Link(link))
    db_session.add_all(list_objs)
    db_session.commit()
    logging.getLogger('file').info('Celery post urls - %s', list_objs)
