def plural(a, b, prepend=False):
    if b != 1:
        if a[-1] == 'y':
            a = a[:-1] + 'ies'
        elif a[-1] != 's':
            a += 's'
    if prepend:
        a = f'{b} {a}'
    return a


