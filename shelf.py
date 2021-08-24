import dill
import glob
import uuid
import argparse
import zlib
import base64
import time
import datetime
import numpy as np

import fuzzywuzzy
from fuzzywuzzy import fuzz
import re

import string
import random
from colorama import Fore, Back, Style

from session import Session
from base import Base
from library import Library, Statistics
from note import Note
from term import Term
from stringb import String
from utils import load, save

parser = argparse.ArgumentParser(description='Run a shelf command')
parser.add_argument('-i', '--interactive', action='store_true', help="Start shelf's interactive mode, which will use Python's input function to process command line inputs as direct inputs to the program (to eliminate the need to prefix each command with 'python shelf.py')")
parser.add_argument('-q', '--quit', action='store_true', help='Exit interactive mode')
parser.add_argument('-s', '--similarity', action='store_true', help='Find notes similar to this one (based on edit distance)')
parser.add_argument('-e', '--export', help='Export your notes library to another format (Markdown, JSON, etc.)')
parser.add_argument('-b', '--backup', action='store_true', help='Copy the entire library to another file')
parser.add_argument('-t', '--terms', action='store_true', help='Extract common terms from your notes')
parser.add_argument('-w', '--stats', action='store_true', help='Show general statistics about a note library')
parser.add_argument('-r', '--rank', help='Interactively rank notes')
parser.add_argument('-v', '--sort', help='Sort by an attribute of each note')
parser.add_argument('-n', '--number', help='Numerical parameter for another function (how many ratings to complete, how many results to display, etc.)', type=int)
parser.add_argument('-c', '--remove', help='Clear a field')
parser.add_argument('-u', '--recompute', help='Recalulate the specified field')
parser.add_argument('-z', '--undo', help='Undo the last action')
parser.add_argument('-a', '--again', help='Repeat the last action')
parser.add_argument('-y', '--explore', help='Explore backup files', type=int)
parser.add_argument('-f', '--find', help='Search for a note using a regular expression', type=str)
parser.add_argument('-d', '--dry', help='Execute a simulated run of the specified command without actually modifying any data')

args = parser.parse_args()
print(args, parser.parse_args(['--interactive']))

# TODO: include number of different notes term appears in

def interactive():
    while True:
        # Get input from user
        text = input()
        if text[0] == '-':
            interactive_args = parser.parse_args(text.split())
            # Exit loop (quit flag)
            if interactive_args.quit:
                print('Exiting...')
                break
        # else:
        # If no command flags are provided, assume the input is to be added as a note
        Session.library.add(text)
        save(sess=Session)


# class Settings(Base):




class Tag(Base):
    def __init__(self, name, container=None):
        super().__init__()
        self.name = name
        self.container = container
        self.hash = hash(self.name)

load(sess=Session)
Session.library.upgrade()

if args.number:
    quantity = args.number
else:
    quantity = None

if args.rank:
    if args.rank == 'importance':
        for i in range(quantity or 5):
            Session.library.rank(args.rank)
if args.interactive:
    interactive()
if args.export:
    timestamp = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    if args.export in ['md', 'markdown']:
        Session.library.to_markdown(f'{Session.directory}/notes_export_{timestamp}.md')
if args.backup:
    timestamp = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    backup_path = f'{Session.directory}/shelf_backup_{timestamp}.txt'
    save(path=backup_path, sess=Session)
    print(f'Backed up library to {backup_path}')
if args.terms:
    terms = Session.library.extract_terms()
    for term in terms:
        print(f'> {term} [{term.frequency}]')
        time.sleep(0.1)
if args.sort:
    if args.sort in ['importance', 'length', 'words']:
        results = sorted(Session.library.notes, key=lambda note: getattr(note, args.sort), reverse=True)
        # print(f'Found {len(similar)} similar note{"s" if len(similar)!=1 else ""}:')
        for note in results[:quantity or 20]:
            print(f'> {note} ({args.sort}: {getattr(note, args.sort)})')
            time.sleep(0.05)
    else:
        raise ValueError
if args.remove:
    if args.remove == 'rankings':
        Session.library.comparisons = []
        Session.library.recalculate()
if args.recompute:
    if args.recompute == 'rankings':
        Session.library.recalculate()
if args.explore is not None:
    assert isinstance(args.explore, int)
    assert args.explore >= 0
    backups = glob.glob('./shelf_backup_*')
    backup_file = backups[args.explore]
    print(f'Loading library from {backup_file}')
    temp_library = load(backup_file, store=False)
    temp_library.upgrade()
    for note in temp_library.notes:
        print(note)
if args.find:
    assert isinstance(args.find, str)
    results = []
    for note in Session.library.notes:
        if re.match(args.find, note.content.text):
            results.append(note)
    for note in results:
        print(f'> {note}')
if args.stats:
    colors = 'red yellow green blue cyan magenta'.split()
    for i, attribute in enumerate(['length', 'words']):
        print(f'total {attribute}: {String(sum(getattr(note, attribute) for note in Session.library.notes)).color(colors[i])}')
    print(f'total notes: {String(len(Session.library.notes)).color(colors[2])}')

save(sess=Session)
