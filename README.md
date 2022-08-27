# main

An experimental [monorepo](https://en.wikipedia.org/wiki/Monorepo) for some of
my projects. Most of the existing projects that I've cloned into this
repository will continue to be developed independently in their corresponding
repositories, but I'm hoping to ameliorate some of the code duplication issues
and other maintenance headaches I've run into recently.

## Branches

- leetcode: some of my solutions to programming problems from [leetcode.com](https://leetcode.com/)
- geometry: helper classes for geometry in Python that I've been copy-pasting around periodically for the last 18 months or so (and actually one of the main reasons for creating this monorepo)
- meta: information about this repository itself (code statistics, file listings, issue metadata, etc.)
- pythings: useful tools and scripts for the boring parts of Python (mainly writing tests, documentation, etc.)
- obfuscation: code obfuscation tools repurposed from an old repository of mine

## Statistics


cloc|github.com/AlDanial/cloc v 1.82  T=0.02 s (2041.8 files/s, 219324.6 lines/s)
--- | ---

Language|files|blank|comment|code
:-------|-------:|-------:|-------:|-------:
Markdown|17|274|0|920
Python|5|188|344|716
Bourne Shell|2|77|102|449
JSON|1|0|0|185
vim script|2|10|13|15
TOML|2|4|1|14
Rust|1|2|2|13
YAML|1|0|0|1
--------|--------|--------|--------|--------
SUM:|31|555|462|2313


## Tree

```
.
├── ao
│   ├── ao.sh
│   ├── command_docs.md
│   ├── docinfo.json
│   ├── README.md
│   ├── README.src.md
│   ├── todo
│   │   ├── cflags
│   │   ├── todo_ft.vim
│   │   └── todo.vim
│   └── utodo.sh
├── board
│   └── README.md
├── build.py
├── c2s
│   └── README.md
├── captcha
├── clover
│   ├── Cargo.lock
│   ├── Cargo.toml
│   └── src
│       └── main.rs
├── finch
│   └── README.md
├── generic-github-user
│   ├── docs
│   │   ├── _config.yml
│   │   └── index.md
│   └── README.md
├── obfuscation
│   ├── caterpillar.py
│   └── LICENSE.md
├── pythings
│   ├── build.py
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── pythings.py
│   ├── README.md
│   └── README.src.md
├── README.md
├── README.src.md
├── tetris-variants
│   └── README.md
├── transpiler
├── unicode-art
├── utils
│   ├── build.py
│   ├── mv.py
│   ├── README.md
│   └── README.src.md
└── zeal
    └── README.md

17 directories, 35 files

```

