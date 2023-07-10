from app_celery.celery import app
from core.logger import console_logger, file_logger
from db.connection_db import db_session
from db.models_db import Event, Link


@app.task
def post_urls(urls: list):
    list_objs: list[Link] = []
    list_events: list[Event] = []
    for link in urls:
        list_objs.append(Link(link))
    db_session.add_all(list_objs)
    db_session.commit()
    for link in list_objs:
        console_logger.info(link.id)
        list_events.append(Event(url=link.get_url(), event='url added', link_id=link.id))
    db_session.add_all(list_events)
    db_session.commit()     
    file_logger.info('Celery post urls, count - %s', len(list_objs))
