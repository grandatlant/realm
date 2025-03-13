#!/usr/bin/env -S python3
# -*- coding=utf-8 -*-
"""
Realm changing module for World of Warcraft
"""

from argparse import ArgumentParser
from os.path import abspath, exists as path_exists

from realmsettings import RealmSettings
from clitools import readlines

VERSION = '0.0.1'
DEF_SETTINGS_FILENAME = 'realm.json'
DEF_REALMLIST_FILENAME = '../Data/enUS/realmlist.wtf'

##  CLI stateless subroutines  ##
def _default(args):
    # no command specified. return soft error status
    return 1

def _list(args):
    if not path_exists(args.settings): return 1
    
    with RealmSettings(abspath(args.settings)) as sets:
        for name in sets.realms:
            # condition to pass current realm
            if sets.realm_hidden(name):
                if not (args.all or args.hidden): continue
            else:
                if args.hidden: continue
            hidden_indicator = ('(hidden)' if sets.realm_hidden(name) else '')
            name_to_print = f'{hidden_indicator}{name}'
            print(name_to_print)
            if args.long:
                predicate = (f'{name_to_print} -> ' if args.verbosity else '')
                for string in sets.realm_strings(name):
                    print(f'{predicate}{string}')
    return 0

def _add(args):
    #if not path_exists(args.settings): return 1
    with RealmSettings(abspath(args.settings)) as sets:
        name = args.name
        if sets.have_realm(name) and not args.force:
            ans = input(f'Realm {name} is already exists. Rewrite? (y/n) ')
            if not ans.upper() in 'YES':
                return 1
        
        strings = args.strings
        if not strings:
            if args.verbosity:
                print('Enter strings for realmlist.wtf. EOF (ctrl+d) to finish')
            strings = [got_string for got_string in readlines() if got_string]
        
        new_entry = sets.add(name, strings)
        if new_entry and args.verbosity:
            print(f'New entry for {name} done: {new_entry}')
    
    return 0

def _use(args):
    if not path_exists(args.settings): return 1
    with RealmSettings(abspath(args.settings)) as sets:
        name = args.name
        ## TODO: Implement it!
        raise NotImplementedError('Function _use is not implemented yet.')
    return 0

def _show(args):
    if not path_exists(args.settings): return 1
    with RealmSettings(abspath(args.settings)) as sets:
        for name in args.names:
            if sets.have_realm(name):
                show_success = sets.show(name)
                if show_success and args.verbosity:
                    print(f'Realm {name} marked as non-hidden')
            else:
                if args.verbosity > 1:
                    print(f'Realm {name} not found to show.')
    return 0

def _hide(args):
    if not path_exists(args.settings): return 1
    with RealmSettings(abspath(args.settings)) as sets:
        for name in args.names:
            if sets.have_realm(name):
                hide_success = sets.hide(name)
                if hide_success and args.verbosity:
                    print(f'Realm {name} marked as hidden')
            else:
                if args.verbosity > 1:
                    print(f'Realm {name} not found to hide.')
    return 0

def _remove(args):
    if not path_exists(args.settings): return 1
    with RealmSettings(abspath(args.settings)) as sets:
        for name in args.names:
            if sets.have_realm(name):
                confirmed = False
                if args.force:
                    confirmed = True
                else:
                    prompt = input(f'Confirm removing realm {name}? (y/n) ')
                    if prompt.upper() in 'YES':
                        confirmed = True
                if confirmed:
                    removed = sets.remove(name)
                    if removed and args.verbosity:
                        print(f'Realm {name} removed.')
            else:
                if args.verbosity > 1:
                    print(f'Realm {name} not found to remove.')
    return 0

def _parse_cli_args():
    parser = ArgumentParser(description = __doc__,
                            allow_abbrev = False,
                            epilog = 'Copyright (C) 2025 grandatlant')
    parser.set_defaults(func = _default)
    
    parser.add_argument('--version',
                        action = 'version',
                        version = f'%(prog)s {VERSION}')
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
                         #nargs = '?',
                         #default = '',
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
                         nargs = 1,
                         default = '',
                         help = 'name of chosen realm. '
                         'Use "list" to choose')
    command.set_defaults(func = _use)
    # Show
    command = subs.add_parser('show',
                              help='show hidden realms')
    command.add_argument('names',
                         nargs='+',
                         default='',
                         help='name of hidden realm to show. '
                         'Use "list" to choose')
    command.set_defaults(func = _show)
    # Hide
    command = subs.add_parser('hide',
                              help = 'hide realms')
    command.add_argument('names',
                         nargs = '+',
                         #default = '',
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
                         nargs = '+',
                         default = '',
                         help = 'name of realm to permanently delete. '
                         'Use "list" to choose')
    command.set_defaults(func = _remove)

    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_cli_args()
    
    if args.verbosity > 2:
        print(f'{vars(args) = }')

    result = args.func(args)
            
    if args.verbosity > 2:
        print(f'{result = }')
