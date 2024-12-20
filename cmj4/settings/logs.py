
import inspect
import logging
import sys
import warnings

from decouple import AutoConfig
import yaml


config = AutoConfig()
LOGGING_ROOT_LEVEL = config('LOGGING_ROOT_LEVEL', default='INFO', cast=str)

logging.captureWarnings(True)
yaml.warnings({'YAMLLoadWarning': False})


class MyFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style='%'):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        s = logging.Formatter.format(self, record)

        for i in inspect.stack():
            r = i.frame.f_locals.get('request', None)
            if r:
                try:
                    url = r.path
                except:
                    url = ''
                return f'{s} - {url}'
        return s


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {
        'verbose': {
            'class': 'cmj4.settings.logs.MyFormatter',
            'format': '%(levelname)s %(asctime)s %(name)s:%(funcName)s:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'cmj_logger_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/cmj4_logger.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
            #'filters': ['require_debug_false'],
        },
    },
    'root': {
        'handlers': ['cmj_logger_file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['cmj_logger_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'haystack': {
            'handlers': ['cmj_logger_file', 'console'],
            'level': LOGGING_ROOT_LEVEL,
            'propagate': False,
        },
        'cmj': {
            'handlers': ['cmj_logger_file', 'console'],
            'level': LOGGING_ROOT_LEVEL,
            'propagate': False,
        },
        'sapl': {
            'handlers': ['cmj_logger_file', 'console'],
            'level': LOGGING_ROOT_LEVEL,
            'propagate': False,
        },
    },
}


def uncaught_exceptions(type, value, error_traceback):
    import traceback
    logger = logging.getLogger(__name__)
    error_msg = ''.join(traceback.format_tb(error_traceback))
    logger.error(f'{type}\n{value}\n{error_msg}')
    print(f'{type}\n{value}\n{error_msg}')


# captura exceções que não foram tratadas
sys.excepthook = uncaught_exceptions
