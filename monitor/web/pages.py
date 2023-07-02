
from flask import Blueprint
from flask_jwt_extended import jwt_required

from core.config import settings
from services.web_monitor_service import WebMonitorService

pages = Blueprint('pages', __name__)


@pages.route('/new_urls', methods=['GET', 'POST'])
@jwt_required(optional=settings.app.jwt.disabled_in_api)
def new_urls():
    response = WebMonitorService.post_one_link()
    return response
