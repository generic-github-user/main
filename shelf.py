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
import random

parser = argparse.ArgumentParser(description='Run a shelf command')
parser.add_argument('-i', '--interactive', action='store_true', help="Start shelf's interactive mode, which will use Python's input function to process command line inputs as direct inputs to the program (to eliminate the need to prefix each command with 'python shelf.py')")
parser.add_argument('-q', '--quit', action='store_true', help='Exit interactive mode')
parser.add_argument('-s', '--similarity', action='store_true', help='Find notes similar to this one (based on edit distance)')
parser.add_argument('-e', '--export', help='Export your notes library to another format (Markdown, JSON, etc.)')
parser.add_argument('-b', '--backup', action='store_true', help='Copy the entire library to another file')
parser.add_argument('-t', '--terms', action='store_true', help='Extract common terms from your notes')
parser.add_argument('-r', '--rank', help='Interactively rank notes')
parser.add_argument('-v', '--sort', help='Sort by an attribute of each note')
parser.add_argument('-n', '--number', help='Numerical parameter for another function (how many ratings to complete, how many results to display, etc.)', type=int)
parser.add_argument('-c', '--remove', help='Clear a field')
parser.add_argument('-u', '--recompute', help='Recalulate the specified field')

args = parser.parse_args()
print(args, parser.parse_args(['--interactive']))

class Session:
    directory = '/home/alex/Desktop/python_projects/shelf'
    filepath = '/home/alex/Desktop/python_projects/shelf/notesfile.txt'
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

def load(path=None):
    if path is None:
        path = Session.filepath
    try:
        with open(path, 'r') as note_file:
            Session.library = dill.loads(base64.b64decode(note_file.read()))
        print(f'Loaded library from {path}')
    except Exception as E:
        print(E)
        Session.library = Library()
        print(f'No library found at specified path ({path}); created new library')


def save(path=None):
    if path is None:
        path = Session.filepath
    with open(path, 'w') as note_file:
        note_file.write(base64.b64encode(bytes(dill.dumps(Session.library))).decode('UTF-8'))
    print(f'Saved database to {path}')

class Base:
    def __init__(self, log=False):
        self.uuid = uuid.uuid4().hex
        now = time.time()
        self.created = now
        self.timestamp = datetime.datetime.fromtimestamp(self.created).strftime('%b. %d, %Y')
        self.modified = time.time()
        self.accessed = time.time()
        if log:
            print(f'Created {type(self).__name__} instance at {now}')

    def upgrade(self, *args, **kwargs):
        template = type(self)(*args, **kwargs)
        for k, v in vars(template).items():
            if not hasattr(self, k):
                setattr(self, k, v)
        self.timestamp = datetime.datetime.fromtimestamp(self.created).strftime('%b. %d, %Y')
        return self

# class Settings(Base):

class Statistics(Base):
    def __init__(self):
        super().__init__()

def numeric(w):
    return all(wi in string.digits+'.' for wi in w)

class Library(Base):
    def __init__(self, notes=None, tags=None):
        super().__init__()

        if notes is None:
            notes = []
        self.notes = notes
        if tags is None:
            tags = []
        self.tags = tags
        self.terms = []
        self.comparisons = []

        self.statistics = Statistics()

    def upgrade(self):
        super().upgrade()
        for note in self.notes:
            note.upgrade()

    def recalculate(self, delta=10, criteria='importance'):
        for note in self.notes:
            note.ratings = Values()
        for notes, index in self.comparisons:
            for i in range(2):
                d = delta if (index == i) else -delta
                setattr(notes[i].ratings, criteria, getattr(notes[i].ratings, criteria) + d)

    def add(self, note):
        # Convert other data types to Note instances
        if not isinstance(note, Note):
            note = Note(note, container=self)
        # Add the note
        self.notes.append(note)
        print('Added note')
        similar = note.similar(min_=3, limit=5)
        print(f'Found {len(similar)} similar note{"s" if len(similar)!=1 else ""}:')
        for match, value in similar:
            print(f'> {match} ({value}%)')
            time.sleep(0.1)
        self.changed()
        return self

    def similar(self, note, threshold=90, min_=None, limit=None, sort_results=True):
        results = []
        # Loop through notes
        for note2 in self.notes:
            similarity = fuzz.token_sort_ratio(note.content, note2.content)
            if (note is not note2):
                if min_:
                    results.append([note2, similarity])
                # Compare similarity rating to threshold
                elif (similarity >= threshold):
                    results.append([note2, similarity])
        if sort_results:
            results.sort(key=lambda x: x[1], reverse=True)
        # Get the first n results
        if limit:
            results = results[:limit]
        return results

    def extract_terms(self, n=20, exclude_common=True, weighted=True, weighting='chars', size=(1, 4)):
        # A list of common words that should not be included in the results
        common = 'and of with the or if yet on in to a from as for another be by eg ie'.split()
        self.terms = set()
        frequencies = {}
        # Loop through all stored notes
        for note in self.notes:
            # Get note content (with punctuation removed)
            content = note.content.translate(str.maketrans('', '', string.punctuation))
            # Split into words
            words = content.split()
            # Generate n-grams of each specified length from words in note
            ngrams = []
            for length in range(*size):
                for i in range(0, len(words)-length):
                    span = words[i:i+length]
                    # Include this n-gram if at least one of its words is not in the common words list, or exclude_common is set to False
                    if (not exclude_common) or (not all((w.lower() in common or numeric(w)) for w in span)):
                        ngrams.append(' '.join(span))
            self.terms.update(ngrams)
            # Increment or create each n-gram's corresponding counter in the frequency list
            for term in ngrams:
                if term in frequencies:
                    frequencies[term] += 1
                else:
                    frequencies[term] = 1
        # self.terms = [Term(term) for term in self.terms]
        # Sort the terms by frequency (adjusted with the appropriate weighting), get the first n terms, and generate a list of Term instances
        self.terms = [Term(term, frequency=frequencies[term]) for term in sorted(frequencies.keys(), key=lambda k: frequencies[k] + 0.1*((len(k.split()) if weighting == 'tokens' else len(k)) if weighted else 1), reverse=True)[:n]]
        return self.terms

    def rank(self, criteria, delta=10):
        # Generate list of possible indices
        pool = np.arange(len(self.notes))
        # Select 2 indices without replacement
        indices = np.random.choice(pool, size=2, replace=False)
        # Get the corresponding note objects
        notes = [self.notes[i] for i in indices]
        print(f'Select one of the choices below based on {criteria} and enter the corresponding index (press enter to skip)')
        markers = 'ab'
        # Display list of notes to be compared
        for l, note in zip(markers, notes):
            print(f'> {l}) {note.content}')
        response = input()
        # If the input corresponds to a marker, store the index and adjust the notes' ratings
        if response in markers:
            index = markers.index(response)
            comparison = [notes, index]
            for i in range(2):
                d = delta if (index == i) else -delta
                setattr(notes[i].ratings, criteria, getattr(notes[i].ratings, criteria) + d)
            self.comparisons.append(comparison)
        else:
            pass


    def to_markdown(self, path=None):
        with open(Session.directory+'/md_template.md', 'r') as template_file:
            template = template_file.read()
        output = ''
        for note in self.notes:
            # output += note.content
            note_template = template
            for field in ['content', 'importance', 'timestamp']:
                note_template = note_template.replace(f'[{field}]', str(getattr(note, field)))
            output += note_template
            output += '\n'
        if path:
            with open(path, 'w') as export_file:
                export_file.write(output)
            print(f'Saved note library export to {path}')
        return output

    # def update_statistics(self):
    #     self.statistics.length_chars

    def changed(self):
        self.modified = time.time()
        save()

class Values:
    def __init__(self):
        self.importance = 100

class Note(Base):
    def __init__(self, content, container=None):
        super().__init__()
        self.content = content
        self.container = container
        self.hash = hash(self.content)
        self.ratings = Values()
        self.importance = self.ratings.importance

    def upgrade(self):
        super().upgrade(self.content)
        self.importance = self.ratings.importance
        return self

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

class Term(Base):
    def __init__(self, content, frequency=None):
        super().__init__()
        self.content = content
        self.frequency = frequency

    def __str__(self):
        return self.content

load()
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
    if args.export in ['md', 'markdown']:
        Session.library.to_markdown(Session.directory+'/notes_export.md')
if args.backup:
    timestamp = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    backup_path = f'{Session.directory}/shelf_backup_{timestamp}.txt'
    save(path=backup_path)
    print(f'Backed up library to {backup_path}')
if args.terms:
    terms = Session.library.extract_terms()
    for term in terms:
        print(f'> {term} [{term.frequency}]')
        time.sleep(0.1)
if args.sort:
    if args.sort == 'importance':
        results = sorted(Session.library.notes, key=lambda n: n.ratings.importance, reverse=True)
        # print(f'Found {len(similar)} similar note{"s" if len(similar)!=1 else ""}:')
        for note in results[:quantity or 20]:
            print(f'> {note.content} ({args.sort}: {note.ratings.importance})')
            time.sleep(0.05)
if args.remove:
    if args.remove == 'rankings':
        Session.library.comparisons = []
        Session.library.recalculate()
if args.recompute:
    if args.recompute == 'rankings':
        Session.library.recalculate()

save()
