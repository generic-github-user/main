# ap

*ao-python*

An alternative to the shell-based version of the ao codebase, which is
beginning to show issues with maintainability and scalability. Rust, Lisp, and
zx were also considered (among other languages), but Python's interoperability
(particularly, the massive ecosystem of useful packages and libraries) and
convenience made it the best choice for this next iteration. Another advantage
is how seamlessly pickling/serialization integrate with Python's object model,
permitting fluid development of customized classes that are easy for humans to
interact with.

The core philosophy is the same: track everything, always; and make things
easier for the user (myself in particular), even at the expense of speed or
mathematical elegance. This tool implements many functionalities (file
tracking, bookmark management) that I had been planning to design standalone
tools for; I still might in the future, but being tied to an established API
inhibits rapid prototyping and generalization makes it more time-consuming to
tailor functionality to my needs (though I still try to follow practices like
DRY for the sake of maintainability and consistency as the codebase grows).

At this point, the Python branch is my preferred tool and I'm unsure to what
extent (if any) I will continue developing and/or maintaining the shell
version. It should go without saying that this toolkit is tailored to my needs
and some of the design choices may seem unconventional; regardless, I think the
code is reasonably clean and comprehensible so you shouldn't run into very many
issues modifying or extending it.

## Features

Essentially the same as ao/master; they generally fall into one of these
categories:

- File tracking and automated backups (and searching, archiving, alerts, etc.)
- Ergonomic text-based todo lists
- Bookmark and history management, web crawling/archival, information management, etc.

One key difference is that this version is designed to allow productive
interaction with the internal data via a REPL loop, a feature which is unwieldy
in most other languages (or even in Python with more rigid data structures;
graphs are great for generality and symbolic inference, but often very irksome
to access by hand).

## Installation

Clone this repository, then execute the main script using Python (version 3.10
recommended). The `-i` flag can be used to open a REPL for interactive use. If
you plan on using the script frequently (via the shell), I'd recommend adding
something like the following to your `.bashrc`/`.zshrc`/etc (the path will of
course need to be adjusted).

```
alias ap='python ~/Desktop/ao/ap/ap.py'
alias api='python -i ~/Desktop/ao/ap/ap.py'
```

## Usage

TODO

## Branches

- `ap-docs`: documentation specific to ap
- `ap-restructuring`: reorganizing the codebase for the Python version into distinct modules
- `ap-todo`: updated todo list handling with fewer edge cases
- `command-line`: CLI for `python`
- `comments`: more thoroughly documenting the `python` branch and its associated branches (see also: `ap-docs`)
- `docs`: documentation, comments, etc.
- `file-processing`: alternate version of `files` corresponding to `python`; parent to `images` and other related branches
- `files`: file tracking code (obsolete-ish)
- `images`: sub-branch of `python`; extracting data from images using OCR and other methods
- `master`: original (shell-based) version of ao
- `notes`: note-taking and search functionality
- `plotting`: helpful functions for visualizations, graphs, etc.
- `python`: the Python-based version of ao (i.e., ap); also used as a parent branch for more specialized features
- `system-monitoring`: recording historical information about processor usage, core temperature, available memory, etc.
- `todo-handling`: scripts that manage todo lists
- `web`: web crawling/indexing tools, bookmark management, etc.
