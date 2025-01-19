#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""
Realm changing module for World of Warcraft
"""

import sys

DEBUG = True

VERSION = '0.0.1'
DEF_SETS_FILENAME = 'realm.json'
DEF_REALMLIST_FILENAME = '../Data/enUS/realmlist.wtf'

def load_settings(filename):
    if DEBUG: print('load_settings('+filename+')')
    return filename

def parse_cli_args(args_list=None, ns=None):

    from argparse import ArgumentParser
    
    parser = ArgumentParser(description=__doc__,
                            allow_abbrev=False,
                            epilog='Copyright (C) 2025 grandatlant')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s '+VERSION)
    parser.add_argument('-v','--verbose',
                        action='count',
                        default=0,
                        help='increase verbosity level. Quiet by default')
    parser.add_argument('-s','--settings',
                        default='',
                        help='use settings from .json file. File "'
                        +DEF_SETS_FILENAME+'" is used as default')
    
    ## COMMANDS
    subs = parser.add_subparsers(title='Commands',
                                 description='main settings controlling interface')
    # List
    command = subs.add_parser('list',aliases=['ls'],
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
    command.set_defaults(command='list')
    # Add
    command = subs.add_parser('add',aliases=['new'],
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
    command.set_defaults(command='add')
    # Use
    command = subs.add_parser('use',aliases=['check'],
                              help='use realm by its name')
    command.add_argument('name',
                         nargs='?',
                         default='',
                         help='name of chosen realm. '
                         'Use "%(prog)s list" to choose')
    command.set_defaults(command='use')
    # Show
    command = subs.add_parser('show',aliases=['on'],
                              help='show hidden realm')
    command.add_argument('name',
                         nargs='?',
                         default='',
                         help='name of hidden realm to show. '
                         'Use "%(prog)s list -a|-h" to choose')
    command.set_defaults(command='show')
    # Hide
    command = subs.add_parser('hide',aliases=['off'],
                              help='hide realm from sight')
    command.add_argument('name',
                         nargs='?',
                         default='',
                         help='name of realm to hide. '
                         'Use "%(prog)s list" to choose')
    command.set_defaults(command='hide')
    # Remove
    command = subs.add_parser('remove',aliases=['rm'],
                              help='remove realm by its name')
    command.add_argument('name',
                         nargs='?',
                         default='',
                         help='name of realm to permanently delete.'
                         'Use "%(prog)s list [-a|-h]" to choose')
    command.set_defaults(command='remove')

    args = parser.parse_args(args_list, ns)
    if not hasattr(args, 'command'):
        parser.error('No command specified')
        
    return args

if __name__ == '__main__':

    args = parse_cli_args()
    if DEBUG: print('Parsed args:', args)

    if DEBUG or args.settings:
        settings = load_settings(args.settings)
        if args.verbose: print('Loaded settings:', settings)
