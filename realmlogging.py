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

import os
import logging

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        """dotenv module is missing. no-op, default environment."""
        return None#False##TODO: Think about it

# Environment update first
load_dotenv()

def configure_logger(level=logging.ERROR, **kwds):
    '''Configure logging basicConfig and return logger to use in module'''
    # Settings for default environment
    log_config = {
        'force': True,
        'level': level,
        'style': os.getenv('LOG_STYLE', '{'),
        'format': os.getenv('LOG_FORMAT', '{levelname}: {message}'),
        #format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        }

    log_file_name = os.getenv('LOG_FILE_NAME', None)
    if log_file_name:
        log_config['filename'] = log_file_name
        log_config['filemode'] = os.getenv('LOG_FILE_MODE', 'a')

    # Read all possible other kwargs to update config.
    # force, handlers, or all others filled here can be overriden
    log_config.update(kwds)
    
    logging.basicConfig(**log_config)
    
    return logging.getLogger(__name__)

log_lvl = logging.DEBUG if __debug__ else logging.WARNING
log = configure_logger(log_lvl)
