import logging.config
import sys
import os


def setup_logging():
    is_lambda = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

    handlers_list = ["console"]

    if not is_lambda:
        handlers_list.append("file")

    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": "pipeline.log",
                "mode": "a",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": handlers_list,
                "level": "INFO",
                "propagate": True,
            },
            "httpx": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "httpcore": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOG_CONFIG)
