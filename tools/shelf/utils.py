import base64
import dill
import zlib

from library import Library

def load(path=None, store=True, sess=None):
    """
    Load (unpickle) a library instance from its string representation
    """

    if sess is not None:
        Session = sess
    if path is None:
        path = Session.filepath
    try:
        with open(path, 'r') as note_file:
            loaded = dill.loads(base64.b64decode(note_file.read()))
            if store:
                Session.library = loaded
            else:
                return loaded
        print(f'Loaded library from {path}')
    except Exception as E:
        print(E)
        if store:
            Session.library = Library()
            print(f'No library found at specified path ({path}); created new library')

def pickle(sess=None, compressed=False, level=6):
    """
    Convert a library object (class instance) to a string representation (usually for saving to a local file)
    """

    if sess is not None:
        Session = sess
    save_data = bytes(dill.dumps(Session.library))
    if compressed:
        save_data = zlib.compress(save_data, level=level)
    data_string = base64.b64encode(save_data).decode('UTF-8')
    return data_string

def save(sess=None, path=None, **kwargs):
    """
    Encode the current library as a string and save it to the local file specified by `path` (if not provided, the path stored in the Session object will be used).

    The usual process is `pickle to string` -> `convert to bytes` -> `compress (optional)` -> `encode in base 64` -> `write to file`
    """

    if sess is not None:
        Session = sess
    if path is None:
        path = Session.filepath
    with open(path, 'w') as note_file:
        data_string = pickle(sess=sess, **kwargs)
        note_file.write(data_string)
    print(f'Saved database to {path}')
    return data_string
