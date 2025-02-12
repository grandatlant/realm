#!/usr/bin/env -S python3
# -*- coding=utf-8 -*-
"""
Reads lines from stdin until EOF (Ctrl+D) and prints them after
"""

#import readline

def readlines(prompt = None) -> list:
    res = list()
    try:
        while True:
            res.append(input(prompt if prompt else ''))
    except EOFError:
        pass
    return res

##    MAIN    ##
def main(argv: list = None) -> int:
    lines = readlines(argv[1] if argv and len(argv) > 1 else None)
    #print(lines)
    for line in lines:
        print(line)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
