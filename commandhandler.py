command_list = {}

def command(prefix):
    if not isinstance(prefix, str):
        raise TypeError

    def command_decorator(func):
        # commands.append(func)
        command_list[prefix] = func
        return func
    return command_decorator
