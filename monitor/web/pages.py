import io
import logging

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    render_template_string,
    request,
    url_for
)
from sqlalchemy import select

from core.app import db
from core.config import settings
from db.connection_db import db_session
from db.models_db import Link
from services.api_monitor_service import ApiMonitorService
from web import form
from web.pagination import PageResult

pages = Blueprint('pages', __name__)


@pages.route('/link/<string:link_id>')
def get_link(link_id):
    link = db_session.scalar(select(Link).filter(Link.id == link_id))
    return render_template('link.html', link=link)


@pages.route('/new_link', methods=['GET', 'POST'])
def new_link():
    if request.method == 'POST':
        try:
            if 'url' in request.form:
              link_obj = Link(request.form['url'])
              db_session.add(link_obj)
              db_session.commit()
              flash('Url added.')
            elif 'file' in request.files:
              result = ApiMonitorService.post_links(False)
              flash(f'Urls from file added. - {str(result)}')
        except Exception as e:
            logging.getLogger('console').info('Url add error - %s', e.args)
            db_session.rollback()
            flash(str(e.args))
        # return redirect(url_for('pages.links'))
    return render_template('add_links.html', urlform=form.UrlButtonForm(), fileform=form.FileButtonForm())


@pages.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    _form = form.IdFileButtonForm(request.form)
    if request.method == 'POST':
        try:
            _form.validate()
            if 'file' in request.files and 'id' in request.form:
                id = request.form['id']
                ApiMonitorService.post_image(id, False)
                flash(f'Image for id {id} uploaded.')
            else:
                flash(f'Check id and file. {_form.errors}')
        except Exception as e:
            logging.getLogger('console').info('Image add error - %s.', e.args)
            db_session.rollback()
            flash(str(e.args))
    return render_template('add_image.html', id_file_form=form.IdFileButtonForm())


@pages.route('/logs', defaults={'pagenum': 1})
@pages.route('/logs/<int:pagenum>')
def logs(pagenum):
    with open(settings.app.logger.file, newline='',
              encoding=settings.app.logger.encoding) as log_file:
        logs_list = [i.rstrip() for i in log_file.readlines()]
        logs_list.reverse()
    return render_template('logs.html', listing=PageResult(logs_list, pagenum))


@pages.route('/', defaults={'page': 1})
@pages.route('/links', defaults={'page': 1})
@pages.route('/links/<int:page>')
def links(page):
    pagination = db.paginate(db.select(Link), page=page, per_page=10)
    links = pagination.items
    titles = [('id', 'id'), ('url', 'url'), ('linkstatus', 'linkstatus'), ('lasttime', 'lasttime')]
    data = []
    for link in links:
        url = link.get_url()
        data.append({'id': link.id, 'url': url, 'linkstatus': link.linkstatus, 'lasttime': link.lasttime})
    return render_template('links.html', titles=titles, Link=Link, data=data, links=links, pagination=pagination)


@pages.route('/links/<string:link_id>/view')
def view_link(link_id):
    link = db_session.scalar(select(Link).filter(Link.id == link_id))
    image = io.BytesIO(link.filedata)
    url = link.get_url()
    if link:
        return render_template('link.html', link=link, image=image, url=url)
    flash(f'Could not view link {link_id} as it does not exist.')
    return redirect(url_for('pages.links'))


@pages.route('/links/<string:link_id>/delete', methods=['POST'])
def delete_link(link_id):
    link = db_session.scalar(select(Link).filter(Link.id == link_id))
    if link:
        db_session.delete(link)
        db_session.commit()
        flash(f'Link {link_id} has been deleted.')
    else:
        flash(f'Link {link_id} did not exist and could therefore not be deleted.')
    return redirect(url_for('pages.links'))


@pages.route('/images/<string:pid>')
def get_image(pid):
    link = db_session.scalar(select(Link).filter(Link.id == pid))
    if link.filedata:
        response = make_response(link.filedata)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
        return response
    return {}
