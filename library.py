import time
import numpy as np
import string

import fuzzywuzzy
from fuzzywuzzy import fuzz

from session import Session
from base import Base
from note import Note
from term import Term
# from utils import load, save

def numeric(w):
    return all(wi in string.digits+'.' for wi in w)

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
        super().changed()
        self.modified = time.time()
        # save()
