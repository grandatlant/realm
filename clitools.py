#!/usr/bin/env -S python3
# -*- coding=utf-8 -*-
r"""
Some useful functions to work with cli
"""

def readlines(*preprint, prompt = None, lines = None, end = None):
    r"""
    Generator for input() until EOFError throwed
    """
    prompt_input = str(prompt) if prompt else ''
    append_lines = isinstance(lines, list)
    
    if preprint:
        print(*preprint)
        
    try:
        while True:
            line = input(prompt_input)
            if append_lines: lines.append(line)
            yield line
    except EOFError:
        pass

    if end is not None:
        if append_lines: lines.append(end)
        yield end

##  MAIN
def main():
    return None

if __name__ == '__main__':
    main()
