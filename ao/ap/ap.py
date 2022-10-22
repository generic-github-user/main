# OS/system utilities and file interaction
import os
import sys
import shutil
from pathlib import Path
import argparse

import graphviz

# Serialization and other miscellaneous tools
import pickle
import copy
import time
import itertools

import re
import string

# Logging
import warnings
import textwrap

# Monitoring
import psutil
import hashlib
from PIL import Image
from PIL import UnidentifiedImageError
import pytesseract

# Utilities and internal modules
from utils import getsize, hashfile
from files import filenode, snapshot, catalog

# Configuration data
from config import *

parser = argparse.ArgumentParser()
# parser.add_argument('subcommand', type=str)
subparsers = parser.add_subparsers()

imf_parser = subparsers.add_parser('imf')
imf_parser.add_argument('text', type=str)
imf_parser.set_defaults(func=lambda argvals: openfiles(
    list(filter(lambda x: hasattr(x, 'text')
                and argvals.text.lower() in x.text.lower(),
                data['files']))))

# try:
#     with open(dbpath, 'rb') as f:
#         data = pickle.load(f)
# except Exception as E:
#     print(E)
#     data = {
#         'snapshots': [],
#         'files': []
#     }

if len(sys.argv) > 1 and sys.argv[1] == 'CLEAR':
    data = {
        'snapshots': [],
        'files': []
    }


# Store the current database at `path` (serialized using pickle; not very
# efficient, but extremely expressive)
def save(path=dbpath):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


# Logging helper function; displays the string `content`, indented and
# line-wrapped
def log(content, level=0):
    n = 60
    lines = [content[i:i+n] for i in range(0, len(content), n)]
    #print('  '*level+content)
    #print(lines[0])
    #print('\n~ '.join(lines))

    p = '  ' * level  # prefix
    print(p + f'\n{p}~ '.join(textwrap.wrap(content, n)))


# Helper class to make my life easier;
# - supports arbitrary keyword arguments (which are stored as attributes)
# - tracks access and modification
# - enables method chaining for common iterable operations
class node:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        created = time.time()


# Generates a folder containing symlinks to each of the given files and opens
# it using the associated program
def openfiles(files):
    dirname = f'/home/alex/Desktop/ap-temp-{time.time()}'
    # be careful
    fcopy = copy.deepcopy(files)
    # If two or more files have the same name, rename (copies of) them with a
    # numeric suffix
    for f in fcopy:
        if sum(f.name == g.name for g in fcopy) > 1:
            # we're operating over references so we can modify the cloned nodes
            # directly
            for i, h in enumerate(list(filter(
                    lambda x: f.name == x.name, fcopy))):
                suffix = f'-{i+1}'
                # a, b = 
                h.name = str(Path(h.name).stem+suffix+h.ext)
                # h.path += suffix

    Path(dirname).mkdir()
    # Generate the symlinks and open the folder
    for f in fcopy:
        Path(os.path.join(dirname, f.name)).symlink_to(f.path)
    os.system(f'xdg-open {dirname}')


# Add `tag` to `fnode` if its extension matches any of the types in `types`
def tagfile(fnode, types, tag):
    if (hasattr(fnode, 'ext') and
        fnode.ext.lower()[1:] in types.split() and
            'image' not in fnode.tags):  # TODO
        fnode.tags.append('image')


# Apply some simple tagging rules to file nodes
def tagfiles(n=0):
    log('Tagging files')
    for anode in itertools.islice(data['files'], n):
        anode.validate()
        # Rules (i.e., types -> tag)
        tagfile(anode, 'gif png jpg jpeg tiff webm', 'image')
        tagfile(anode, 'txt js py sh java css html todo', 'textlike')

        # temporary-ish code to upgrade old file node instances
        if not hasattr(anode, 'tags'): setattr(anode, 'tags', [])
        anode.print()
    save()


def mayhave(obj, attr):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    else:
        return None


# Apply OCR to (up to `n`) files tagged with "image" and store the resulting
# text in the filenode
def extracttext(n=0):
    log('Running OCR (Tesseract)')
    for anode in itertools.islice(filter(
            lambda x: (hasattr(x, 'tags') and
                       'image' in x.tags and
                       not mayhave(x, 'processed')),
            data['files']), n):
        # anode.print()
        try:
            log('', 1)
            log(anode.path, 1)
            imgcontent = pytesseract.image_to_string(Image.open(anode.path))
            setattr(anode, 'text', imgcontent)

            # Display a slightly more readable version of the extracted content
            text = imgcontent.replace('\n', '')
            text = re.sub('[\n ]+', ' ', text, re.M)
            log(f"Result (condensed): {text}", 1)
        # Catch occasional invalid images
        except UnidentifiedImageError as exception:
            print(exception)
        anode.processed = True
    # Update database file
    save()


with open(dbpath, 'rb') as f:
    data = pickle.load(f)

args = parser.parse_args()
# match args.subcommand:
#     'imf'

if hasattr(args, 'func'):
    args.func(args)
