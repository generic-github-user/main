from ftoken import Token
from node import Node, Block, String, Tuple, Array, Call, Expression, Comment,\
                Operation, Operator, Int, Float, Symbol
from chartype import CharType


# TODO: make parser recursive?
def parse(tokens: list[Token]) -> Node:
    tree = Block()
    stack = [tree]
    current = tree
    depth = 0
    indentlevel = 0
    indentexpr = '    '
    for token in tokens:
        current = stack[-1]
        depth = len(stack)
        if isinstance(current, String) and token.type != CharType.Quote:
            current.add(token)
            continue
        if isinstance(current, Comment) and '\n' not in token.content:
            current.add(token)
            continue
        match token.type:
            case CharType.Quote:
                if isinstance(current, String):
                    stack.pop()
                else:
                    nnode = String()
                    current.add(nnode)
                    stack.append(nnode)

            case CharType.Punctuation:
                match token.content:
                    case "(":
                        nnode = Tuple()
                        if isinstance(current[-1], Expression):
                            nnode_inner = Call(
                                [current[-1], nnode],
                                depth=depth
                            )
                            current[-1] = nnode_inner
                            # stack.append(nnode_inner)

                        # current.add(nnode)
                        stack.append(nnode)

                    case ")":
                        stack.pop()

                    case "[":
                        nnode = Array()
                        current.add(nnode)
                        stack.append(nnode)

                    case "]":
                        stack.pop()

                    case "#":
                        nnode = Comment()
                        current.add(nnode)
                        stack.append(nnode)

                    case _:
                        if token.content in ["+", "-", "*", "**", "/", "//", "%",
                                             "<", "<=", ">", ">=", "==", "!=",
                                             "^", "|", "&", "!", "~", ">>", "<<",
                                             "->", ".", "..", "@", "+-", "="]:
                            # current.add(Operator([token]))
                            if not current.children:
                                # raise SyntaxError(stack)
                                raise SyntaxError
                            nnode = Operation(
                                [current[-1], Operator([token], depth=depth)],
                                # op=Operator([token])
                                depth=depth
                            )
                            current[-1] = nnode
                            stack.append(nnode)
                        else:
                            raise SyntaxError(token)

            case CharType.Letter:
                current.add(Symbol([token]))
                if isinstance(current, Operation):
                    stack.pop()

            case CharType.Digit:
                current.add(Int([token], depth=depth))
                if isinstance(current, Operation):
                    stack.pop()

            case CharType.Whitespace:
                if token.content.startswith('\n'):
                    # indent = len(token.content[1:])
                    indent = len(token.content.replace('\n', ''))
                    print(f'Indent level: {indent}')
                    if isinstance(current, Block):
                        if indent > indentlevel:
                            print('Found implied INDENT token')
                            nnode = Block()
                            current.add(nnode)
                            stack.append(nnode)
                        elif indent < indentlevel:
                            assert (indentlevel - indent) // len(indentexpr) < len(stack)
                            print('Found implied DEDENT token')
                            for i in range((indentlevel - indent) // len(indentexpr)):
                                stack.pop()
                        else:
                            assert indent == indentlevel
                    indentlevel = indent
                # not needed, just to indicate that other whitespace is ignored
                else:
                    pass

                if '\n' in token.content:
                    if isinstance(current, Comment):
                        stack.pop()

            # case CharType.Newline:
            #    if isinstance(current, Comment):
            #        stack.pop()

            case _:
                print(tree)
                print(token)
                raise SyntaxError
    return tree
