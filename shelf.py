import dill
import uuid
import argparse
import zlib
import base64
import time
import datetime
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import fuzz
import string

parser = argparse.ArgumentParser(description='Run a shelf command')
parser.add_argument('-i', '--interactive', action='store_true', help="Start shelf's interactive mode, which will use Python's input function to process command line inputs as direct inputs to the program (to eliminate the need to prefix each command with 'python shelf.py')")
parser.add_argument('-q', '--quit', action='store_true', help='Exit interactive mode')
parser.add_argument('-s', '--similarity', action='store_true', help='Find notes similar to this one (based on edit distance)')
parser.add_argument('-b', '--backup', action='store_true', help='Copy the entire library to another file')

args = parser.parse_args()
print(args, parser.parse_args(['--interactive']))
class Session:
    library = None

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
        else:
            # If no command flags are provided, assume the input is to be added as a note
            Session.library.add(text)

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
        # Convert other data types to Note instances
        if not isinstance(note, Note):
            note = Note(note, container=self)
        # Add the note
        self.notes.append(note)
        print('Added note')
        similar = note.similar(limit=5)
        print(f'Found {len(similar)} similar note{"s" if len(similar)!=1 else ""}:')
        for match, value in similar:
            print(f'{match} ({value}%)')
        self.changed()
        return self

    def similar(self, note, threshold=90, limit=None):
        results = []
        # Loop through notes
        for note2 in self.notes:
            similarity = fuzz.token_sort_ratio(note.content, note2.content)
            if (note is not note2) and (similarity >= threshold):
                results.append([note2, similarity])
        # Get the first n results
        if limit:
            results = results[:limit]
        return results

class Note(Base):
    def __init__(self, content, container=None):
        super().__init__()
        self.content = content
        self.container = container
        self.hash = hash(self.content)

    def similar(self, **kwargs):
        return self.container.similar(self, **kwargs)

    def __str__(self):
        return self.content

class Tag(Base):
    def __init__(self, name, container=None):
        super().__init__()
        self.name = name
        self.container = container
        self.hash = hash(self.name)

load()
if args.backup:
    timestamp = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    save(path=f'./shelf_backup_{timestamp}.txt')

save()
