import warnings

from utils import hashfile

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
