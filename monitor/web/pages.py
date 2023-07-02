import logging

from flask import (
    Blueprint,
    redirect,
    render_template,
    render_template_string,
    request,
    url_for
)
from flask_jwt_extended import jwt_required
from sqlalchemy import select

from core.config import settings
from db.connection_db import db_session
from db.models_db import Link
from services.web_monitor_service import WebMonitorService

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    links = db_session.scalars(select(Link)).all()
    db_session.close()
    return render_template('index.html', links=links)

@pages.route('/<string:link_id>')
def get_link(link_id):
    link = db_session.scalar(select(Link).filter(Link.id == link_id).limit(1))
    db_session.close()
    return render_template('link.html', link=link)

@pages.route('/new_link', methods=['GET', 'POST'])
def new_link():
    if request.method == 'POST':
        # logging.getLogger('console').info('Url - %s error else.', request.files)
        try:
            if 'url' in request.form:
              logging.getLogger('console').info('Url - %s error else.', 'AAAAAAAAAAAAAAA')
              # logging.getLogger('console').info('Url - %s error add.', request.form['url'])
              link_obj = Link(request.form['url'])
              db_session.add(link_obj)
              db_session.commit()
            elif 'file' in request.files:
              # logging.getLogger('console').info('Url - %s error else.', request.files['file'])
              result = WebMonitorService.post_links()
              return render_template_string(str(result))
        except Exception as e:
            logging.getLogger('console').info('Url - %s error add.', e.args)
            db_session.rollback()
            return render_template_string(str(e.args))
        return redirect(url_for('pages.index'))
    return render_template('add_links.html')
