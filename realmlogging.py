#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm logging module
"""

__version__ = '1.0.0'
__copyright__ = 'Copyright (C) 2025 grandatlant'

__all__ = [
    'logging',
    'log',
    'log_lvl',
    'configure_logger',
]

import logging

try:
    from dotenv import dotenv_values
except ImportError:
    def dotenv_values(*a, **kw):
        """dotenv module is missing. no-op, default environment."""
        return dict()


def configure_logger(level=logging.ERROR, **kwds):
    '''Configure logging basicConfig and return logger to use in module'''
    env = dotenv_values()
    log_config = {
        #'force': True,
        'level': level,
        'style': env.get('LOG_STYLE', '{'),
        'format': env.get('LOG_FORMAT', '{levelname}: {message}'),
        #format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        }

    log_file_name = env.get('LOG_FILE_NAME', None)
    if log_file_name:
        log_config['filename'] = log_file_name
        log_config['filemode'] = env.get('LOG_FILE_MODE', 'a')

    # Read all possible other kwargs to update config.
    # force, handlers, or all others filled here can be overriden
    log_config.update(kwds)
    
    logging.basicConfig(**log_config)
    
    return logging.getLogger(__name__)


log_lvl = logging.DEBUG if __debug__ else logging.ERROR
log = configure_logger(log_lvl)
