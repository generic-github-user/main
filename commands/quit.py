from commandhandler import command

# bind database to all command functions?
@command('quit')
def quitCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    # say('Goodbye')
    quit()
