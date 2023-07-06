from app_celery.celery import app
from core.logger import file_logger
from db.connection_db import db_session
from db.models_db import Link


@app.task
def post_urls(urls: list):
    list_objs: list[Link] = []
    for link in urls:
        list_objs.append(Link(link))
    db_session.add_all(list_objs)
    db_session.commit()
    file_logger.info('Celery post urls - %s', list_objs)
