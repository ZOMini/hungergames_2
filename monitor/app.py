import re
import threading

from flask import Response, request

from api.v1.auth import auth
from api.v1.monitor import monitor
from core.app import app, db
from core.docs import init_docs
from core.logger import console_logger, file_logger
from db.connection_db import engine
from services.flask_turbo_service import update_logs_and_events
from services.jwt_service import *  # Регистрируем JWT
from web.auth import web_auth
from web.pages import pages

app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(monitor, url_prefix="/api/v1/monitor")
app.register_blueprint(web_auth, url_prefix='/web/auth')
app.register_blueprint(pages, url_prefix="/web")

init_docs()


@app.after_request
def logAfterRequest(response: Response):
    _ignore = ('/bootstrap/static/icons/bootstrap-icons.svg', '/turbo-stream')  # '/web/logs', '/web/events'
    if not any(re.match(f"{de}$", request.path) for de in _ignore):
        file_logger.info(
            "path: %s | method: %s | status: %s | size: %s",
            request.path,
            request.method,
            response.status,
            response.content_length,
        )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response


with app.app_context():
    threading.Thread(target=update_logs_and_events, daemon=True).start()


def test_app():
    return app


if __name__ == '__main__':
    app.run()
