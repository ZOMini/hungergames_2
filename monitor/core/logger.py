import logging
import queue
import re
import sys
from logging.config import dictConfig
from logging.handlers import QueueListener, RotatingFileHandler

from werkzeug import serving

from core.config import settings

dictconfig = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        "size-rotate": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": settings.app.logger.file,
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "loggers": {
        "file": {
            "level": "INFO",
            "handlers": ["size-rotate"],
            "propagate": False,
        },
        "console": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def disable_endpoint_logs():
    """Disable logs for requests to specific endpoints."""
    disabled_endpoints = ('/web/logs', '/bootstrap/static')
    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if not any(re.match(f"{de}$", self.path) for de in disabled_endpoints):
            parent_log_request(self, *args, **kwargs)
    serving.WSGIRequestHandler.log_request = log_request


def init_loggers(answer=False):
    log_queue = queue.Queue()
    file_logger = logging.getLogger('file')
    console_logger = logging.getLogger('console')
    file_logger.setLevel(logging.INFO)
    console_logger.setLevel(logging.INFO)
    handler_file = RotatingFileHandler(settings.app.logger.file, maxBytes=1024 * 1024)
    handler_console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_file.setFormatter(formatter)
    handler_console.setFormatter(formatter)
    file_logger.addHandler(handler_file)
    console_logger.addHandler(handler_console)
    queue_listener = QueueListener(log_queue, handler_file)
    queue_listener.start()
    disable_endpoint_logs()
    if answer:
        return console_logger, file_logger
    # dictConfig(dictconfig)


console_logger, file_logger = init_loggers(True)
