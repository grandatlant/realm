#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm changing module for World of Warcraft,
using PyQt5
"""

__version__ = '1.1.0'
__copyright__ = 'Copyright (C) 2025 grandatlant'

__all__ = [
    'MainFrame',
]

import os
import sys
import atexit
import operator

from realmlogging import log
from realmsettings import CoreSettings
from wrappers import log_perf_counter, wrap_with

from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtGui import (
    QIcon, QFont,
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QLabel,
)

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        """dotenv module is missing. no-op, default environment."""
        log.warning('Failed to import dotenv. Using default environment')
        return None#False##TODO: Think about it

# Environment update first
load_dotenv()

DEF_SETTINGS_FILENAME = os.getenv(
    'DEF_SETTINGS_FILENAME',
    os.path.join('.','realm.json'))
_settings_filename = DEF_SETTINGS_FILENAME
_settings_instance = CoreSettings(_settings_filename)

class MainWindow:
    """Main GUI window class."""
    @property
    def realm_list(self) -> list:
        """List of non-hidden realms in settings."""
        return [
            name
            for name in self.settings
            if not self.settings.realm_hidden(name)
        ]

    @property
    def list_variable(self) -> list:
        """String representation of realm_list property."""
        return [
            ''.join((
                name,
                ' (',
                r'\n'.join(self.settings.realm_strings(name)),
                ')',
            ))
            for name in self.realm_list
            #if name
        ]
    
    def __init__(
        self,
        app,
        settings = _settings_instance,
        *args, **kwds
    ) -> None:
        self.app = app
        self.settings = settings# or RealmSettings(DEF_SETTINGS_FILENAME)
        self.mainwindow = window = QMainWindow(*args, **kwds)
        
        window.setWindowTitle('realm')
        #self.setWindowIcon(QIcon('realm.jpg'))
        window.setGeometry(100, 100, 500, 300)
        
        self.label = QLabel("Main frame for UI", window)
        self.label.setFont(QFont('Arial', 20))
        self.label.setGeometry(0, 0, 500, 50)
        self.label.setStyleSheet(
            'color: red;'
            'background-color: #292929;'
            'font-style: italic;'
        )
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

    def show(self):
        """Delegate to QMainWindow.show()"""
        self.mainwindow.show()

    def _selected_realm_name(self):
##        selection = self.realm_listbox.curselection()
##        if selection:
##            selected_index = selection[0]
##            selected_name = self.realm_list[selected_index]
##            return selected_name
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
                #self.realm_listbox.configure(listvariable=self.list_variable)
            else:
                log.error('Failed to hide realm "%s".' % selected_name)
        else:
            log.debug('No selection, skip command.')
        
    def clr_btn_cmd(self):
        log.debug('Clear Button command')
    
@log_perf_counter
def load_settings():
    """Manual loading procedure."""
    return _settings_instance.load()

#@atexit.register
@log_perf_counter
def save_settings():
    """Manual saving procedure.
    Saving @atexit temporary disabled."""
    return _settings_instance.save()

   
##  MAIN ENTRY POINT
@wrap_with(load_settings, save_settings,
           return_filter_func = operator.not_)
def main(args=None):
    app = QApplication(args or [])
    
    mainwindow = MainWindow(app)
    mainwindow.show()

    result = app.exec_()
    
    return result

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
