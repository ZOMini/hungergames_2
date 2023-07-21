import logging
import re
import sys

from werkzeug import serving

from core.async_logging_handler import AsyncRotatingFileHandler
from core.config import settings


def disable_endpoint_logs():
    """Disable logs for requests to specific endpoints."""
    disabled_endpoints = ('/bootstrap/static/icons/bootstrap-icons.svg')
    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if not any(re.match(f"{de}$", self.path) for de in disabled_endpoints):
            parent_log_request(self, *args, **kwargs)
    serving.WSGIRequestHandler.log_request = log_request


def init_loggers(answer=False):
    file_logger = logging.getLogger('file')
    console_logger = logging.getLogger('console')
    file_logger.setLevel(logging.INFO)
    console_logger.setLevel(logging.INFO)
    handler_file = AsyncRotatingFileHandler(settings.app.logger.file, maxBytes=1024 * 1024, delay=False, backupCount=0)
    handler_console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_file.setFormatter(formatter)
    handler_console.setFormatter(formatter)
    file_logger.addHandler(handler_file)
    console_logger.addHandler(handler_console)
    disable_endpoint_logs()
    if answer:
        return console_logger, file_logger


console_logger, file_logger = init_loggers(True)
