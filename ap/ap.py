import os
import sys
import shutil
from pathlib import Path
import argparse

import graphviz

import pickle
import copy
import time
import itertools

import re
import string

import warnings
import textwrap

import psutil
import hashlib
from PIL import Image
from PIL import UnidentifiedImageError
import pytesseract

dbpath = '/home/alex/Desktop/ap.pickle'
timelimit = 20

loglevel = 0
parser = argparse.ArgumentParser()
#parser.add_argument('subcommand', type=str)
subparsers = parser.add_subparsers()

imf_parser = subparsers.add_parser('imf')
imf_parser.add_argument('text', type=str)
imf_parser.set_defaults(func=lambda argvals: openfiles(list(filter(lambda x: hasattr(x, 'text') and argvals.text.lower() in x.text.lower(), data['files']))))

from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

# Estimate the "true" size of an object, which may be nested and/or contain
# references to other objects (from https://stackoverflow.com/a/30316760)
def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size

# Hash a file given a path and return hex digests for the md5 and sha1 hashes
# of the file's content (based on https://stackoverflow.com/a/44873382)
def hashfile(path):
    # 256kb
    BUF_SIZE = 2 ** 18

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data: break
            md5.update(data)
            sha1.update(data)
    return (md5.hexdigest(), sha1.hexdigest())

#try:
#    with open(dbpath, 'rb') as f:
#        data = pickle.load(f)
#except Exception as E:
#    print(E)
#    data = {
#        'snapshots': [],
#        'files': []
#    }

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
    n=60
    lines = [content[i:i+n] for i in range(0, len(content), n)]
    #print('  '*level+content)
    #print(lines[0])
    #print('\n~ '.join(lines))

    p='  ' * level # prefix
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

# Very minimalist class for representing a file; aggregated from file
# snapshots, which represent a (possibly nonexistent) file at a particular
# point in time
class filenode:

    attrs = {'id': int, # Numeric ID 
             'path': str, # Filepath
             'name': str, # File name
             'tags': list, # Internal file tags (different than those assigned to metadata by a file manager)
             'size': int, # File size in bytes
             'snapshots': list, # A chronologically ordered (?) list of file snapshots
             'ext': str # File extension
             }
    def __init__(self, **kwargs):
        self.id = 0
        self.path = ''
        self.ext = ''
        self.size = 0
        self.tags = []
        self.snapshots = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Check that the expected attributes are present within this filenode and
    # have the correct types (this is Python, so we only emit a warning if
    # something is askew)
    def validate(self):
        for k, v in filenode.attrs.items():
            if hasattr(self, k):
                if not isinstance(getattr(self, k), v):
                    warnings.warn(f'Attribute `{k}` should have type {v}')
            else:
                warnings.warn(f'filenode missing expected attribute: `{k}`')

    # Generate a string representing this filenode
    def __str__(self):
        return 'filenode { '+'\n'.join(f'{a}: {getattr(self, a) if hasattr(self, a) else None}' for a in 'name path ext tags snapshots'.split())+' }'

    def print(self):
        print(self)

# Information about a file at a specific point in time (see above), similar to
# those used by Git; this approach enables highly accurate monitoring and
# versioning without having to continuously listen for file system events
class snapshot:
    # Initialize a new file snapshot
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Integrate a file snapshot into The File Database
    def process(self):
        log('')
        print(f'Integrating snapshot: {self}')
        #print(len(data['files']))
        current = list(filter(lambda x: x.path == self.path, data['files']))
        if len(current) > 1:
            #raise BaseException('')
            warnings.warn('File database has more than one live file with the\
                          same path; this should not happen')
        #node = current.next()

        # "temporary" - generate ext if not present
        #hasn'tattr
        if not hasattr(self, 'ext'):
            _, self.ext = os.path.splitext(self.path)

        # If a matching filenode is found, integrate this snapshot into it
        if current:
            log(f'Found corresponding node ({self.path})', 1)
            current[0].snapshots.append(self)
            #current[0].ext = self.ext
            current[0].ext = self.ext
            #current[0].print()
        # Otherwise, add a new node with a reference to this snapshot
        else:
            log(f'Adding file node for {self.path} ({len(data["files"])} total)', 1)
            newnode = filenode(
                id=len(data['files']),
                name=self.name, path=self.path, ext=self.ext,
                size=self.data.st_size,
                snapshots=[self],
                tags=[],
                processed=False,
                textproc=False
            )
            data['files'].append(newnode)
            #newnode.print()
        # Mark the snapshot as having been incorporated into the main database
        self.processed=True

# TODO: refactor using https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir

# Collect information about every file and subdirectory in `path` (optionally
# recursive); these are referred to as file "snapshots" that can be processed
# into internal representations of actual files ("nodes"). These snapshots are
# considered to be immutable (excepting boolean flags) and are stored
# persistently to regenerate file nodes if/when necessary.
def catalog(path='.', limit=1000, i=0, recursive=True, level=0, delay=0.01) -> int:
    for subpath in os.listdir(path):
        log(f'Getting stats for {subpath} ({i}/?)', level)
        fullpath = os.path.join(path, subpath)
        #S = snapshot()
        #S.data = os.stat(fullpath)
        # Why don't old nodes (without name/path) cause issues?
        log(f'Adding snapshot; {len(data["snapshots"])} total', level+1)
        fname, ext = os.path.splitext(fullpath)
        # Get information about a file or directory
        stats = os.stat(fullpath)
        # should we move the hashing elsewhere?
        # TODO: store references to files contained in directory (and possibly the inverse)
        snapshot_info = dict(
            id=len(data['files']),
            name=subpath,
            path=fullpath,
            ext=ext,
            data=stats,
            time=time.time(),
            isdir=os.path.isdir(fullpath),
            processed=False,
            #md5=md5,
            #sha1=sha1
        )
        # Only hash small files (exclude dirs)
        if os.path.isdir(fullpath) or stats.st_size > 10e7:
            snapshot_info |= dict(md5=None, sha1=None, hashed=False)
        else:
            md5, sha1 = hashfile(fullpath)
            snapshot_info |= dict(md5=md5, sha1=sha1, hashed=True)
        # Store snapshot in main database
        newsnapshot = snapshot(**snapshot_info)
        data['snapshots'].append(newsnapshot)
        # Integrate the snapshot into the file database
        newsnapshot.process()
        i += 1

        # Recurse into subdirectories (if enabled)
        #if os.path.isdir(subpath) and recursive:
        if os.path.isdir(fullpath) and recursive:
            i = catalog(fullpath, limit, i, True, level=level+1)
        # Limit total number of files visited
        if i >= limit:
            print(f'Reached limit: {limit}')
            break
        time.sleep(delay)
    return i

# Generates a folder containing symlinks to each of the given files and opens
# it using the associated program
def openfiles(files):
    dirname = f'/home/alex/Desktop/ap-temp-{time.time()}'
    # be careful
    fcopy = copy.deepcopy(files)
    for f in fcopy:
        if sum(f.name == g.name for g in fcopy) > 1:
            for i, h in enumerate(list(filter(lambda x: f.name == x.name, fcopy))):
                suffix = f'-{i+1}'
                #a, b = 
                h.name = str(Path(h.name).stem+suffix+h.ext)
                # h.path += suffix

    Path(dirname).mkdir()
    for f in fcopy:
        Path(os.path.join(dirname, f.name)).symlink_to(f.path)
    os.system(f'xdg-open {dirname}')

def tagfile(fnode, types, tag):
    if (hasattr(fnode, 'ext') and
        fnode.ext.lower()[1:] in types.split() and
        'image' not in fnode.tags):
        fnode.tags.append('image')

def tagfiles(n=0):
    log('Tagging files')
    for anode in itertools.islice(data['files'], n):
        anode.validate()
        tagfile(anode, 'gif png jpg jpeg tiff webm', 'image')
        tagfile(anode, 'txt js py sh java css html todo', 'textlike')

        if not hasattr(anode, 'tags'): setattr(anode, 'tags', [])
        anode.print()
    save()

def mayhave(obj, attr):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    else:
        return None

def extracttext(n=0):
    log('Running OCR (Tesseract)')
    for anode in itertools.islice(filter(
            lambda x:
                (hasattr(x, 'tags') and
                'image' in x.tags and
                not mayhave(x, 'processed')),
            data['files']), n):
        #anode.print()
        try:
            log('', 1)
            log(anode.path, 1)
            imgcontent = pytesseract.image_to_string(Image.open(anode.path))
            setattr(anode, 'text', imgcontent)

            text = imgcontent.replace('\n', '')
            text = re.sub('[\n ]+', ' ', text, re.M)
            log(f"Result (condensed): {text}", 1)
        except UnidentifiedImageError as exception:
            print(exception)
        anode.processed = True
    save()

with open(dbpath, 'rb') as f:
    data = pickle.load(f)

args = parser.parse_args()
#match args.subcommand:
#    'imf'

if hasattr(args, 'func'):
    args.func(args)

# TODO: generate folder from tags/types
# TODO: generate human-readable file manifest
# TODO: add command/function for general searches
# TODO: fuzzy string matching
# TODO: auto-generate appropriate file names ?
# TODO: store file relations in snapshots/nodes
