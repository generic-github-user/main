import base64
import dill

from library import Library

def load(path=None, store=True, sess=None):
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


def save(path=None, sess=None):
    if sess is not None:
        Session = sess
    if path is None:
        path = Session.filepath
    with open(path, 'w') as note_file:
        note_file.write(base64.b64encode(bytes(dill.dumps(Session.library))).decode('UTF-8'))
    print(f'Saved database to {path}')
