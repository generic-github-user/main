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

def pickle(sess=None, compressed=False, level=6):
    if sess is not None:
        Session = sess
    save_data = bytes(dill.dumps(Session.library))
    data_string = base64.b64encode(save_data).decode('UTF-8')
    return data_string

def save(sess=None, path=None, **kwargs):
    if sess is not None:
        Session = sess
    if path is None:
        path = Session.filepath
    with open(path, 'w') as note_file:
        data_string = pickle(sess=sess, **kwargs)
        note_file.write(data_string)
    print(f'Saved database to {path}')
    return data_string
