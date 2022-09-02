import sys
import os, os.path
from io import open
import glob, time
import pathlib

from lark import Lark
from lark.indenter import PythonIndenter


kwargs = dict(postlex=PythonIndenter(), start='file_input')

# python_parser3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser='lalr', **kwargs)
grammar = pathlib.Path('python.lark').read_text()
parser = Lark(grammar, parser='lalr', lexer='contextual', **kwargs)
# parser = Lark(grammar, parser='earley', lexer='dynamic', **kwargs)

def _read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()

def _get_lib_path():
    if os.name == 'nt':
        if 'PyPy' in sys.version:
            return os.path.join(sys.base_prefix, 'lib-python', sys.winver)
        else:
            return os.path.join(sys.base_prefix, 'Lib')
    else:
        return [x for x in sys.path if x.endswith('%s.%s' % sys.version_info[:2])][0]

def test_python_lib():
    path = _get_lib_path()

    start = time.time()
    files = glob.glob(path+'/*.py')
    total_kb = 0
    for f in files:
        r = _read(os.path.join(path, f))
        kb = len(r) / 1024
        print( '%s -\t%.1f kb' % (f, kb))
        parser.parse(r + '\n')
        total_kb += kb

    end = time.time()
    print( "test_python_lib (%d files, %.1f kb), time: %.2f secs"%(len(files), total_kb, end-start) )


tree = parser.parse(_read('sample-2.np') + '\n')
print(tree.pretty())
