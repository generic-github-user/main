# main

[![CodeFactor](https://www.codefactor.io/repository/github/generic-github-user/main/badge)](https://www.codefactor.io/repository/github/generic-github-user/main)
[![tokei](https://img.shields.io/tokei/lines/github/generic-github-user/main)](https://github.com/generic-github-user/main)

An experimental [monorepo](https://en.wikipedia.org/wiki/Monorepo) for some of
my projects. Most of the existing projects that I've cloned into this
repository will continue to be developed independently in their corresponding
repositories, but I'm hoping to ameliorate some of the code duplication issues
and other maintenance headaches I've run into recently.

Other projects of mine are integrated through git submodules, branch merges,
and git's subtree tool, depending on what seems most appropriate. After the
repositories are combined, I sometimes make a point of ceasing development in
the original repository and treating this one as a single source of truth;
seeing as most of these projects were already inactive, I haven't run into too
many issues. `projects.yaml` stores metadata about each major project,
including its current development status and how close it is to completion.
`build.py` pulls information from various sources to generate `README.md`,
using `README.src.md` as a template and substituting the outputs of commands
from `substitutions.yaml`.

I find gratuitous use of git branches helpful for organization; this repository
has several dozen, and I freely merge components between branches as needed.
I'm less cautious about merging into the mainline (currently `/master`) here
than in some of my other repos since there is no unified public API that needs
to remain stable. I plan to integrate more third-party tooling in the future
and complete some heavy refactoring of old projects that I am interested in
further developing or reusing components from.

## Branches

- `geometry`: helper classes for geometry in Python that I've been copy-pasting
	around periodically for the last 18 months or so (and actually one of the
	main reasons for creating this monorepo)
- `leetcode`: some of my solutions to programming problems from
	[leetcode.com](https://leetcode.com/)
- `meta`: information about this repository itself (code statistics, file
	listings, issue metadata, etc.)
- `obfuscation`: code obfuscation tools repurposed from an old repository of
	mine
- `pythings`: useful tools and scripts for the boring parts of Python (mainly
	writing tests, documentation, etc.)
- `unicode-art`: scripts and command-line tools for generating diagrams,
	charts, and other materials using ASCII and/or Unicode characters
- `graphs`: Python graph classes and functions that I find myself rewriting
	often for different projects
- `packings`: polyomino tiling simulations (also see the source repository on
	my GitHub profile)
- `wordle-variants`: various language-based guessing games

## Statistics

[[stats]]

## Tree

```
[[tree]]
```

## History

```
[[history]]
```
