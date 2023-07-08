from flask import jsonify, render_template, request

from core.app import app


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# @app.errorhandler(InvalidAPIUsage)
# def invalid_api_usage(e):
#     return jsonify(e.to_dict()), e.status_code

def error_500(e):
  return render_template('500.html'), 500

def error_400(e):
  return render_template('400.html'), 400

def error_404(e):
  return render_template('404.html'), 404
