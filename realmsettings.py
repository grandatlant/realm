#!/usr/bin/env -S python3
# -*- coding = utf-8 -*-
"""
Classes and functions for RealmSettings
"""

import json
from sys import stderr

# Constants for realm entry keys
_NAME = 'name'
_STRINGS = 'strings'
_HIDDEN = 'hidden'

def create_realm_entry(name, /, strings = None, *, hidden = False, **kwds):
    keys = _NAME, _STRINGS, _HIDDEN
    vals = name, (strings if strings else []), hidden
    entry = dict(zip(keys, vals))
    entry.update(kwds) ## for future usage if I need it
    return entry

class RealmSettings:
    r"""File-supported RealmSettings with context-managing protocol"""
    __slots__ = '_filename', '_realms'
    
    def __init__(self, filename = None, /, *args, **kwds):
        super().__init__()
        self._filename = filename if filename else self.default_file_name()
        self._realms = dict()

    @staticmethod
    def default_file_name():
        return 'RealmSettings.json'

    @property
    def filename(self):
        return self._filename
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
        return (True if (name in self.realms) else False)

    def add(self, name, strings = None):
        entry = create_realm_entry(name, strings)
        self.realms[name] = entry
        return entry
    def remove(self, name):
        return self.pop(name, False)
    
    def realm_name(self, name):
        #return name ## TODO: Think about it
        if self.have_realm(name):
            return self.realms[name][_NAME]
        else:
            return '' ## TODO: Think about it
    def realm_strings(self, name):
        if self.have_realm(name):
            return self.realms[name][_STRINGS]
        else:
            return [] ## TODO: Think about it
    def realm_hidden(self, name):
        if self.have_realm(name):
            return self.realms[name][_HIDDEN]
        else:
            return None ## TODO: Think about it
    
    def show(self, name):
        if self.have_realm(name):
            self.realms[name][_HIDDEN] = False
            return True
    def hide(self, name):
        if self.have_realm(name):
            self.realms[name][_HIDDEN] = True
            return True
            
    def load(self):
        try:
            with open(self._filename, 'rt') as f:
                self._realms = dict(json.load(f))
        except OSError as ex:
            print(f"Can't load {self._filename}: {ex}", file = stderr)
    def save(self):
        with open(self._filename, 'wt') as f:
            json.dump(self._realms, f)

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
