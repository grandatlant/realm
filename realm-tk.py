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

class MainFrame:
    """Main GUI frame class."""
    def __init__(self, parent, *args, **kwds):
        #super().__init__(parent, *args, **kwds)
        self.parent = parent
        
        self.main_frame = tk.Frame(
            self.parent,
            relief='ridge',
            borderwidth=5,
        )
        self.main_frame.pack(fill='both', expand=1)
        
        self.label = tk.Label(
            self.main_frame,
            text="--- Main frame for UI ---",
        )
        self.label.pack(fill='x', expand=1)

        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.pack(fill='x', expand=1)
        
        self.use_btn = tk.Button(
            self.btn_frame,
            text='Use',
            command=self.use_btn_cmd,
        )
        self.use_btn.grid(row=1, column=1)
        self.add_btn = tk.Button(
            self.btn_frame,
            text='Add',
            command=self.add_btn_cmd,
        )
        self.add_btn.grid(row=1, column=2)
        self.rmv_btn = tk.Button(
            self.btn_frame,
            text='Remove',
            command=self.rmv_btn_cmd,
        )
        self.rmv_btn.grid(row=1, column=3)
        self.clr_btn = tk.Button(
            self.btn_frame,
            text='Clear',
            command=self.clr_btn_cmd,
        )
        self.clr_btn.grid(row=1, column=4)

        self.lst_frame = tk.Frame(self.main_frame)
        self.lst_frame.pack(fill='both', expand=1)

        self.realm_listbox = tk.Listbox(
            self.lst_frame,
            listvariable=tk.Variable(
                value=['1', '2', 'foo', 'bar'],
            ),
        )
        self.realm_listbox.pack(fill='both')
        
        self.exit_button = tk.Button(
            self.main_frame,
            text="Exit",
            command=self.parent.destroy,
        )
        self.exit_button.pack(side='bottom', fill='x')
        
    def use_btn_cmd(self):
        log.debug('Use Button command')
        print(self.realm_listbox.curselection())
        
    def add_btn_cmd(self):
        log.debug('Add Button command')
        
    def rmv_btn_cmd(self):
        log.debug('Remove Button command')
        
    def clr_btn_cmd(self):
        log.debug('Clear Button command')
        


##  MAIN ENTRY POINT
def main(args=None):
    root = tk.Tk()
    root.title('realm-tk')
    MainFrame(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
