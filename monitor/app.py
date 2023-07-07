import re

from flask import Response, request

from api.v1.auth import auth
from api.v1.monitor import monitor
from core.app import app
from core.docs import init_docs
from core.logger import console_logger, file_logger
from services.jwt_service import *  # Регистрируем JWT
from web.auth import web_auth
from web.pages import pages

app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(monitor, url_prefix="/api/v1/monitor")
app.register_blueprint(pages, url_prefix="/web")
app.register_blueprint(web_auth, url_prefix='/web/auth')
init_docs()


@app.after_request
def logAfterRequest(response: Response):
    _ignore = ('/web/logs', '/web/events', '/bootstrap/static')
    if not any(re.match(f"{de}$", request.path) for de in _ignore):
        file_logger.info(
            "path: %s | method: %s | status: %s | size: %s",
            request.path,
            request.method,
            response.status,
            response.content_length,
        )
    return response


if __name__ == '__main__':
    app.run()
