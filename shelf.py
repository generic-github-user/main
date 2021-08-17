import dill
import uuid
import argparse
import zlib
import base64
import time
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import fuzz

parser = argparse.ArgumentParser(description='Run a shelf command')
parser.add_argument('-i', '--interactive', action='store_true', help="Start shelf's interactive mode, which will use Python's input function to process command line inputs as direct inputs to the program (to eliminate the need to prefix each command with 'python shelf.py')")
parser.add_argument('-q', '--quit', action='store_true', help='Exit interactive mode')
parser.add_argument('-s', '--similarity', action='store_true', help='Find notes similar to this one (based on edit distance)')

args = parser.parse_args()
print(args, parser.parse_args(['--interactive']))
class Session:
    library = None
def load(path='./notesfile.txt'):
    try:
        with open(path, 'r') as note_file:
            Session.library = dill.loads(base64.b64decode(note_file.read()))
        print(f'Loaded library from {path}')
    except Exception as E:
        print(E)
        Session.library = Library()
        print(f'No library found at specified path ({path}); created new library')


def save(path='./notesfile.txt'):
    with open(path, 'w') as note_file:
        note_file.write(base64.b64encode(bytes(dill.dumps(Session.library))).decode('UTF-8'))
    print(f'Saved database to {path}')

class Base:
    def __init__(self):
        self.uuid = uuid.uuid4().hex
        now = time.time()
        self.created = now
        self.modified = time.time()
        self.accessed = time.time()
        print(f'Created {type(self).__name__} instance at {now}')

# class Settings(Base):

class Statistics(Base):
    def __init__(self):
        super().__init__()

class Library(Base):
    def __init__(self, notes=None, tags=None):
        super().__init__()

        if notes is None:
            notes = []
        self.notes = notes
        if tags is None:
            tags = []
        self.tags = tags

        self.statistics = Statistics()

    def add(self, note):
        if not isinstance(note, Note):
            note = Note(note, container=self)
        self.notes.append(note)
        print('Added note')
        similar = note.similar(limit=5)
        print(f'Found {len(similar)} similar note{"s" if len(similar)!=1 else ""}:')
        for match, value in similar:
            print(f'{match} ({value}%)')
        self.changed()
        return self
