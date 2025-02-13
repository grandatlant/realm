#!/usr/bin/env -S python3
# -*- coding=utf-8 -*-
"""
Realm changing module for World of Warcraft
"""

VERSION = '0.0.1'
DEF_SETTINGS_FILENAME = './realm.json'
DEF_REALMLIST_FILENAME = '../Data/enUS/realmlist.wtf'

import sys
from argparse import ArgumentParser, Namespace
from clitools import readlines

# Realm control classes
from classes import *

##  CLI stateless subroutines  ##
def _list(args):
    pass

def _add(args):
    pass

def _use(args):
    pass

def _show(args):
    pass

def _hide(args):
    pass

def _remove(args):
    pass

def _parse_cli_args(args: list = None, namespace = None) -> Namespace:
    
    parser = ArgumentParser(description=__doc__,
                            allow_abbrev=False,
                            epilog='Copyright (C) 2025 grandatlant')
    # default debug/verbose action - function 'print()'
    parser.set_defaults(func=print)
    
    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {VERSION}')
    parser.add_argument('-v','--verbose',
                        dest='verbosity',
                        action='count',
                        default=0,
                        help='increase verbosity level. Quiet by default.')
    parser.add_argument('-s','--settings',
                        default='',
                        help='use settings from .json file. '
                        f'File "{DEF_SETTINGS_FILENAME}" is used as default')
    ## COMMANDS
    subs = parser.add_subparsers(title='Commands',
                                 dest='command',
                                 description='main settings interface')
    # List
    command = subs.add_parser('list',
                              help='list all realms')
    command.add_argument('-l','--long',
                         action='store_true', default=False,
                         help='list full information, not only names')
    cmdgroup = command.add_mutually_exclusive_group()
    cmdgroup.add_argument('--all',
                          action='store_true', default=False,
                          help='list all realms, including hidden')
    cmdgroup.add_argument('--hidden',
                          action='store_true', default=False,
                          help='list hidden realms')
    command.set_defaults(func=_list)
    # Add
    command = subs.add_parser('add',
                              help='add new realm')
    command.add_argument('-n','--name',
                         #nargs='?',
                         default='',
                         help='name for new or existing realm to add or change. '
                         'Asked from standard input if omit')
    command.add_argument('strings',
                         nargs='*',
                         help='strings for realmlist.wtf file. '
                         'Asked from standard input if omit')
    command.set_defaults(func=_add)
    # Use
    command = subs.add_parser('use',
                              help='use realm by its name')
    command.add_argument('name',
                         nargs=1,
                         default='',
                         help='name of chosen realm. '
                         'Use "list" to choose')
    command.set_defaults(func=_use)
    # Show
    command = subs.add_parser('show',
                              help='show hidden realm')
    command.add_argument('names',
                         nargs='+',
                         default='',
                         help='name of hidden realm to show. '
                         'Use "list" to choose')
    command.set_defaults(func=_show)
    # Hide
    command = subs.add_parser('hide',
                              help='hide realm from sight')
    command.add_argument('names',
                         nargs='+',
                         default='',
                         help='name of realm to hide. '
                         'Use "list" to choose')
    command.set_defaults(func=_hide)
    # Remove
    command = subs.add_parser('remove',
                              help='remove realm by its name')
    command.add_argument('-f', '--force',
                         action='store_true', default=False,
                         help='force deletion operation, never prompt')
    command.add_argument('names',
                         nargs='+',
                         default='',
                         help='name of realm to permanently delete. '
                         'Use "list" to choose')
    command.set_defaults(func=_remove)

    return parser.parse_args(args=args, namespace=namespace)


##    MAIN    ##
def _main() -> int:

    args = _parse_cli_args()
    
    if args.verbosity > 2:
        print(f'sys.argv = {sys.argv}')
        print('Parsed args:', vars(args))
    
    result = 0
    if args.command or args.verbosity > 1:
        try:
            result = args.func(args)
        except AttributeError:
            # assume func is absent for command
            result = 1
    return result if result is not None else 0

if __name__ == '__main__':
    print(_main())
