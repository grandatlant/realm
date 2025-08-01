#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Classes and functions for RealmSettings
"""

__version__ = '1.2.3'

__all__ = [
    'EntryField',
    'DefaultFactory',
    'SettingsData',
    'BaseSettings',
    'CoreSettings',
    'Saveable',
    'Loader',
    'Dumper',
    'SettingsContextManager',
    'RealmSettings',
]

import sys
from os.path import abspath, join as path_join, exists as path_exists

import json
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from typing import (
    IO,
    TextIO,
    Protocol,
    runtime_checkable,
    Union,
    Optional,
)

class EntryField(str, Enum):
    NAME = 'name'
    HIDDEN = 'hidden'
    STRINGS = 'strings'


class DefaultFactory:
    """Factory methods for module use"""
    __slots__ = ()
    
    @staticmethod
    def filename():
        return path_join('.', 'DefaultSettings.json')
    
    @staticmethod
    def realmlist():
        return path_join('..', 'Data', 'enUS', 'realmlist.wtf')
    
    @staticmethod
    def realms():
        return dict()
    
    @staticmethod
    def realm_entry(name,
                    /,
                    strings=None,
                    *,
                    hidden=False,
                    **kwds):
        """Creates new dict() with keys from EntryField Enum, 
        filled with function params"""
        keys = EntryField.NAME, EntryField.HIDDEN, EntryField.STRINGS
        vals = name, hidden or False, strings or []
        entry = dict(zip(keys, vals))
        entry.update(kwds) ## for future usage if I need it
        return entry


#@runtime_checkable
class ItemAccessBase(Protocol):
    """Item access interface"""
    __slots__ = ()
    
    @abstractmethod
    def __contains__(self, key, /): return False
    @abstractmethod
    def __getitem__(self, key, /): return None
    @abstractmethod
    def __setitem__(self, key, value, /): pass
    @abstractmethod
    def __delitem__(self, key, /): pass
    @abstractmethod
    def __iter__(self, /): return DefaultFactory.realms().__iter__()
    
    @abstractmethod
    def get(self, name, default=None, /): return default
    @abstractmethod
    def pop(self, name, default=None, /): return default
    @abstractmethod
    def popitem(self, /): raise KeyError(f'{self.__class__} have no items')
    @abstractmethod
    def clear(self, /): return None


@dataclass
class SettingsData(ItemAccessBase):
    """Dataclass for Settings fields"""
    __filename: str = field(
        default_factory=DefaultFactory.filename,
    )
    @property
    def filename(self):
        return self.__filename
    
    __realmlist: str = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=DefaultFactory.realmlist,
    )
    @property
    def realmlist(self):
        return self.__realmlist
    @realmlist.setter
    def realmlist(self, value):
        ## TODO: Validate ?
        self.__realmlist = value

    __realms: dict = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=DefaultFactory.realms,
    )
    @property
    def realms(self):
        return self.__realms
    
    def __post_init__(self):
        pass
    
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
    
    def get(self, name, default=None):
        return self.realms.get(name, default)
    def pop(self, name, default=None):
        return self.realms.pop(name, default)
    def popitem(self):
        return self.realms.popitem()
    def clear(self):
        return self.realms.clear()


class BaseSettings(ItemAccessBase):
    """BaseSettings interface"""
    __slots__ = ()
    
    def have_realm(self, name, /):
        return (name in self)
    def realm_entry(self, name, /):
        return self.get(name, DefaultFactory.realm_entry(name))
    def realm_name(self, name, /):
        return self.realm_entry(name).get(EntryField.NAME, '')
    def realm_hidden(self, name, /):
        return self.realm_entry(name).get(EntryField.HIDDEN, None)
    def realm_strings(self, name, /):
        return self.realm_entry(name).get(EntryField.STRINGS, [])
    
    def add(self, name, strings = None, /):
        """Add or edit realm with 'name'.
        Return value: entry link"""
        entry = DefaultFactory.realm_entry(name, strings)
        self[name] = entry
        return entry
    
    def remove(self, name, /):
        """Remove realm 'name' for good
        Return value is removed entry link or False if failed"""
        return self.pop(name, False)
    
    def show(self, name):
        """Unmark realm 'name' as hidden"""
        if self.have_realm(name):
            self.realm_entry(name)[EntryField.HIDDEN] = False
            return True
        return False
    
    def hide(self, name):
        """Mark realm 'name' as hidden"""
        if self.have_realm(name):
            self.realm_entry(name)[EntryField.HIDDEN] = True
            return True
        return False
    
    @abstractmethod
    def use(self, name, /):
        """Push realm's 'strings' to 'realmlist.wtf' file"""
        return None


@runtime_checkable
class Saveable(Protocol):
    """save-load interface"""
    @abstractmethod
    def load(self, /, *args, **kwargs) -> bool:
        """Load settings. Return True if success."""
    @abstractmethod
    def save(self, /, *args, **kwargs) -> bool:
        """Save settings. Return True if success."""


@runtime_checkable
class Loader(Protocol):
    """Used to load objects from file."""
    @abstractmethod
    def load(self, /, file: IO, *args, **kwargs) -> object:
        """Used to load object from file.
        Return value - Loaded Object"""
        return object()


@runtime_checkable
class Dumper(Protocol):
    """Used to dump objects to file."""
    @abstractmethod
    def dump(self, /, obj: object, file: IO, *args, **kwargs) -> None:
        """Used to dump object to file."""


class _ProxyDescriptorBase(ABC):
    """Descriptor ABC to specify Loader and Dumper proxy-objects."""
    __slots__ = ('owner', 'name', 'object', 'args', 'kwargs')
    
    def __init__(
        self,
        obj: Union[Loader, Dumper],
        *args, **kwargs
    ) -> None:
        self.object: Union[Loader, Dumper] = obj
        self.args: tuple = args
        self.kwargs: dict = kwargs

    def __set_name__(self, owner, name):
        self.owner, self.name = owner, name

    @property
    def attrname(self):
        """Private attribute name for instance."""
        return '_' + self.name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        # obj._name or self
        return getattr(obj, self.attrname, self)
    
    @abstractmethod
    def __set__(self, obj, value):
        setattr(obj, self.attrname, value)


class DefaultLoader(_ProxyDescriptorBase, Loader):
    """Descriptor to specify Loader object"""

    def __set__(self, obj, value):
        if (isinstance(value, Loader)
            or hasattr(value, 'load') and callable(value.load)
        ):
            super().__set__(obj, value)
        else:
            raise ValueError('Loader must have callable "load" method!')

    def load(self, /,
             file: IO,
             *args, **kwargs) -> object:
        return self.object.load(
            file,
            *self.args,
            *args,
            **self.kwargs,
            **kwargs,
        )


class DefaultDumper(_ProxyDescriptorBase, Dumper):
    """Descriptor to specify Dumper object"""

    def __set__(self, obj, value):
        if (isinstance(value, Dumper)
            or hasattr(value, 'dump') and callable(value.dump)
        ):
            super().__set__(obj, value)
        else:
            raise ValueError('Dumper must have callable "dump" method!')

    def dump(self, /,
             obj: object,
             file: IO,
             *args, **kwargs) -> None:
        self.object.dump(
            obj,
            file,
            *self.args,
            *args,
            **self.kwargs,
            **kwargs,
        )


class CoreSettings(SettingsData, BaseSettings, Saveable):
    """File-supported RealmSettings"""
    
    # Default dependencies
    # IO object for printing OSErrors
    errfile: TextIO = sys.stderr
    # Object to call load(f) method for loading dict() from f
    loader: Loader = DefaultLoader(json)
    # Object to call dump(sets, f) method for saving dict() to f
    dumper: Dumper = DefaultDumper(json, indent=4)
    
    def use(self, name):
        """Push realm`s 'strings' to 'realmlist.wtf' file"""
        if self.have_realm(name) and path_exists(self.realmlist):
            try:
                with open(self.realmlist, 'wt') as rlfile:
                    for line in self.realm_strings(name):
                        rlfile.write(f'{line}\r\n')
            except OSError as ex:
                print(f"Can't use realm '{self.name}' "
                      "for realmlist file '{self.realmlist}': "
                      "{ex}", file = self.errfile)
                return False
            else:
                return True
        return False
    
    def load(self, /,
             loader: Optional[Loader] = None,
             *args, **kwargs) -> bool:
        """Load settings from file.
        Return value - True if succeed, False othervise"""
        loader = loader or self.loader
        try:
            with open(self.filename, 'r') as f:
                sets = dict(loader.load(f, *args, **kwargs))
        except OSError as ex:
            print(f"Can't load '{self.filename}': {ex}",
                  file = self.errfile)
        else:
            self.realmlist = sets.get('realmlist', self.realmlist)
            #self.realms.clear()
            self.realms.update(sets.get('realms', DefaultFactory.realms()))
            return True
        return False
    
    def save(self, /,
             dumper: Optional[Dumper] = None,
             *args, **kwargs) -> bool:
        """Save current settings to file.
        Return value - True if succeed, False othervise"""
        dumper = dumper or self.dumper
        sets = {
            'realmlist': self.realmlist,
            'realms':    self.realms,
        }
        try:
            with open(self.filename, 'w') as f:
                dumper.dump(sets, f, *args, **kwargs)
        except OSError as ex:
            print(f"Can't save '{self.filename}': {ex}",
                  file = self.errfile)
        else:
            return True
        return False


class SettingsContextManager(AbstractContextManager, Saveable):
    """Context manager for settings"""
    __slots__ = ()
    
    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self, exc_type = None, exc_value = None, traceback = None):
        if not any((exc_type, exc_value, traceback)):
            self.save()
        return None


class RealmSettings(CoreSettings, SettingsContextManager):
    """Settings with advanced features besides Core:
    context managing protocol with load-save methods apply"""
    

##  MAIN ENTRY POINT  ##
def main() -> int:
    if not __debug__: return 0
    
    from pprint import pprint as pp

    with RealmSettings() as sets:
        print(f'{sets.filename = }')
        print(f'{sets.realmlist = }')
        print('Realms:')
        pp(sets.realms)
        
        print('Processing default realms...')
        print('Add realm "warmane"...')
        sets.add('warmane', ['set realmlist logon.warmane.com'])
        print('Add realm "wowcircle"...')
        sets.add('wowcircle', ['set realmlist logon.wowcircle.me'])
        print('Add realm "uwow"...')
        sets.add('uwow', ['set realmlist login.uwow.biz',
                        'set realmlist login2.uwow.biz',
                        'set realmlist login3.uwow.biz',
                        'set realmlist login4.uwow.biz'])
        print('Hide realm "uwow"...')
        sets.hide('uwow')
        
        print('Test with "dummy" realm:')
        print('Add...')
        assert sets.add('dummy', ['set realmlist localhost'])
        print('Hide...')
        assert sets.hide('dummy')
        print('Show...')
        assert sets.show('dummy')
        print('Remove...')
        assert sets.remove('dummy')
        print('"dummy" test ok.')
        #print('Use "warmane" realm.')
        #assert sets.use('warmane')
        print('Save test:')
        assert sets.save()
        print('Save test OK.')
        print('Realms filled:')
        pp(sets.realms)
        
    return 0

if __name__ == '__main__':
    main()
