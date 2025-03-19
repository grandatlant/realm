#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Classes and functions for RealmSettings
"""

import json
from sys import stderr
from os.path import join as path_join
from enum import unique, Enum

@unique
class EntryField(str, Enum):
    NAME = 'name'
    HIDDEN = 'hidden'
    STRINGS = 'strings'

class RealmSettings:
    r"""File-supported RealmSettings with context-managing protocol"""
    __slots__ = '_filename', '_wow_path', '_realms'

    def __init__(self, filename = None, /, *args, **kwds):
        ##super().__init__()
        self._filename = filename or self.default_file_name()
        self._wow_path = self.default_wow_path()
        self._realms = dict()
    
    @staticmethod
    def default_file_name():
        return path_join('RealmSettings.json')
    @staticmethod
    def default_wow_path():
        return path_join('..')
    @staticmethod
    def create_realm_entry(name, strings = None, /,*, hidden = False, **kwds):
        keys = EntryField.NAME, EntryField.HIDDEN, EntryField.STRINGS
        vals = name, hidden, strings or []
        entry = dict(zip(keys, vals))
        entry.update(kwds) ## for future usage if I need it
        return entry
    
    @property
    def filename(self):
        return self._filename
    @property
    def realmlist_filename(self):
        return path_join(self._wow_path, 'Data', 'enUS', 'realmlist.wtf')
    @property
    def realms(self):
        return self._realms
    
    def __contains__(self, key, /):
        return self.realms.__contains__(key)
    def __getitem__(self, key, /):
        return self.realms.__getitem__(key)
    def __setitem__(self, key, value, /):
        return self.realms.__setitem__(key, value)
    
    def get(self, name, default = None):
        return self.realms.get(name, default)
    def pop(self, name, default = None):
        return self.realms.pop(name, default)

    def have_realm(self, name):
        return (name in self.realms)

    def add(self, name, strings = None):
        entry = self.create_realm_entry(name, strings)
        self.realms[name] = entry
        return entry
    def remove(self, name):
        return self.realms.pop(name, False)
    
    def realm_name(self, name):
        return self.realms.get(name, {}).get(EntryField.NAME, '')
    def realm_strings(self, name):
        return self.realms.get(name, {}).get(EntryField.STRINGS, [])
    def realm_hidden(self, name):
        return self.realms.get(name, {}).get(EntryField.HIDDEN, None)
    
    def show(self, name):
        if self.have_realm(name):
            self.realms[name][EntryField.HIDDEN] = False
            return True
        return False
    def hide(self, name):
        if self.have_realm(name):
            self.realms[name][EntryField.HIDDEN] = True
            return True
        return False
    
    def load(self):
        try:
            with open(self.filename, 'rt') as f:
                sets = dict(json.load(f))
                self._wow_path = sets.get('wow_path', self._wow_path)
                self._realms.clear()
                self._realms.update(sets.get('realms', {}))
        except OSError as ex:
            print(f"Can't load {self._filename}: {ex}", file = stderr)
    def save(self):
        with open(self.filename, 'wt') as f:
            sets = dict()
            sets['wow_path'] = self._wow_path
            sets['realms'] = self._realms
            json.dump(sets, f)
    
    def __enter__(self):
        self.load()
        return self
    def __exit__(self, exc_type = None, exc_value = None, traceback = None):
        if not exc_type:
            self.save()
            return True
    

##  MAIN ENTRY POINT  ##
def main():
    #return None
    from pprint import pprint as pp
    with RealmSettings() as sets:
        print(f'{sets.default_file_name() = }')
        print(f'{sets.default_wow_path() = }')
        print(f'{sets.realmlist_filename = }')
        print(f'Initial settings for default {sets.filename}')
        pp(sets.realms)

        print('Processing default realms...')
        sets.add('warmane', ['set realmlist logon.warmane.com'])
        sets.add('wowcircle', ['set realmlist logon.wowcircle.me'])
        sets.add('uwow', ['set realmlist login.uwow.biz',
                          'set realmlist login2.uwow.biz',
                          'set realmlist login3.uwow.biz',
                          'set realmlist login4.uwow.biz'])
        print('Settings filled.')
        pp(sets.realms)

if __name__ == '__main__':
    main()
