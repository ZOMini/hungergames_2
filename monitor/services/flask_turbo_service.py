import time

from flask import render_template

from core.app import app, db, turbo
from core.config import settings
from db.models_db import Event
from web.pagination import PageResult


def update_logs():
    def inject_logs_sub():
        with open(settings.app.logger.file, newline='',
                encoding=settings.app.logger.encoding) as log_file:
            listing = [i.rstrip() for i in log_file.readlines()[-20:]]  # Последние 20 строк логов.
            listing.reverse()
        listing=PageResult(listing, 1)
        return {'listing': listing}
    with app.app_context():
        while True:
            time.sleep(3)
            turbo.push(turbo.replace(render_template('logs_sub.html', **inject_logs_sub()), 'logs_sub'))


def update_events():
    def inject_events_sub():
        pagination = db.paginate(db.select(Event).order_by(Event.timestamp.desc()), page=1, per_page=10)
        events = pagination.items
        titles = [('timestamp', 'Time'), ('url', 'Url'), ('event', 'Event')]
        data = []
        for event in events:
            data.append({'timestamp': event.timestamp, 'url': event.url, 'event': event.event})
        return {'events': data, 'titles': titles}
    with app.app_context():
        while True:
            time.sleep(3)
            turbo.push(turbo.replace(render_template('events_sub.html', **inject_events_sub()), 'events_sub'))
