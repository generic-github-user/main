import time
import copy
from .loadcfg import config
from lib.pylist import List


# Represents a task or entry in a todo list, possibly with several sub-tasks
class todo:
    # Initialize a new todo item
    def __init__(self, raw, content='', config=None, **kwargs):
        # The original text from which this todo item was parsed
        self.raw = raw

        # The "text" or content of the todo item (excludes tags and other
        # metadata/markup)
        self.content = content

        # A boolean flag indicating whether the corresponding task is complete
        self.done = False

        # A timestamp indicating when this item was marked as complete
        # (actually reflects the first occasion on which the script was rerun
        # after the file was modified)
        self.donetime = None

        # A (chronologically ordered) set of "snapshots" reflecting every
        # processed todo item that was considered a match to the "canonical"
        # version of the task in the database (currently unused for efficiency
        # reasons)
        self.snapshots = []

        # Tags used to mark various properties about the task (item) -- these
        # are sometimes further processed into special attributes like
        # todo.done and todo.duration
        self.tags = []
        self.flags = {}

        # unused
        self.source = None

        # The time at which the todo instance representing this item was first
        # created
        self.created = time.time()
        self.importance = 0

        # This might be used in the future but for now is just somewhat
        # redundant metadata; if we incorporate positional context when
        # analyzing lists we may as well be writing an entire version control
        # system
        self.line = None

        # The file (specific todo list) in which the item currently resides;
        # this is often modified during processing so that when the lists are
        # rewritten the item is moved to a new file
        self.location = ''
        self.time = None
        self.duration = None
        self.frequency = None

        # Nested tasks/children of this item; currently unused due to parsing
        # limitations (the eventual goal is to integrate the zeal markup
        # parser, though the block indentation parser might be factored out
        # into a separate module)
        self.sub = []
        self.parent = None
        self.config = config

    def clone(self):
        return copy.copy(self)

    def with_attr(self, k, v):
        result = self.clone()
        setattr(result, k, v)
        return result

    # Convert this item to a string representation of the form used in the todo
    # files (i.e., `content [*] #tag1 #tag2 -t [date] [--]`)
    def toraw(self):
        # if not hasattr(self, 'config'):
        # self.config = 

        # don't blame me, blame whoever decided that overloading the
        # multiplication operator was okay
        return List(['*' * self.importance,
                     f"[{self.time.strftime('%m-%d')}]" if self.time is not None else '',
                     self.content,
                     ' '.join('#'+t for t in self.tags),
                     ' '.join(f'-{k}{f" {v}" if v is not None else ""}'
                              for k, v in self.flags.items()),
                     f' {config.complete_symbol}' * self.done])\
                .filter(lambda x: x != '').join(' ')

    # Generate a string summarizing this instance
    def __str__(self):
        inner = [f'"{self.raw}"', f'<{self.tags}>']
        # inner = "\n\t".join(inner)
        inner = ' '.join(inner)
        return f'todo {{ {inner} }}'
