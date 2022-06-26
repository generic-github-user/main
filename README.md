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
