#!/usr/bin/env -S python3 -OO
# -*- coding = utf-8 -*-
"""
Realm changing module for World of Warcraft,
using tkinter
"""
import sys
import tkinter as tk


def build_ui(parent):
    frame = tk.Frame(parent, relief='ridge', borderwidth=5)
    frame.pack(fill='both', expand=1)
    
    label = tk.Label(frame, text="--- Main frame for UI ---")
    label.pack(fill='x', expand=1)
    
    button = tk.Button(frame, text="Exit", command=parent.destroy)
    button.pack(side='bottom')

##  MAIN ENTRY POINT
def main(args=None):
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
