from token import Token
from node import Node


def range_filter(node):
    """This filter handles desugaring of the ".." syntax, which is modelled
    loosely after Rust's. The operator is transformed into a call to the
    `range` function, which returns a particular kind of iterator. If the
    traits system and/or iterator trait/type are not used in the compilation
    process, it can be further rewritten into a standalone loop.

    This filter is also used as an example of a generic filter in `README.md`,
    and is helpful for demonstrating the purpose of the compiler extension
    infrastructure project."""

    # if isinstance(node, Node):
    #     print(node.type, node.op == '..')
    if node.type == 'bin_op' and node.op == '..':
        # we could also use string interpolation in combination with a parser
        # call, but this way is conceptually cleaner
        return Node(type_='call', children=[
            Token(type_='IDENTIFIER', value='range'),
            Node(type_='tuple', depth=node.depth+1, children=[
                node.left, node.right], parent=node.parent)
        ], depth=node.depth, parent=node.parent)
    return node
