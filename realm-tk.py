#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm changing module for World of Warcraft,
using tkinter
"""

__version__ = '1.0.1'
__copyright__ = 'Copyright (C) 2025 grandatlant'

import os
import sys
import tkinter as tk

from realmlogging import log

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        """dotenv module is missing. no-op, default environment."""
        log.warning('Failed to import dotenv. Using default environment')
        return None#False##TODO: Think about it

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
    sys.exit(main(sys.argv))
