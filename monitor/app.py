import re
import threading

from flask import Response, request

from api.v1.auth import auth
from api.v1.monitor import monitor
from core.app import app
from core.docs import init_docs
from core.logger import console_logger, file_logger
from services.flask_turbo_service import update_events, update_logs
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
    threading.Thread(target=update_logs, daemon=True).start()
    threading.Thread(target=update_events, daemon=True).start()


if __name__ == '__main__':
    app.run()
