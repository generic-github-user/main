# ao.sh

## Requirements

- tesseract
- Python
- curl
- bash (recent)

## Installation

`git clone` this repository and copy the script to a convenient location.

I also recommend adding something like the following to your `.bashrc`:
```
alias ao=bash ~/Desktop/ao.sh
```

## Todo Management

The bash script `utodo.sh` processes plaintext todo lists. By default, it
expects a `todo.txt` and `recurring.txt` to exist, though these can be easily
changed. Both files are formatted with one item/task per line; by convention,
the name/description of the task appears first (though this is not technically
necessary), potentially followed by space-separated options (flags and possibly
arguments, a la bash) and metadata. Completed tasks are marked with `--`; these
are dumped to the archive `complete.txt`.

For example:

```
organize desktop files -f d -d 5m
```

This item, if placed in `recurring.txt`, will be appended (with a date
inserted) to the main todo list once a day; if already present in that list or
`complete.txt`

The possible arguments are as follows, though it is simple enough to add more.

- `archive`: The task is treated as being "completed" and removed from the main
  list, but this flag indicates that it was not actually done for some reason.
  `cc` (cancelled) is an alias.
- `frequency` or `f`: How often a task should be repeated
- `daily`: An alias for `-f d`
- `duration` or `d`: Approximately how long this task will take to complete
  once; its argument is a nonnegative integer followed by `m` for "minutes" or
  `h` for "hours"

Some other symbols provide a more readable shorthand interface to these options:

- `*`, `**`, ...: Indicate task priority/importance or urgency (or another
  property the user finds useful)

### Syntax Highlighting

For classic vim, copy (or symlink, e.g. using `ln -s ...`) `todo.vim` to
`~/.vim/syntax` and `todo_ft.vim` to `~/.vim/ftdetect`. For neovim, replace
`~/.vim` with `~/.config/nvim`. The new highlighting should be automatically
applied to all `.todo` files. By default, all URLs and flags/arguments are
highlighted.

### Workflow

I personally find it helpful to keep `todo.txt` open as a vim tab (I use
neovim, either is fine) and periodically refer to/update it (though any text
editor should work fine). This makes it very ergonomic to mark a task as
complete using `A--`, then repeat it on other tasks using `.`.
`<CTRL+V><movement>0I|$A<text><esc>` are quite useful for prepending or
appending to a set of lines (similarly, you can use `sed` or `awk` commands for
more advanced manipulations).

`bash (ao/)utodo.sh` can be run from a terminal or directly in vim using the
`!` command prefix; the latter method is preferable since it will immediately
reload the buffer. If updated externally, use `:e` to update the buffer. Some
guidance on automatically reloading the file can be found
[here](https://superuser.com/questions/181377/auto-reloading-a-file-in-vim-as-soon-as-it-changes-on-disk)
and
[here](https://unix.stackexchange.com/questions/149209/refresh-changed-content-of-file-opened-in-vim/383044#383044).
