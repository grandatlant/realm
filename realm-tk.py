#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm changing module for World of Warcraft,
using tkinter
"""

__version__ = '1.1.0'
__copyright__ = 'Copyright (C) 2025 grandatlant'

__all__ = [
    'MainFrame',
]

import os
import sys
import atexit
import tkinter as tk

from realmlogging import log
from realmsettings import CoreSettings
from wrappers import log_perf_counter, wrap_with

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
_settings_filename = DEF_SETTINGS_FILENAME
_settings_instance = CoreSettings(_settings_filename)

class MainFrame:
    """Main GUI frame class."""
    @property
    def realm_list(self) -> list:
        """List of non-hidden realms in settings."""
        return [
            name
            for name in self.settings
            if not self.settings.realm_hidden(name)
        ]

    @property
    def list_variable(self) -> tk.Variable:
        """String representation of realm_list property for tkinter."""
        return tk.Variable(
            value=[
                ''.join((
                    name,
                    ' (',
                    r'\n'.join(self.settings.realm_strings(name)),
                    ')',
                ))
                for name in self.realm_list
                #if name
            ],
        )
    
    def __init__(
        self,
        parent: tk.Misc,
        settings = _settings_instance,
        *args, **kwds
    ) -> None:
        #super().__init__(parent, *args, **kwds)
        self.parent = parent
        self.settings = settings# or RealmSettings(DEF_SETTINGS_FILENAME)
        
        self.frame = tk.Frame(
            self.parent,
            relief='ridge',
            borderwidth=5,
        )
        self.frame.pack(fill='both', expand=1)
        
        '''self.label = tk.Label(
            self.frame,
            text="--- Main frame for UI ---",
        )
        self.label.pack(fill='x', expand=1)'''

        self.btn_frame = tk.Frame(self.frame)
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

        self.lst_frame = tk.Frame(self.frame)
        self.lst_frame.pack(fill='both', expand=1)
        
        self.realm_listbox = tk.Listbox(
            self.lst_frame,
            listvariable=self.list_variable,
        )
        self.realm_listbox.pack(fill='both')
        
        self.exit_button = tk.Button(
            self.frame,
            text="Exit",
            command=self.parent.destroy,
        )
        self.exit_button.pack(side='bottom', fill='x')

    def _selected_realm_name(self):
        selection = self.realm_listbox.curselection()
        if selection:
            selected_index = selection[0]
            selected_name = self.realm_list[selected_index]
            return selected_name
        return None
        
    def use_btn_cmd(self):
        log.debug('Use Button command')
        selected_name = self._selected_realm_name()
        if selected_name:
            if self.settings.use(selected_name):
                log.debug('Active realm "%s" used.' % selected_name)
            else:
                log.error('Failed to use realm "%s".' % selected_name)
        else:
            log.debug('No selection, skip command.')
        
    def add_btn_cmd(self):
        log.debug('Add Button command')
        
    def rmv_btn_cmd(self):
        log.debug('Remove Button command')
        selected_name = self._selected_realm_name()
        if selected_name:
            if self.settings.hide(selected_name):
                log.debug('Active realm "%s" made hidden.' % selected_name)
                # update list data
                self.realm_listbox.configure(listvariable=self.list_variable)
            else:
                log.error('Failed to hide realm "%s".' % selected_name)
        else:
            log.debug('No selection, skip command.')
        
    def clr_btn_cmd(self):
        log.debug('Clear Button command')

def load_settings():
    """Manual loading procedure."""
    return _settings_instance.load()

#@atexit.register
def save_settings():
    """Mock. Saving @atexit temporary disabled."""
    return _settings_instance.save()

##  MAIN ENTRY POINT
@wrap_with(load_settings, save_settings)
def main(args=None):
    root = tk.Tk()
    root.title('realm-tk')
    MainFrame(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
'''
else:
    try:
        if load_settings():
            atexit.register(save_settings)
    except Exception:
        pass
'''
