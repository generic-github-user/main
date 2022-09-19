from token import Token
from node import Node, Block, String, Tuple, Array, Call, Expression, Comment,\
                Operation, Operator, Int, Float, Symbol
from chartype import CharType


def parse(tokens: list[Token]) -> Node:
    tree = Block()
    stack = [tree]
    current = tree
    depth = 0
    for token in tokens:
        current = stack[-1]
        depth = len(stack)
        if isinstance(current, String) and token.type != CharType.Quote:
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
                            stack.append(nnode_inner)

                        current.add(nnode)
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

                if token.content in ["+", "-", "*", "**", "/", "//", "%",
                                     "<", "<=", ">", ">=", "==", "!=",
                                     "^", "|", "&", "!", "~",
                                     "->", ".", "..", "@", "+-"]:
                    # current.add(Operator([token]))
                    nnode = Operation(
                        [current[-1], Operator([token], depth=depth)],
                        # op=Operator([token])
                        depth=depth
                    )
                    current[-1] = nnode
                    stack.append(nnode)

            case CharType.Letter:
                current.add(Symbol([token]))
                if isinstance(current, Operation):
                    stack.pop()

            case CharType.Digit:
                current.add(Int([token], depth=depth))
                if isinstance(current, Operation):
                    stack.pop()

            case CharType.Whitespace:
                pass

            case CharType.Newline:
                if isinstance(current, Comment):
                    stack.pop()

            case _:
                print(tree)
                print(token)
                raise SyntaxError
    return tree
