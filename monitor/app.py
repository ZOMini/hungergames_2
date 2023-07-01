import logging
from http import HTTPStatus as HTTP

from flask import Response, jsonify, request

from api.v1.auth import auth
from api.v1.monitor import monitor
from core.app import app
from core.docs import init_docs
from services.jwt_service import *  # Регистрируем JWT

app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(monitor, url_prefix="/api/v1/monitor")
init_docs()

@app.errorhandler(Exception)
def handle_exception(e: Exception):
    return jsonify(e.args), HTTP.BAD_REQUEST

@app.after_request
def logAfterRequest(response: Response):
    logging.getLogger('file').info(
        "path: %s | method: %s | status: %s | size: %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
    )
    return response


if __name__ == '__main__':
    app.run()
