import textwrap


def raise_error(etype, message):
    wrapped = textwrap.dedent(message).replace("\n", " ")
    print(f'Compiler error ({etype} error): {wrapped}')
    quit()
