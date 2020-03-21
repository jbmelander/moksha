import argparse
import os
import yaml
import pathlib
import curses
from ui import Session
from core import Tree
from utils import Config

def main(stdscr):
    PATHDEF = Config().PathDef
    default_filepath = os.path.join(PATHDEF.SaveDirectory,PATHDEF.DefaultFile)

    if not os.path.isdir(PATHDEF.SaveDirectory):
        os.mkdir(PATHDEF.SaveDirectory)

    tree =  Tree() 

    if os.path.exists(default_filepath):
        tree.load(default_filepath)
    else:
        tree.save_as(default_filepath)
    # Gui Session
    Session(stdscr,tree)
    

if __name__ == '__main__':
    curses.wrapper(main)
    

