#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm changing module for World of Warcraft,
using tkinter
"""

__version__ = '1.0.0'
__copyright__ = 'Copyright (C) 2025 grandatlant'

import os
import sys
import tkinter as tk

import logging
log = logging.getLogger()#__name__)#root logger by default. Configured later

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        '''no-op, default environment'''
        log.warning('Failed to import dotenv. Using default environment')

# Environment update first
load_dotenv()

DEF_SETTINGS_FILENAME = os.getenv('DEF_SETTINGS_FILENAME',
                                  os.path.join('.','realm.json'))

def use_btn_cmd():
    log.debug('Use Button command')
def add_btn_cmd():
    log.debug('Add Button command')
def rmv_btn_cmd():
    log.debug('Remove Button command')
def clr_btn_cmd():
    log.debug('Clear Button command')

def configure_logger(level=logging.ERROR, **kwds):
    '''Configure logging basicConfig and return logger to use in module'''
    # Settings for default environment
    log_config = {
        'level': level,
        'style': '{',
        'format': '{levelname}: {message}',
        #format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        }
    
    log_style = os.getenv('LOG_STYLE', '{')
    log_format = os.getenv('LOG_FORMAT', None)
    if log_format:
        log_config['style'] = log_style
        log_config['format'] = log_format
        
    log_file_name = os.getenv('LOG_FILE_NAME', None)
    log_file_mode = os.getenv('LOG_FILE_MODE', 'a')
    if log_file_name:
        log_config['filename'] = log_file_name
        log_config['filemode'] = log_file_mode

    # Read all possible other kwargs to update config.
    # force, handlers, or all others filled here can be overriden
    log_config.update(kwds)
    
    logging.basicConfig(**log_config)
    
    return logging.getLogger(__name__)

def build_ui(parent):
    main_frame = tk.Frame(parent, relief='ridge', borderwidth=5)
    main_frame.pack(fill='both', expand=1)
    
    label = tk.Label(main_frame, text="--- Main frame for UI ---")
    label.pack(fill='x', expand=1)

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill='x', expand=1)
    use_btn = tk.Button(btn_frame, text='Use', command=use_btn_cmd)
    use_btn.grid(row=1, column=1)
    add_btn = tk.Button(btn_frame, text='Add', command=add_btn_cmd)
    add_btn.grid(row=1, column=2)
    rmv_btn = tk.Button(btn_frame, text='Remove', command=rmv_btn_cmd)
    rmv_btn.grid(row=1, column=3)
    clr_btn = tk.Button(btn_frame, text='Clear', command=clr_btn_cmd)
    clr_btn.grid(row=1, column=4)

    lst_frame = tk.Frame(main_frame)
    lst_frame.pack(fill='both', expand=1)
    
    exit_button = tk.Button(main_frame, text="Exit", command=parent.destroy)
    exit_button.pack(side='bottom')
    
    return main_frame

##  MAIN ENTRY POINT
def main(args=None):
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    log_lvl = logging.DEBUG if __debug__ else logging.WARNING
    log = configure_logger(log_lvl)
    sys.exit(main(sys.argv))
