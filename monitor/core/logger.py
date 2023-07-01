from logging.config import dictConfig

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


def init_loggers():
    dictConfig(dictconfig)
