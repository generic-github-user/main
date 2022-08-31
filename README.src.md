# main

[![CodeFactor](https://www.codefactor.io/repository/github/generic-github-user/main/badge)](https://www.codefactor.io/repository/github/generic-github-user/main)
[![tokei](https://img.shields.io/tokei/lines/github/generic-github-user/main)](https://github.com/generic-github-user/main)

## Contents

[[toc]]

## Overview

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

## Projects

[[projects]]

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

## On Monorepos

Here's a sampling of links you might find interesting if you're considering
doing something like this:

- https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/fulltext
- https://presumably.de/monorepos-and-the-fallacy-of-scale.html
- https://medium.com/@mattklein123/monorepos-please-dont-e9a279be011b
- https://blog.afoolishmanifesto.com/posts/personal-monorepo/
- https://news.ycombinator.com/item?id=23483436
- https://betterprogramming.pub/the-pros-and-cons-monorepos-explained-f86c998392e1

These were the concerns that were most salient to me when I was first
considering whether (and to what extent) I wanted to incorporate a monorepo
structure into my workflow:

*favorable*

- being able to update a build script or some piece of "glue" code that
	operates across multiple projects just once can significantly enhance
	productivity and overall neatness
- empirically, I'm more motivated to revisit old projects when they are easily
	accessible and tightly integrated with more recent work
- I have many custom helper functions, data structure classes, etc. that don't
	necessarily constitute one or more complete software libraries but are still
	used across many of my projects; having everything in one place makes code
	deduplication much less painful and allows me to rapidly revise somewhat
	large subsets of my codebase on which many other parts are dependent
- I want to be able to continuously enforce a consistent style across all my
	code without manually configuring a tool across dozens of different
	repositories (even if this style changes over time)

*unfavorable*

- access control is much less straightforward in a monorepo setup, and I have
	several private repositories that would ideally be integrated with my other
	code

*n/a*

- scale: I doubt this repository will exceed a gigabyte in size anytime in the
	near future, so my current tooling is more than efficient enough
- versioning: this is also mentioned near the top of the page, but most of my
	projects are experiments or personal scripts rather than software packages or
	libraries that need to maintain a stable public API; thus the difficulty of
	per-project versioning in a monorepo is not a significant drawback for me

## Tree

```
[[tree]]
```

## History

```
[[history]]
```
