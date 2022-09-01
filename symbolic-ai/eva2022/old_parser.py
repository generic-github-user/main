def parseExpression(ex):
    frame = []
    valueType = None
    value = None
    for c in ex:
        if c in string.digits:
            if valueType == 'num':
                value += c
            else:
                # last = frame
                frame.append(value)
                value = c
                valueType = 'num'
        elif (c in '+-*/^'):
            if valueType == 'op':
                value += c
            else:
                frame.append(value)
                value = c
                valueType = 'op'
