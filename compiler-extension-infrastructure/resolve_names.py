# from .token import Token
# from .node import Node
# import .node as cnode
from . import node as cnode

# from raise_error import raise_error
from . import raise_error


def resolve_names(node, namespace):
    """Replaces identifiers in particular kinds of locations ("evaluation
    contexts") with references to their values. This should generally happen
    before type inference is attempted."""

    if node.type == 'function_declaration':
        assert hasattr(node, 'signature') and node.signature is not None
        assert hasattr(node.signature, 'arguments') and\
            node.signature.arguments is not None
        fnode = cnode.Node(type_='function', vtype='function',
                           return_type=node.return_type,
                           definition=node,
                           name=node.signature.name,
                           signature=node.signature,
                           body=node.body,
                           arguments=node.signature.arguments,
                           arity=node.signature.arguments.children.len(),
                           parent=node.parent)
        namespace[node.name] = fnode
        for p in fnode.arguments.children:
            namespace[p.name] = None
        # breakpoint()
        result = node.with_attr('body', node.body.resolve_names(namespace))
        fnode.arguments.children.map(lambda x: namespace.pop(x.name))
        return result

    if node.type in ['start', 'program', 'form', 'block', 'statement',
                     'call', 'expression', 'declaration', 'expression']:
        print(f'Resolving names in {node.type}')
        return node.with_attr('children',
                              node.children.map(lambda x: x.resolve_names(namespace)))

    if node.type in ['operation', 'tuple', 'bin_op', 'literal']:
        print(f'Resolving names in {node.type}')
        return node.with_attr('children',
                              node.children.map(lambda x: x.resolve_names(namespace)))

    if node.type in ['OPERATOR', 'STRING', 'INT']:
        return node

    if node.type == 'IDENTIFIER':
        # assert isinstance(node, Token)
        print(f'Dereferencing name {node.value}')
        if node.value not in namespace:
            raise_error('name resolution', f"""\
                        {node.value} not defined when used at line {node.line};
                        make sure that name is defined and in scope.""")
        # breakpoint()
        return namespace[node.value]

    raise NotImplementedError(node.type)
    # self.children.map(lambda x : x.infer_types())
    # return node
