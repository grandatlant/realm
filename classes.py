#!/usr/bin/env -S python3
# -*- coding=utf-8 -*-
"""
Realm control classes module
"""

DEF_SETTINGS_FILENAME = './realm.json'

class BaseRealmEntry(dict):
    pass

class RealmEntry(BaseRealmEntry):
    pass

class BaseRealmCollection(list):
    def __init__(self, iterable = ()):
        super().__init__(iterable)
        self._itemType = BaseRealmEntry

class RealmCollection(BaseRealmCollection):
    def __init__(self, itemType = BaseRealmEntry):
        super().__init__()
        self._itemType = itemType

class RealmCollectionFactory:
    @staticmethod
    def create():
        return RealmCollection(RealmEntry)

class BaseSettings:
    def __init__(self, filename: str = '', /):
        self._filename = filename if filename else DEF_SETTINGS_FILENAME
        self._realms = RealmCollectionFactory.create()

class RealmSettings(BaseSettings):
    """ Container for script saved settings """
    def __init__(self, filename: str = '', *args, **kwargs):
        super().__init__(filename, *args, **kwargs)
        if filename:
            self._filename = filename
        for attr in kwargs:
            if hasattr(self, attr):
                # No any changes for attributes already exists
                #raise AttributeError
                pass
            else:
                setattr(self, attr, kwargs[attr])
    def load(self):
        """ Loads settings from file """
        pass
    def save(self):
        """ Saves settings to file """
        pass



if __name__ == '__main__':
    """ Debug code """
    sets = RealmSettings()

    print('sets = RealmSettings()');
    print(sets)
    print('vars(sets) = ', vars(sets))
