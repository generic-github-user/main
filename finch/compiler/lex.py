import string
from ftoken import Token
from chartype import CharType


def lex(source: str) -> list[Token]:
    tokens = []
    line = 0
    col = 0
    for c in source:
        chartype = None
        if c in string.ascii_letters:
            chartype = CharType.Letter
        elif c in string.digits:
            chartype = CharType.Digit
        elif c in string.whitespace:
            chartype = CharType.Whitespace
        # elif c == '\n':
        #    chartype = CharType.Newline
        elif c == '"':
            chartype = CharType.Quote
        elif c in string.punctuation:
            chartype = CharType.Punctuation
        else:
            raise SyntaxError(f'Unknown character type: {c}')

        if not tokens or\
                chartype != tokens[-1].type or\
                c in '()':
            tokens.append(Token(c, chartype, line=line, column=col))
        else:
            tokens[-1].content += c

        col += 1
        if c == '\n':
            line += 1
            col = 0
    # print(tokens)
    return tokens


# class NodeType:
#    Int = 0
#    Float = 1
#    String = 2
