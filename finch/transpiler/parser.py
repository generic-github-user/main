import lark
from lark import Lark
from lark.indenter import Indenter

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2

with open('grammar.lark', 'r') as grammar:
    parser = Lark(grammar.read(), parser='lalr', lexer='contextual', postlex=TreeIndenter(), debug=True)

class Token:
    def __init__(self, source, parent=None):
        self.parent = parent
        self.source = source
        for attr in 'type value line column'.split():
            setattr(self, attr, getattr(self.source, attr))
            self.length = len(self.source)

    def text(self): return self.value

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'

    def rustify(self):
        pass

    def pythonize(self, type_annotations=False) -> str:
        #match self.type:
        #    case 'binary_operator':
        match self.value:
            case "+" | "-" | "*" | "/" | "**" | "." | ".." | "#"\
            | "==" | "!=" | "~" | "!~" | ">" | ">=" | "<" | "<="\
            | "^" | "<<" | ">>" | "%" : return self.value
            case '&': return 'and'
            case '|': return 'or'
            case '@': return '@'
            #case '->':
            #case '+-': return f'set({
        match self.type:
            case 'NUMBER' | 'IDENTIFIER' | 'STRING': return self.value
            case 'COMMENT': return '#'+self.value[2:]
            case _: raise NotImplementedError(self.type, self.value)




class Node:
    def __init__(self, source, parent=None, depth=0, root=None):
        self.parent = parent
        self.root = root if root else self
        self.children = []
        self.source = source

        self.meta = self.source.meta
        self.type = self.source.data
        self.depth = depth
        for c in self.source.children:
            #print(c)
            if isinstance(c, lark.Tree): self.children.append(
                    Node(c, self, self.depth+1, root=self.root if self.root else self))
            elif c is None: self.children.append(c)
            else:
                assert isinstance(c, lark.Token), c
                self.children.append(Token(c))

    def text(self):
        return ''.join(c.text() for c in self.children)

    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' + '\n' + '\n'.join('  '*self.depth + str(n) for n in self.children)

    def pythonize(self, type_annotations=False, priority='perf', dependencies=None) -> str:
        result = None
with open('example.fn', 'r') as f:
    parsed = parser.parse(f.read())
print(parsed.pretty()[:2000])
#print(parsed)
ast = Node(parsed)
print(ast)

tr_python = ast.pythonize()
print(tr_python)
exec(tr_python)

def parse():

    result = ''
    #for tree in parsed.iter_subtrees():
        #print(tree.pretty()[:100])
    #breakpoint()
    print(result)

parse()

#TODO: internally convert parts of AST to lists (repeated operations, method chaining, etc.)
#TODO: ML-based AST optimization
