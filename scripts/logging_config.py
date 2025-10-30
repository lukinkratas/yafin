from logging.config import dictConfig


def configure_logging() -> None:
    """Configure logging."""
    cfg = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': (
                    '%(asctime)s | %(levelname)-8s | %(name)-12s | '
                    '%(filename)s:%(lineno)d | %(funcName)s | %(message)s'
                ),
            },
            'simple': {
                'format': '%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'main.log',
                'formatter': 'default',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
            },
        },
    }
    dictConfig(cfg)
