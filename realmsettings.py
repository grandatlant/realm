#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Classes and functions for RealmSettings
"""

__version__ = '1.0.0'

__all__ = ['EntryField',
           'BaseSettings',
           'CoreSettings',
           'RealmSettings']

from sys import stderr as errfile, exit as sys_exit
from os.path import abspath, join as path_join, exists as path_exists

from json import load as json_load, dump as json_dump
from enum import Enum
from abc import ABC, abstractmethod

class EntryField(str, Enum):
    NAME = 'name'
    HIDDEN = 'hidden'
    STRINGS = 'strings'

class BaseSettings(ABC):
    """BaseSettings ABC interface"""
    __slots__ = ()
    
    ## Item access
    
    @abstractmethod
    def __contains__(self, key, /): return False
    @abstractmethod
    def __getitem__(self, key, /): return None
    @abstractmethod
    def __setitem__(self, key, value, /): pass
    @abstractmethod
    def __delitem__(self, key, /): pass
    @abstractmethod
    def __iter__(self, /): return {}.__iter__()
    
    # Safe item-getters
    
    @abstractmethod
    def get(self, name, default = None): return default
    @abstractmethod
    def pop(self, name, default = None): return default
    @abstractmethod
    def popitem(self): raise KeyError(f'{self.__class__} have no items')
    @abstractmethod
    def clear(self): return None
    

class CoreSettings(BaseSettings):
    """File-supported RealmSettings with context-managing protocol"""
    __slots__ = '_filename', '_realmlist', '_realms',
    
    def __init__(self, filename = None, /, *args, **kwds):
        """Initial instance fill"""
        self._filename = filename or self.default_filename()
        self._realmlist = self.default_realmlist()
        self._realms = dict()
        
    @classmethod
    def default_filename(cls) -> str:
        """Returns './{cls.__name__}.json'"""
        return path_join('.', cls.__name__+'.json')
    @staticmethod
    def default_realmlist() -> str:
        """Returns '../Data/enUS/realmlist.wtf'"""
        return path_join('..', 'Data', 'enUS', 'realmlist.wtf')
    @staticmethod
    def create_realm_entry(name, strings = None, /, *,
                           hidden = False, **kwds) -> dict:
        """Creates new dict() with keys from EntryField Enum, 
        filled with function params"""
        keys = EntryField.NAME, EntryField.HIDDEN, EntryField.STRINGS
        vals = name, hidden or False, strings or []
        entry = dict(zip(keys, vals))
        entry.update(kwds) ## for future usage if I need it
        return entry

    ## Propertys
    
    @property
    def realms(self):
        return self._realms
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def realmlist(self):
        return self._realmlist #abspath(self._realmlist)
    @realmlist.setter
    def realmlist(self, value):
        ## TODO: Validate ?
        self._realmlist = value #abspath(value)

    ## Delegated methods
    
    def __contains__(self, key, /):
        return self.realms.__contains__(key)
    def __getitem__(self, key, /):
        return self.realms.__getitem__(key)
    def __setitem__(self, key, value, /):
        return self.realms.__setitem__(key, value)
    def __delitem__(self, key, /):
        return self.realms.__delitem__(key)
    def __iter__(self):
        return self.realms.__iter__()
    
    def get(self, name, default = None):
        return self.realms.get(name, default)
    def pop(self, name, default = None):
        return self.realms.pop(name, default)
    def popitem(self):
        return self.realms.popitem()
    def clear(self):
        return self.realms.clear()

    ## Service methods
    
    def have_realm(self, name):
        return (name in self)
    def realm_name(self, name):
        return self.get(name, {}).get(EntryField.NAME, '')
    def realm_strings(self, name):
        return self.get(name, {}).get(EntryField.STRINGS, [])
    def realm_hidden(self, name):
        return self.get(name, {}).get(EntryField.HIDDEN, None)
    
    def add(self, name, strings = None):
        """Add or edit realm 'name'"""
        entry = self.create_realm_entry(name, strings)
        self.realms[name] = entry
        return entry
    def remove(self, name):
        """Remove realm 'name' for good"""
        return self.realms.pop(name, False)
    
    def show(self, name):
        """Unmark realm 'name' as hidden"""
        if self.have_realm(name):
            self.realms[name][EntryField.HIDDEN] = False
            return True
        return False
    def hide(self, name):
        """Mark realm 'name' as hidden"""
        if self.have_realm(name):
            self.realms[name][EntryField.HIDDEN] = True
            return True
        return False
    
    def use(self, name):
        r"""Push realm`s 'strings' to 'realmlist.wtf' file"""
        if self.have_realm(name) and path_exists(self.realmlist):
            with open(self.realmlist, 'wt') as rlfile:
                for line in self.realm_strings(name):
                    rlfile.write(f'{line}\r\n')
            return True
        return False
    
    def load(self):
        """Load settings from JSON file"""
        try:
            with open(self.filename, 'rt') as f:
                sets = dict(json_load(f))
                self.realmlist = sets.get('realmlist', self.realmlist)
                self.realms.clear()
                self.realms.update(sets.get('realms', dict()))
        except OSError as ex:
            print(f"Can't load {self._filename}: {ex}", file = errfile)
    def save(self):
        """Save current settings to JSON file"""
        try:
            with open(self.filename, 'wt') as f:
                sets = dict()
                sets['realmlist'] = self.realmlist
                sets['realms'] = self.realms
                json_dump(sets, f)
        except OSError as ex:
            print(f"Can't save {self._filename}: {ex}", file = errfile)

    ## Context methods
    
    def __enter__(self):
        self.load()
        return self
    def __exit__(self, exc_type = None, exc_value = None, traceback = None):
        if not any((exc_type, exc_value, traceback)):
            self.save()

class RealmSettings(CoreSettings):
    __slots__ = ()
    

##  MAIN ENTRY POINT  ##
def main() -> int:
    if not __debug__: return 0
    
    from pprint import pprint as pp
    with RealmSettings() as sets:
        print(f'{sets.default_filename() = }')
        print(f'{sets.default_realmlist() = }')
        print(f'{sets.filename = }')
        print(f'{sets.realmlist = }')
        print('Realms:')
        pp(sets.realms)
        
        print('Processing default realms...')
        sets.add('warmane', ['set realmlist logon.warmane.com'])
        sets.add('wowcircle', ['set realmlist logon.wowcircle.me'])
        sets.add('uwow', ['set realmlist login.uwow.biz',
                          'set realmlist login2.uwow.biz',
                          'set realmlist login3.uwow.biz',
                          'set realmlist login4.uwow.biz'])
        sets.hide('uwow')
        print('Settings filled.')
        pp(sets.realms)
        
    return 0

if __name__ == '__main__':
    sys_exit(main())
