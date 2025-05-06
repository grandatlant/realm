#!/usr/bin/env -S python3 -OO
# -*- coding=utf-8 -*-
"""
Realm changing module for World of Warcraft
"""

from argparse import ArgumentParser
from functools import wraps
from sys import exit as sys_exit

from realmsettings import RealmSettings
from clitools import confirm_action, readlines

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

__version__ = '1.1.2'
__copyright__ = 'Copyright (C) 2025 grandatlant'

DEF_SETTINGS_FILENAME = os.getenv('DEF_SETTINGS_FILENAME',
                                  os.path.join('.','realm.json'))

## Helper fucntions

def verbose_print(msg, /, verbosity = 1, min_level = 1):
    if verbosity >= min_level:
        print(msg)
def info_print(msg, verbosity):
    verbose_print(msg, verbosity, 2)

def check_settings(check_func):
    def decorator(func):
        @wraps(func)
        def wrapper(args, *func_args, **func_kwargs):
            if not check_func(args.settings):
                verbose_print('Settings check for file "' + 
                              args.settings + '" failed.', 
                              args.verbosity)
                return 1
            return func(args, *func_args, **func_kwargs)
        return wrapper
    return decorator

##  CLI stateless subroutines  ##

def _default(args):
    # no command specified. return soft error status
    return 1

@check_settings(os.path.exists)
def _list(args):    
    with RealmSettings(args.settings) as sets:
        for name in sets.realms:
            # condition to pass current realm
            if sets.realm_hidden(name):
                if not (args.all or args.hidden):
                    continue
            else:
                if args.hidden:
                    continue
            hidden_indicator = ('(hidden)'
                                if args.all and sets.realm_hidden(name)
                                else '')
            name_to_print = f'{hidden_indicator}{name}'
            print(name_to_print)
            if args.long:
                prefix = (f'{name_to_print} -> ' if args.verbosity else '')
                for string in sets.realm_strings(name):
                    print(f'{prefix}{string}')
    return 0

#@check_settings(os.path.exists)
def _add(args):
    with RealmSettings(args.settings) as sets:
        name = args.name
        if sets.have_realm(name) and not args.force:
            ## TODO : Think about verbosity and input here
            if not confirm_action('Realm '+name+' exists. Rewrite?(y/n)'):
                return 1
        
        strings = args.strings
        if not strings:
            verbose_print('Enter strings for realmlist.wtf. '
                          'EOF (ctrl+d) to finish', args.verbosity)
            strings = [got_string.strip()
                       for got_string in readlines()
                       if got_string]
        
        new_entry = sets.add(name, strings)
        if new_entry and args.verbosity:
            verbose_print('New entry for '+name+' done: {new_entry}',
                          args.verbosity)
    
    return 0

@check_settings(os.path.exists)
def _use(args):
    with RealmSettings(args.settings) as sets:
        while not os.path.exists(sets.realmlist):
            if confirm_action('Path "'+sets.realmlist+'" '
                              'to "realmlist.wtf" is not exists. '
                              'Change it? (y/n)'):
                sets.realmlist = input('Enter new path to "realmlist.wtf": ')
            else:
                return 1
        name = args.name
        if sets.have_realm(name):
            if sets.use(name):
                verbose_print('Realm "'+name+'" used for realmlist',
                              args.verbosity)
            else:
                verbose_print('Failed to use realm "'+name+'" '
                              'for '+sets.realmlist+' file',
                              args.verbosity)
                return 1
        else:
            verbose_print('Realm '+name+' not found to use.',
                          args.verbosity)
            return 1
    return 0

@check_settings(os.path.exists)
def _show(args):
    with RealmSettings(args.settings) as sets:
        names = args.names if args.names else readlines()
        for name in names:
            if sets.have_realm(name) and sets.show(name):
                verbose_print('Realm '+name+' marked as non-hidden',
                              args.verbosity)
            else:
                info_print('Realm '+name+' not found to show.',
                           args.verbosity)
    return 0

@check_settings(os.path.exists)
def _hide(args):
    with RealmSettings(args.settings) as sets:
        names = args.names if args.names else readlines()
        for name in names:
            if sets.have_realm(name) and sets.hide(name):
                verbose_print('Realm '+name+' marked as hidden',
                              args.verbosity)
            else:
                info_print('Realm '+name+' not found to hide.',
                           args.verbosity)
    return 0

@check_settings(os.path.exists)
def _remove(args):
    with RealmSettings(args.settings) as sets:
        names = args.names if args.names else readlines()
        for name in names:
            if sets.have_realm(name):
                confirmed = False
                if args.force:
                    confirmed = True
                else:
                    if args.verbosity and confirm_action(
                        'Confirm removing realm "'+name+'"?(y/n)'):
                        confirmed = True
                if confirmed and sets.remove(name):
                    verbose_print('Realm '+name+' removed.',
                                  args.verbosity)
            else:
                info_print('Realm '+name+' not found to remove.',
                           args.verbosity)
    return 0

def parse_cli_args():
    
    parser = ArgumentParser(description = __doc__,
                            allow_abbrev = False,
                            epilog = __copyright__)
    parser.set_defaults(func = _default)
    
    parser.add_argument('--version',
                        action = 'version',
                        version = f'%(prog)s {__version__}')
    parser.add_argument('-v','--verbose',
                        dest = 'verbosity',
                        action = 'count',
                        default = 0,
                        help = 'increase verbosity level. Quiet by default.')
    parser.add_argument('-s','--settings',
                        default = DEF_SETTINGS_FILENAME,
                        help = 'use settings from a .json file. '
                        f'File "{DEF_SETTINGS_FILENAME}" is used as default')
    
    ## COMMANDS
    
    subs = parser.add_subparsers(title = 'Commands',
                                 dest = 'command',
                                 description = 'main settings interface')
    
    # List
    
    command = subs.add_parser('list',
                              help = 'list realms')
    command.add_argument('-l','--long',
                         action = 'store_true', default = False,
                         help = 'list full information, not only names')
    cmdgroup = command.add_mutually_exclusive_group()
    cmdgroup.add_argument('--all',
                          action = 'store_true', default = False,
                          help = 'list all realms, including hidden')
    cmdgroup.add_argument('--hidden',
                          action = 'store_true', default = False,
                          help = 'list hidden realms only')
    command.set_defaults(func = _list)
    
    # Add
    
    command = subs.add_parser('add',
                              help = 'add new realm or change existing')
    command.add_argument('-f', '--force',
                         action = 'store_true', default = False,
                         help = 'force change existing realm, no prompt')
    command.add_argument('name',
                         help = 'name for new or existing realm to add or change.')
    command.add_argument('strings',
                         nargs = '*',
                         help = 'strings for realmlist.wtf file. '
                         'Asked from standard input if omit')
    command.set_defaults(func = _add)
    
    # Use
    
    command = subs.add_parser('use',
                              help = 'use realm by name')
    command.add_argument('name',
                         help = 'name of chosen realm. '
                         'Use "list" to choose')
    command.set_defaults(func = _use)
    
    # Show
    
    command = subs.add_parser('show',
                              help='show hidden realms')
    command.add_argument('names',
                         nargs='*',
                         help='name of hidden realm to show. '
                         'Use "list" to choose')
    command.set_defaults(func = _show)
    
    # Hide
    
    command = subs.add_parser('hide',
                              help = 'hide realms')
    command.add_argument('names',
                         nargs = '*',
                         help = 'name of realm to hide. '
                         'Use "list" to choose')
    command.set_defaults(func = _hide)
    
    # Remove
    
    command = subs.add_parser('remove',
                              help = 'remove realms')
    command.add_argument('-f', '--force',
                         action = 'store_true', default = False,
                         help = 'force deletion operation, no prompt')
    command.add_argument('names',
                         nargs = '*',
                         help = 'name of realm to permanently delete. '
                         'Use "list" to choose')
    command.set_defaults(func = _remove)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cli_args()
    #if __debug__: print(f'{vars(os.environ) = }')
    if __debug__: print(f'{vars(args) = }')
    result = args.func(args)
    if __debug__: print(f'{result = }')
    sys_exit(result)
