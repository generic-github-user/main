from commandhandler import command
from global import Eva
database = Eva.database

import pyparsing
expr = pyparsing.infixNotation(
    operand,
    [
        (".", 2, pyparsing.opAssoc.LEFT),
        (";", 2, pyparsing.opAssoc.LEFT),
        ("/", 2, pyparsing.opAssoc.LEFT),
        (">", 2, pyparsing.opAssoc.LEFT),
        ("^", 2, pyparsing.opAssoc.LEFT),
        ("?", 2, pyparsing.opAssoc.LEFT),
    ],
)

@command('@')
def queryCommand(newInput):
    parsed = expr.parseString(newInput[1:])
    print('Parsed as:')
    print(parsed)
    def queryGenerator(query):
        def newQuery():
            output = database.filter(lambda n: n.value==query[0][0])[0]
            for ci in range((len(query[0])-1)//2):
                # A, op, B = cond
                op, B = query[0][ci*2+1:ci*2+3]
                if op == '/':
                    func = lambda n: n.adjacent(B, return_ids=False)
                elif op == '^':
                    func = lambda n: n.referrers()
                # elif op == ';':
                #     func = lambda g: [think(n.id) for n in g]
                # output = output.nodeFilter(func)
                output = func(output)

                # database.addNode('user_selection')
            # selection = output
            return output
        return newQuery

    Q = queryGenerator(parsed)
    results = Q()
    say(f'Found {len(results)} matching nodes')
    say('Updating selection')
    Eva.selection = results
    print(results)
    for r in results:
        print(r)
    return results
