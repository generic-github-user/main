<!--  This file was automatically generated from          -->
<!--  README.src.md; you should edit that file instead.   -->
<!--  Any changes made to this file will be overwritten   -->
<!--  the next time build.py is executed.                 -->




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

## Projects

- pythings  `tools` `utilities` `metaprogramming`
- obfuscation  `tools` `security` `languages`
- unicode-art  `graphics` `diagrams` `tools`
- leetcode  `programming-challenges` `leetcode` `algorithms`
- geometry  `libraries` `mathematics` `geometry` `analysis`
- graphs  `libraries` `mathematics` `graphs` `graph-theory` `data-structures`
- captcha  `hci` `security` `experiments`
- zeal  `serialization` `markup` `file-formats`
- ao 
- board  `mathematics` `combinatorics` `board-games` `simulations` `chess`
- transpiler  `programming-languages` `transpilers` `compilers`
- finch  `programming-languages` `new-language` `compilers` `transpilers` `experimental`
- clover  `ai` `ml` `mathematics` `optimization`
- c2s  `programming-languages` `new-language` `compilers` `transpilers` `experimental`
- utils  `unix` `utilities` `tools` `scripting` `command-line`
- tetris-variants  `games` `tetris` `interactive`
- generic-github-user  `meta` `profile`
- packings  `mathematics` `combinatorics` `simulations` `geometry`
- englint 
- set 
- grammars 
- chrestomathy 
- CA2 
- CogBench 
- Time-Zone-Roles  `discord-bot` `automation`
- Blender  `add-ons` `extensions` `3d-graphics` `blender`
- quickplot  `plotting` `graphs` `tools` `libraries` `matplotlib`
- epidemic-modelling  `mathematics` `modelling` `simulations` `dynamical-systems`
- fractals  `fractals` `mathematics` `graphics` `numerical-analysis` `dynamical-systems`
- ascii-physics-sim  `ascii` `physics` `simulations` `experiments`
- self-avoiding-walks  `mathematics` `combinatorics` `analysis` `simulations` `random-walks`
- python-experiments  `tools` `utilities` `metaprogramming` `experiments` `programming-languages`
- python-snippets  `tools` `utilities` `templates` `programming-languages` `helpers` `libraries`
- shelf  `tools` `utilities` `software` `command-line` `organization` `notes`
- locus 
- punchcard 
- wordtetris 
- alexandria 
- roulette-curves 
- cellular-automata-experiments 
- foldz 
- programming-puzzles 
- visual-computing-simulation 
- project-summary 

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


cloc|github.com/AlDanial/cloc v 1.82  T=0.11 s (2380.4 files/s, 368363.4 lines/s)
--- | ---

Language|files|blank|comment|code
:-------|-------:|-------:|-------:|-------:
Python|100|2306|2811|7314
HTML|15|2061|35|6012
Markdown|44|644|0|4879
Jupyter Notebook|13|0|5687|2134
C|20|357|403|2007
YAML|20|89|26|829
Bourne Shell|3|77|102|452
C/C++ Header|18|87|69|324
INI|4|52|0|248
JSON|5|0|0|226
make|4|41|6|103
JavaScript|1|7|30|95
Rust|2|19|19|89
XML|2|4|0|52
TOML|4|8|2|26
vim script|2|10|13|15
--------|--------|--------|--------|--------
SUM:|257|5762|9203|24805


## Tree

```
.
├── ao
│   ├── ao.sh
│   ├── ap
│   │   ├── ap.py
│   │   ├── files.py
│   │   ├── README.md
│   │   ├── todo.py
│   │   └── utils.py
│   ├── command_docs.md
│   ├── docinfo.json
│   ├── README.md
│   ├── README.src.md
│   ├── todo
│   │   ├── cflags
│   │   ├── todo_ft.vim
│   │   └── todo.vim
│   └── utodo.sh
├── build.py
├── ca2
│   ├── abbrs.txt
│   ├── array
│   │   ├── array.c
│   │   ├── array.c0
│   │   ├── array.h
│   │   ├── array_op.ct
│   │   └── array_reduce.ct
│   ├── build.py
│   ├── ca.c
│   ├── ca.c0
│   ├── colors
│   │   ├── colors.c
│   │   └── colors.c0
│   ├── commands
│   │   ├── commands.c
│   │   ├── commands.c0
│   │   ├── commands.h
│   │   ├── enumerate_cmd.ct
│   │   ├── print_cmd.ct
│   │   ├── randomstate_cmd.ct
│   │   ├── render_cmd.ct
│   │   ├── simulate_cmd.ct
│   │   └── write_cmd.ct
│   ├── graph
│   │   ├── graph.c
│   │   ├── graph.c0
│   │   └── graph.h
│   ├── hashing
│   │   ├── hashing.c
│   │   ├── hashing.c0
│   │   └── hashing.h
│   ├── helpers
│   │   ├── helpers.c
│   │   ├── helpers.c0
│   │   └── helpers.h
│   ├── image
│   │   ├── image.c
│   │   ├── image.c0
│   │   └── image.h
│   ├── list
│   │   ├── list.c
│   │   └── list.h
│   ├── mainheaders.h
│   ├── makefile
│   ├── plot
│   │   ├── plot.c
│   │   ├── plot.c0
│   │   ├── plot.h
│   │   └── plot.py
│   ├── progress
│   │   ├── progress.c
│   │   └── progress.h
│   ├── README.md
│   ├── README.src.md
│   ├── rule
│   │   ├── rule.c
│   │   ├── rule.c0
│   │   └── rule.h
│   ├── session.c
│   ├── session.h
│   ├── simulate
│   ├── simulation
│   │   ├── simulation.c
│   │   ├── simulation.c0
│   │   └── simulation.h
│   ├── state
│   │   ├── extract.ct
│   │   ├── ptr_reduce.ct
│   │   ├── state.c
│   │   ├── state.c0
│   │   └── state.h
│   ├── test
│   │   └── test.h
│   ├── timeinfo.c
│   ├── timeinfo.h
│   ├── tinypng
│   │   ├── TinyPngOut.c
│   │   └── TinyPngOut.h
│   ├── todo.txt
│   ├── typing
│   │   ├── typing.c
│   │   ├── typing.c0
│   │   └── typing.h
│   └── vector
│       ├── vector.c
│       ├── vector.c0
│       └── vector.h
├── captcha
├── clover
│   ├── Cargo.lock
│   ├── Cargo.toml
│   └── src
│       └── main.rs
├── consequi
│   ├── duration.py
│   ├── main.py
│   ├── README.md
│   ├── settings.py
│   ├── tag.py
│   └── task.py
├── decision-tree-experiments
│   ├── game.py
│   ├── main.py
│   ├── node.py
│   ├── README.md
│   └── tree.py
├── diagrammar
│   ├── main.py
│   ├── object.py
│   └── README.md
├── generic-github-user
│   ├── docs
│   │   ├── _config.yml
│   │   └── index.md
│   └── README.md
├── icon-encoder
│   ├── README.md
│   ├── screenshots
│   │   ├── Figure_1-1 (2).png
│   │   ├── Figure_1-1.png
│   │   ├── Figure_1-2 (2).png
│   │   ├── Figure_1-2.png
│   │   ├── Figure_1 (2).png
│   │   ├── Figure_1-3 (2).png
│   │   ├── Figure_1-3.png
│   │   ├── Figure_1-4 (2).png
│   │   ├── Figure_1-4.png
│   │   ├── Figure_1-5 (2).png
│   │   ├── Figure_1-5.png
│   │   ├── Figure_1-6.png
│   │   ├── Figure_1-7.png
│   │   ├── Figure_1-8.png
│   │   ├── Figure_1-9.png
│   │   └── Figure_1.png
│   └── src
│       └── main.py
├── keyboard-dynamics
│   ├── keyboard.py
│   ├── LICENSE
│   └── README.md
├── languages
│   ├── c2s
│   │   └── README.md
│   ├── finch
│   │   └── README.md
│   └── locus
│       └── locus.ipynb
├── leetcode
│   ├── 1436.py
│   ├── 1528.py
│   ├── 1869.py
│   ├── 39.py
│   └── 796.py
├── lib
│   ├── graphs
│   │   ├── completegraph.py
│   │   ├── giraffe.ipynb
│   │   ├── giraffe.py
│   │   ├── graph.py
│   │   ├── gridgraph.py
│   │   ├── manual_testing.py
│   │   ├── node.py
│   │   ├── randomgraph.py
│   │   └── randomizer.py
│   ├── micronotes
│   │   ├── demo.html
│   │   ├── LICENSE
│   │   ├── micronotes.js
│   │   ├── README.md
│   │   └── screenshots
│   │       ├── 1.png
│   │       ├── 2.png
│   │       └── 3.png
│   ├── punchcard
│   │   └── dataclass.py
│   ├── pythings
│   │   ├── build.py
│   │   ├── pythings.py
│   │   ├── README.md
│   │   └── README.src.md
│   ├── quickplot
│   │   ├── quickplot.py
│   │   └── requirements.txt
│   └── zeal
│       └── README.md
├── mathematics
│   ├── combinatorics
│   │   ├── board
│   │   │   └── README.md
│   │   ├── grammars
│   │   │   ├── Cargo.lock
│   │   │   ├── Cargo.toml
│   │   │   ├── README.md
│   │   │   └── src
│   │   │       └── main.rs
│   │   ├── packings
│   │   │   ├── packings.c
│   │   │   ├── packings.py
│   │   │   └── README.md
│   │   ├── random-walks
│   │   │   ├── docker-compose.yml
│   │   │   ├── docs
│   │   │   │   ├── _config.yml
│   │   │   │   ├── _data
│   │   │   │   │   └── topnav.yml
│   │   │   │   ├── feed.xml
│   │   │   │   ├── Gemfile
│   │   │   │   ├── Gemfile.lock
│   │   │   │   └── sitemap.xml
│   │   │   ├── LICENSE
│   │   │   ├── Makefile
│   │   │   ├── MANIFEST.in
│   │   │   ├── random-walks
│   │   │   │   ├── __init__.py
│   │   │   │   └── _nbdev.py
│   │   │   ├── requirements.txt
│   │   │   ├── settings.ini
│   │   │   └── setup.py
│   │   └── self-avoiding-walks
│   │       ├── self-avoiding-walk.ipynb
│   │       └── self-avoiding-walk.py
│   ├── fractals
│   │   ├── fractals.ipynb
│   │   └── README.md
│   └── symbolic-approximation
│       ├── LICENSE
│       ├── requirements.txt
│       └── symbolic-approximation.py
├── music-generation-experiments
│   ├── chord.py
│   ├── composition.py
│   ├── main.py
│   ├── melody.py
│   ├── noteinfo.py
│   ├── note.py
│   ├── pitch.py
│   ├── README.md
│   └── scale.py
├── Pipfile
├── Pipfile.lock
├── programming-puzzles
│   ├── puzzles.ipynb
│   └── puzzles.py
├── projects.yaml
├── __pycache__
│   ├── completegraph.cpython-38.pyc
│   ├── completegraph.cpython-39.pyc
│   ├── giraffe.cpython-38.pyc
│   ├── graph.cpython-38.pyc
│   ├── graph.cpython-39.pyc
│   ├── gridgraph.cpython-38.pyc
│   ├── gridgraph.cpython-39.pyc
│   ├── node.cpython-38.pyc
│   ├── node.cpython-39.pyc
│   ├── randomgraph.cpython-38.pyc
│   └── randomgraph.cpython-39.pyc
├── python-experiments
│   ├── automacro.ipynb
│   ├── automacro.py
│   ├── LICENSE.md
│   ├── processor.py
│   ├── py2english.py
│   ├── README.md
│   ├── requirements.txt
│   ├── symbolic-algebra.ipynb
│   └── symbolic-algebra.py
├── python-snippets
│   ├── README.md
│   ├── snippets.ipynb
│   └── snippets.py
├── README.md
├── README.src.md
├── simulations
│   ├── attractors
│   │   ├── 00_attractor.ipynb
│   │   ├── attractor.py
│   │   ├── attractors
│   │   │   ├── core.py
│   │   │   ├── __init__.py
│   │   │   └── _nbdev.py
│   │   ├── attractors.py
│   │   ├── CONTRIBUTING.md
│   │   ├── docker-compose.yml
│   │   ├── docs
│   │   │   ├── attractor.html
│   │   │   ├── attractors.html
│   │   │   ├── _config.yml
│   │   │   ├── _data
│   │   │   │   ├── sidebars
│   │   │   │   │   └── home_sidebar.yml
│   │   │   │   └── topnav.yml
│   │   │   ├── feed.xml
│   │   │   ├── Gemfile
│   │   │   ├── Gemfile.lock
│   │   │   ├── images
│   │   │   │   ├── output_10_1.png
│   │   │   │   ├── output_10_2.png
│   │   │   │   ├── output_12_1.png
│   │   │   │   ├── output_12_2.png
│   │   │   │   ├── output_14_2.png
│   │   │   │   ├── output_6_1.png
│   │   │   │   └── output_8_1.png
│   │   │   ├── index.html
│   │   │   ├── sidebar.json
│   │   │   └── sitemap.xml
│   │   ├── index.ipynb
│   │   ├── LICENSE.md
│   │   ├── line.py
│   │   ├── Makefile
│   │   ├── MANIFEST.in
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── rotate.py
│   │   ├── settings.ini
│   │   ├── setup.py
│   │   └── simulate.py
│   ├── cellular-automata-experiments
│   │   ├── doc-generator.py
│   │   ├── docs
│   │   │   ├── class_template.md
│   │   │   ├── method_template.md
│   │   │   └── parameter_template.md
│   │   ├── main.py
│   │   └── README.md
│   ├── epidemic-modelling
│   │   ├── epidemic-modelling.py
│   │   ├── LICENSE
│   │   └── README.md
│   ├── foldz
│   │   ├── CONTRIBUTING.md
│   │   ├── docker-compose.yml
│   │   ├── docs
│   │   │   ├── _config.yml
│   │   │   ├── _data
│   │   │   │   ├── sidebars
│   │   │   │   │   └── home_sidebar.yml
│   │   │   │   └── topnav.yml
│   │   │   ├── feed.xml
│   │   │   ├── fold.html
│   │   │   ├── Gemfile
│   │   │   ├── Gemfile.lock
│   │   │   ├── index.html
│   │   │   ├── sidebar.json
│   │   │   └── sitemap.xml
│   │   ├── FoldZ
│   │   │   ├── fold.py
│   │   │   ├── __init__.py
│   │   │   └── _nbdev.py
│   │   ├── LICENSE
│   │   ├── Makefile
│   │   ├── MANIFEST.in
│   │   ├── README.md
│   │   ├── settings.ini
│   │   └── setup.py
│   ├── physics
│   │   ├── docs
│   │   │   ├── _config.yml
│   │   │   ├── geometry.html
│   │   │   ├── helpers.html
│   │   │   ├── index.html
│   │   │   ├── main.html
│   │   │   ├── material.html
│   │   │   ├── object.html
│   │   │   ├── renderer.html
│   │   │   ├── scene.html
│   │   │   └── tensor.html
│   │   ├── geometry.py
│   │   ├── helpers.py
│   │   ├── main.py
│   │   ├── material.py
│   │   ├── object.py
│   │   ├── README.md
│   │   ├── renderer.py
│   │   ├── scene.py
│   │   ├── scripts
│   │   │   └── build-docs.txt
│   │   └── tensor.py
│   └── roulette-curves
│       └── main.py
├── substitutions.yaml
├── tetris-variants
│   └── README.md
├── todo-backup
│   ├── todo-30-08-1661911147_21-59-07.yaml
│   ├── todo-30-08-1661911208_22-00-08.yaml
│   ├── todo-30-08-1661911220_22-00-20.yaml
│   ├── todo-30-08-1661912623_22-23-43.yaml
│   ├── todo-30-08-1661912670_22-24-30.yaml
│   └── todo-30-08-1661912755_22-25-55.yaml
├── tools
│   ├── alexandria
│   │   ├── library.ipynb
│   │   └── main.py
│   ├── ao
│   │   ├── ao.sh
│   │   ├── command_docs.md
│   │   ├── docinfo.json
│   │   ├── README.md
│   │   ├── README.src.md
│   │   ├── todo
│   │   │   ├── cflags
│   │   │   ├── todo_ft.vim
│   │   │   └── todo.vim
│   │   └── utodo.sh
│   ├── cogbench
│   │   ├── 00_core.ipynb
│   │   ├── docker-compose.yml
│   │   ├── docs
│   │   │   ├── feed.xml
│   │   │   ├── Gemfile
│   │   │   ├── Gemfile.lock
│   │   │   └── sitemap.xml
│   │   ├── MANIFEST.in
│   │   ├── manual
│   │   │   ├── alternation.py
│   │   │   ├── cogbench.py
│   │   │   ├── minmax.py
│   │   │   ├── test.py
│   │   │   └── utils.py
│   │   ├── settings.ini
│   │   └── setup.py
│   ├── obfuscation
│   │   ├── caterpillar.py
│   │   └── LICENSE.md
│   ├── project-summary
│   │   ├── summarize.ipynb
│   │   └── summarize.py
│   ├── shelf
│   │   ├── base.py
│   │   ├── library.py
│   │   ├── LICENSE
│   │   ├── md_template.md
│   │   ├── note.py
│   │   ├── README.md
│   │   ├── session.py
│   │   ├── shelf.py
│   │   ├── stringb.py
│   │   ├── term.py
│   │   └── utils.py
│   ├── utils
│   │   ├── build.py
│   │   ├── mv.py
│   │   ├── README.md
│   │   └── README.src.md
│   └── ytodo.py
├── transpiler
├── unicode-art
├── update.sh
├── visual-computing-simulation
│   └── simulation.py
├── wordtetris
│   ├── LICENSE
│   └── wordtetris.py
├── yaml_json.py
└── ydone.yaml

100 directories, 374 files

```

## History

```
*   1bedcbe (HEAD -> master, origin/master) Merge branch 'diagrammer'
|\  
| *   bc1b2aa (origin/diagrammer, diagrammer) Add 'diagrammar/' from commit '449c42701c868038d6b5a8cdeff4a3e2c6a5188b'
| |\  
| | * 449c427 Create README.md
| | * 0153739 cleanup
| | * 721d83b create gitignore
| | * 4979e86 move Object class (and Arrow subclass) to new file
| | * 581ba53 create arrow class
| | * 1f84828 misc.
| | * 097aa8d add object scaling command
| | * aeac13b fix rotation bugs
| | * 97a4652 handle floats and negatives
| | * 22f776c include last block in result
| | * 6928f5b outline handling in Object class
| | * 1dccc47 add command to set border/outline width
| | * 5481435 clear canvas each time Scene.render() is called
| | * 2f59a1b add option to parse integers out of result
| | * 0b23f1d add function to split text and numbers in a string
| | * 9a1f2e8 create camera class
| | * a70dfd7 add child objects/sub-objects
| | * 76ee53a accept integer dimensions argument
| | * 53d55da add text rendering
| | * 15116f2 misc
| | * 5faef96 add object rotation command
| | * 97e2aab more comments and placeholders
| | * 063a2e1 add comments
| | * ddd724a add regular polygon generator
| | * df53849 move flip code out of specific shape drawer
| | * 9e655f4 update to use stored context
| | * eb48463 cleanup
| | * f5444ca test code
| | * ce14d43 misc
| | * 04b23b8 add method to get command inputs from user in console
| | * 5ba1528 add method to render current scene
| | * b72351b command placeholders
| | * b01a06d updates to clone method
| | * 3d990da add fill argument
| | * 992c617 add object duplication command
| | * 0d4b0a0 use context buffer (result of last command) as input for next command
| | * 0236e17 allow inputting list of command argument strings for Scene.command()
| | * 53eeb3f initialize bounds as None
| | * cf66f0f command for changing object's fill color
| | * b787902 command for moving objects
| | * d10eb49 command for adding circles to scene
| | * ad649dc add simple command processor
| | * 33ad35e add method to add objects to scene
| | * 662a577 add clear function to reset canvas
| | * 6e50b85 miscellaneous
| | * 4229f19 add direction shortcuts
| | * 5f80a13 fix Object clone method (certain attributes like the 'drawer' should be shallow copied)
| | * 2c53ebc add method to update calculated object data
| | * 300c58b add abbreviated axes (Scene.x, .y, etc.)
| | * a280ea0 add method to generate bounding box for object
| | * 675f163 add option for vertically flipping when drawing objects
| | * 340cd0c add display with pyplot imshow
| | * 34c1443 add color handling
| | * ec14ed6 create Scene class
| | * ca704c2 add Object.clone method
| | * 8e229b2 add Object.move() method
| | * 18b0ba9 add Object.draw()
| | * f833712 add Object class
| | * ada68b2 rendering tests
| | * e902d16 init and import modules
* |   91981ce Merge branch 'consequi'
|\ \  
| * \   de8e0ce (origin/consequi, consequi) Add 'consequi/' from commit '84b8e90e65ab6b24bc1ac28e2d27b8b59e2c30a0'
| |\ \  
| | |/  
| |/|   
| | * 84b8e90 add comments to backup function
| | * c0726ad add additional backup information
| | * b68b18f add compressed plaintext backups (#37)
| | * f1c4782 move command aliases to settings.py
| | *   eea56ae Merge pull request #27 from generic-github-user/remove
| | |\  
| | | *   c19be4e Merge pull request #26 from generic-github-user/backup
| | | |\  
| | | | * 4c31303 add (simple) backup functionality
| | | | * 990db07 create function to convert session data to dictionary objects
| | | | * b30802d add settings to main data file
| | | |/  
| | | * 94eaaf8 add undo task removal
| | | * d467165 add task remove/delete command
| | | * 788b56f add remove_tasks
| | |/  
| | *   f4d4d75 Merge pull request #21 from generic-github-user/archiving
| | |\  
| | | * c25b043 add task archiving
| | | * bd1062a various restructuring of search/print commands
| | | * bdb7c6a add function to get tasks in session that are not archived
| | | * 96c6a06 add method to quickly get archival state of task
| | | * 3a5f2d0 miscellaneous
| | | * f13f537 add deselect function
| | | * 6baa4d3 add selection command
| | | * 0218ddd add printing of current selection (if no arguments provided)
| | | * 4fccc91 add task searching function
| | | * 9ffa8bf add context from previous command
| | | * 25b0d51 add aliases for new commands
| | |/  
| | * e2e96ad Fix #20
| | * 52209ab compute efficiency ratio (task importance divided by estimated completion time)
| | * f2ea5d6 add multi-word tag names
| | * db068a5 move Tag class to its own file
| | * be35398 error handling
| | * bb1c7fc fix bug in argument extractor
| | * 8358de2 add duration label handling
| | * 68afb4a fix bug and add more task properties
| | * 145a9e1 add parsing of other duration formats (e.g., "5 hours, 30 minutes")
| | * b309834 add duration parser (...hh:mm:ss)
| | * d3452fb add info about different time units
| | * 93dcdc8 add get_arg function
| | * 99adf47 fix handling of multiword task entries
| | * f3944d8 fix date parsing
| | * 497c938 add task display as table (in lookup command)
| | * 6b5d5ff ignore .pyc
| | * 28c8445 move Settings and Task classes to their own files
| | * 71b56d3 add tag creation handling
| | * 63ec9bb add tag import/export functions (nearly identical to task class methods)
| | * 0180688 add entity aliases
| | * e2fb8fa fix merge conflicts
| | *   0246f57 Merge pull request #12 from generic-github-user/comments
| | |\  
| | | *   bb318c4 Merge branch 'master' into comments
| | | |\  
| | | |/  
| | |/|   
| | * | 73c693a add back missing add_task changes
| | * |   a8c08d3 Merge pull request #11 from generic-github-user/revert-10-revert-9-undo
| | |\ \  
| | | * | 54657a8 Revert "Revert "Undo""
| | |/ /  
| | * |   87ff598 Merge pull request #10 from generic-github-user/revert-9-undo
| | |\ \  
| | | * | b78b08f Revert "Undo"
| | |/ /  
| | * |   aa36521 Merge pull request #9 from generic-github-user/undo
| | |\ \  
| | | * | d84f974 remove last command from buffer once undo is complete
| | | * | c11e277 add max command/undo buffer size
| | | * | b3af7dc add undo function for ranking system
| | | * | 7049037 add undo add task command
| | | * | 509b062 restructured code to use dict as main data wrapper (tasks, tags, etc. to be stored in sub-arrays)
| | | * | a4596be create Tag class
| | |/ /  
| | | * 34022c2 add more comments
| | | * c216786 add some comments
| | |/  
| | * 9524261 fix aliases broken in previous merge commit
| | *   101b3be Merge pull request #2 from generic-github-user/ranking
| | |\  
| | | *   c9d65eb Merge branch 'master' into ranking
| | | |\  
| | | |/  
| | |/|   
| | * | 858a9c8 add short command aliases
| | * | dab969c add exit command(s)
| | | * 8046ff5 save after loading data (to apply changes made during loading process, such as format standardization/updates)
| | | * 799480e round importance scores to nearest integer value
| | | * d677f0e create simple ranking system
| | | * 4eba2cc add task IDs
| | |/  
| | *   b51fdd7 Merge pull request #1 from generic-github-user/dev
| | |\  
| | | * 6bfb883 store date as string to avoid JSON serialization error
| | | * 634b934 add command to list all tasks
| | | * eab142c only decode datestring if the task has one
| | | * 7132ee0 programmatically access task properties
| | | * 087847a parse complex date strings with https://github.com/kvh/recurrent
| | | * f601b36 add datestring storage
| | | * 9ec6018 fix data loading issue
| | * | 3a2ef2e make sure not to overwrite data file when opening
| | |/  
| | * 810f9d8 gitignore data storage files
| | * f32b1b5 add greetings
| | * 64d79f5 get commands from user (in command line/console)
| | * 8fcde78 cleanup
| | * ca4831f add command processor
| | * 13ace08 error handling
| | * 77a7a86 remove unused self argument
| | * 1cc930c add method for getting task as string
| | * ebb5559 add method for getting task as dictionary object
| | * 73310a8 create Task class
| | * 11f0f48 update function variable names
| | *   e28dcc4 Merge branch 'master' of https://github.com/generic-github-user/consequi
| | |\  
| | | * bdcc0fa Create README.md
| | * | 112b310 add functions for loading/saving data
| | |/  
| | * 54db252 initialize
* | b78388b Rebuild project
* |   c3f0a3c Merge branch 'meta'
|\ \  
* | | ec89e06 (origin/ytodo, ytodo) update .gitignore
* | | 6d10835 filter out tasks marked as complete and append to an archive file
* | | 1c18187 add simple YAML-based version of todo manager
* | | bc22647 Rebuild project
* | |   740f9e2 Merge branch 'ao'
|\ \ \  
| * \ \   c4e401d (origin/ao, ao) Add 'ao/' from commit '94f741b542116f4daa0b0e32129d217e6a455a61'
| |\ \ \  
| | |_|/  
| |/| |   
| | * |   94f741b Merge pull request #30 from generic-github-user/python
| | |\ \  
| | | * \   e4519ed Merge branch 'ap-todo' into python
| | | |\ \  
| | | | * | 468f35e improve sorting of todo items
| | | | * | db3d73f move todo items based on completion status and tags
| | | | * | e763394 clean up unused code
| | | | * | ab2e0e7 parse and integrate each todo list separately
| | | | * | 1d3f3df store paths to multiple (synced) todo lists
| | | | * | f05e213 update todo file content with new state
| | | | * | 9b19705 misc. bug fixes and logging
| | | | * | 209a6b5 automatically back up todo file(s) and database
| | | | * | 840f2b6 update stored state based on snapshots generated from todo list file
| | | | * | 3c6eedd add some high-level comments to todo.py
| | | | * | a22fcd4 add function for parsing todo statements and generating corresponding snapshots
| | | | * | b600744 fix some bugs, misc todo class improvements
| | | | * | 9e092e0 add todo class for representing items on todo list(s)
| | | * | | 1499fd0 move TODOs from ap.py to github issues
| | | * | |   cfb9569 Merge pull request #15 from generic-github-user/ap-docs
| | | |\ \ \  
| | | | * \ \   3aed490 Merge branch 'python' into ap-docs
| | | | |\ \ \  
| | | | |/ / /  
| | | |/| | |   
| | | * | | | a884211 summarize import groups
| | | * | | |   14f668c Merge pull request #12 from generic-github-user/ap-restructuring
| | | |\ \ \ \  
| | | | |_|/ /  
| | | |/| | |   
| | | | * | |   b1c0bde Merge branch 'python' into ap-restructuring
| | | | |\ \ \  
| | | | |/ / /  
| | | |/| | |   
| | | * | | | 5712f15 minor README changes
| | | * | | | 5d235f0 record sensor data from psutil
| | | | * | | fe64530 move global settings to config file
| | | | * | | d02452f move file handling classes and functions to files module
| | | | * | |   4c7277c Merge branch 'ap-restructuring' of github.com:generic-github-user/ao into ap-restructuring
| | | | |\ \ \  
| | | | | * | | d505f42 move getsize and hashfile helper functions to utils.py
| | | | |/ / /  
| | | |/| | |   
| | | | * | | b62cbb7 move getsize and hashfile helper functions to utils.py
| | | |/ / /  
| | | | * | ccd549b minor README tweaks
| | | | * |   c1bc53b Merge pull request #14 from generic-github-user/comments
| | | | |\ \  
| | | | | * | 7457912 add comments to openfiles function
| | | | | * | b8c3818 add comments to extracttext file
| | | | | * | 35de70d add some comments to tagfile and tagfiles
| | | | | * |   7bbe6a4 Merge branch 'images' into comments
| | | | | |\ \  
| | | | | | * | cc6dc4c make this version work (was originally one file, split into multiple branches to preserve my sanity and achieved the opposite effect)
| | | | | | * |   f9209ab Merge pull request #8 from generic-github-user/command-line
| | | | | | |\ \  
| | | | | | | * | fa8aeab use argparse to process subcommands supplied via the terminal
| | | | | | * | |   3701299 Merge pull request #7 from generic-github-user/file-processing
| | | | | | |\ \ \  
| | | | | | | |/ /  
| | | | | | |/| |   
| | | | | | | * | 200ad71 refactor tagfiles
| | | | | | | * | 1873a10 miscellaneous
| | | | | | | * | 25bc256 add helper function for accessing sets of files though default file manager
| | | | | | * | | d481791 use (py)tesseract to extract text from images
| | | | | | |/ /  
| | | | | | * / e0b2837 automatically tag some files based on filetype
| | | | |_|/ /  
| | | |/| | |   
| | | | | * | 303c3d7 add some comments to snapshot class
| | | | | * | 3a830da add some comments to catalog function
| | | | | * | ae11626 add more comments to filenode class
| | | | | * | 958cf96 add summary comments to other functions
| | | | * | | f73d53b add descriptions of other branches
| | | | |/ /  
| | | | * / cceab27 add summaries of some branches to README
| | | |/ /  
| | | * | a8eab31 add function for generating file snapshots (using os and pathlib)
| | | * | 6a0d2e3 add file snapshot class (in the style of Git and other VCS software)
| | | * | dab6837 add filenode class for representing files and directories
| | | * | b2a73c7 more .gitignore updates
| | | * | db832bc add feature summary to README
| | | * | 67f5d51 expand README introduction
| | | * | 931b100 add more helper functions (log and save)
| | | * | 43dd651 add some helper functions
| | | * | ef69999 add ap.py
| | | * | 1f49544 update .gitignore
| | | * | ca0a3f9 add README for Python-based version
| | * | | c53c961 copy branch descriptions from README.md in ao@ao-docs
| | * | | 01c9dd7 add link to new(-ish) python branch
| | |/ /  
| | * | 45e86d1 update requirements list
| | * |   c042f17 Merge pull request #6 from generic-github-user/todo-handling
| | |\ \  
| | | * \   a6916b2 Merge branch 'master' of github.com:generic-github-user/ao into todo-handling
| | | |\ \  
| | | |/ /  
| | |/| |   
| | * | |   24a417a Merge pull request #5 from generic-github-user/system-monitoring
| | |\ \ \  
| | | * \ \   c4faf9e Merge branch 'master' of github.com:generic-github-user/ao into system-monitoring
| | | |\ \ \  
| | | |/ / /  
| | |/| | |   
| | * | | | 4c7ebca fix minor errors and reflow README
| | * | | | 74285ff add usage instructions and command reference to README
| | * | | | eaf29a9 move syntax highlighting files and use vim highlighting groups
| | * | | | 579c347 update .gitignore
| | * | | | 7a26168 clean up some temp files, standardize paths
| | * | | | 77bdb2b misc. fixes, improve relative path consistency
| | * | | | 12e2bb3 improve path consistency in utodo.sh
| | * | | | 5428650 add SLOC statistics to README
| | * | | | 743e7bf add table of contents
| | * | | |   ff543d0 Merge pull request #4 from generic-github-user/files
| | |\ \ \ \  
| | | * \ \ \   1ac70ea Merge branch 'master' into files
| | | |\ \ \ \  
| | | |/ / / /  
| | |/| | | |   
| | * | | | | 6561b55 more feature information
| | * | | | | bddd08c add information about some features to README
| | | * | | |   da66d3c Merge pull request #3 from generic-github-user/docs
| | | |\ \ \ \  
| | | | * | | | 937fc4e include command parameters in generated documentation
| | | | * | | | d1f44d2 add documentation database file
| | | | * | | | e459f2d add subcommand (build) for generating documentation files
| | | |/ / / /  
| | | * | | | aebf4e3 reflow some of the longer lines
| | | * | | | 3c6d9ec misc updates and fixes
| | | * | | | d5fb8b2 support dry run option for cleanup subcommand
| | | * | | |   4f39ea9 Merge pull request #2 from generic-github-user/todo-handling
| | | |\ \ \ \  
| | | | | * | | 51f6119 add subcommand for recording data about available memory
| | | | | * | | 549a9a8 misc.
| | | | | * | | 8855661 add record command
| | | | | | * | e642e34 add some comments to utodo.sh
| | | | | | * | 16e43d6 add flags for tasks that recur on a weekly/monthly basis
| | | | | | * | c7324f6 various improvements to todo processing
| | | | | | * | 6e665af grab .gitignore from master
| | | | | | * | bb03314 add ao subcommand for dispatching utodo.sh
| | | | | | * | 60d7cb0 copy over path changes from master
| | | | | | * | fcded87 miscellaneous
| | | | | |/ /  
| | | | |/| |   
| | | | * | |   13a8f41 Merge branch 'files' into todo-handling
| | | | |\ \ \  
| | | | |/ / /  
| | | |/| | |   
| | | * | | | c248b2a Display output types and command parameters
| | | * | | | e3dcce6 process command parameter information
| | | * | | | 617eca7 add some comments and reformat comment blocks
| | | * | | | b716fcf process command output type markers
| | | * | | | c19189b support argument for help command
| | | * | | | 2099d41 add some more comments to shell functions
| | | * | | | c15f8e7 add command output type notations
| | | * | | | 180fa8e improve help command and documentation printing
| | | * | | | 1709898 execute commands from documentation database
| | | * | | | f28c28a add information about command parameters
| | | * | | | 06dc47c add help command for printing information about (sub)command usage
| | | * | | | 8ea5784 add function for documenting commands, parameters, etc.)
| | | * | | | f818a00 refactor commands into functions for easier maintenance and semi-automated documentation
| | | * | | | 41ec5f1 add some more comments
| | | * | | | d9f950f various improvements to cleanup subcommand and file moving
| | | * | | | ca47dc1 support JSON inputs for open subcommand
| | | * | | | c5f4013 add plain output option
| | | * | | | 0d1146f use json-based image index for imfind
| | | * | | |   d3d77a7 Merge pull request #1 from generic-github-user/notes
| | | |\ \ \ \  
| | | | * | | | 4f04f0e refactoring with db helper functions
| | | | * | | | ab303f8 add read_db and write_db helper functions
| | | | * | | | 03c5207 add helper function for extracting a database component to a new file
| | | | * | | | 2e458db add note searching functionality
| | | | * | | | 1c383dd add command for storing text-based notes in database
| | | |/ / / /  
| | | * | | | b56986f add ffind command for searching files
| | | * | | | 1d80309 cleanup and reformatting
| | | * | | | 33b1f8a convert some options to subcommands
| | | * | | | 8b05723 store file snapshot batch as stream of JSON objects (faster)
| | | * | | | 8503117 add some comments
| | | * | | | f85c2c7 misc updates to file snapshot processing
| | | * | | | c9f02f9 add summary of file tracking system
| | | * | | | b633192 generate summary statistics from file information
| | | | |/ /  
| | | |/| |   
| | | * | | b42af4c use jq to generate filenodes from snapshots
| | | * | | 8b0d8ee avoid nesting arrays when recording file information
| | |/ / /  
| | | * | c8fb87f misc
| | | * | 37bf77a add some logging
| | | * | 7af6eaf miscellaneous tips and tricks
| | | * | ccacc55 add todo workflow advice
| | | * | 8c48aa0 add custom syntax highlighting instructions
| | | * | 75345b0 add information about todo item arguments and flags
| | | * | 44526df add todo flag/option syntax highlighting
| | | * | c584710 update script to use .todo file extension
| | | * | 524807f fix some bugs in sed filters
| | | * | 946f5cb add vim scripts for todo list syntax highlighting
| | | * | 2532226 cleanup
| | | * | f5c9208 add information about utodo.sh usage
| | | * | 4c17c9c fix string escaping issues
| | | * | c487c5a improve flag handling and recurring task management
| | | * | 0d1686c misc todo backup improvements
| | | * | 9b78e1b mild refactoring
| | | * | 5a7538f back up tasks whenever update script is run
| | | * | 172ac51 generate specified instances of recurring tasks
| | | * | 1e5101e add script for handling completed tasks
| | |/ /  
| | * | 64242a2 clean up unused code
| | * | 06953bc various "improvements"
| | * | fc6c67c generate and store json data about files when generating manifest
| | * | 3e519bf more misc
| | * | 0031c80 store information about ao command call/execution, etc
| | * | 4b0c1e6 miscellaneous
| | * | 7e3c0d1 add command for generating flower-like patterns
| | * | 05ea618 extract information about text files
| | * | ac8e716 add installation instructions
| | * | 621a41b add README.md
| | * | b0f5e1c add some comments with information about commands
| | * | 045ad15 add command for fetching data from the web
| | * | bf36fd4 store only checksum (without filename)
| | * | 965d43c add command for generating summaries of directory contents
| | * | f75da58 move reorganization functionality to a (sub)command
| | * | 29bd81e improve target directory handling
| | * | 4aa142f cleanup & misc
| | * | bc3bca7 improve logging
| | * | ce328be add helper function to automatically group all files of a certain type
| | * | 9fc9016 add tool for finding images with text
| | * | 97c7c89 add command (option) for running OCR on images and generating checksums
| | * | 8b6f1cc add command for viewing search results as folder of symlinks
| | * | 15e2759 process command line options
| | * | f6d62b4 automatically organize main file types
| | * | 120e90d add additional metadata and path settings
| | * | 29a9c61 set globbing options with shopt
| |  /  
| | | * 8970ece (origin/fractals, fractals) clean up some artifacts from source notebook
| | | * ca65afb extract some functions and classes into independent modules
| | | * 58435f1 add script version of fractal generation/visualization toolkit
| | | | * f552a4d (origin/nushell-testing, nushell-testing) generate file list using script
| | | | | * 1a73bbf (refs/stash) WIP on nushell-testing: 473a935 add simple nu(shell) script for summarizing lines/tokens/characters in source code files
| | | | |/| 
| | | | | * 7825cd6 index on nushell-testing: 473a935 add simple nu(shell) script for summarizing lines/tokens/characters in source code files
| | | | |/  
| | | | * 473a935 add simple nu(shell) script for summarizing lines/tokens/characters in source code files
| | | | * 16d978d (origin/meta, meta) add discussion of monorepo pros/cons
| | | |/  
| | |/|   
| | * | ddd3d16 add notice about auto-generation of README.md (and ref to appropriate file)
| | * | 5b3e5e0 generate project list (see #16)
| |/ /  
|/| |   
* | | c5eeb81 add simple build-and-commit script
* | | 8b26b10 Rebuild project
* | |   84cf2eb (origin/ca2, ca2) Add 'ca2/' from commit '49576963f63827c0cad40c823821a5a7f9d3587a'
|\ \ \  
| |/ /  
|/| |   
| * | 4957696 generate directory listing
| * | 4ae5c9d fix some issues with state code
| * | 0ef3d31 add include guard to prevent duplicate declaration, other minor bug fixes
| * |   e84ac9a Merge pull request #108 from generic-github-user/progress-bar
| |\ \  
| | * \   6b2a8dc Merge branch 'master' into progress-bar
| | |\ \  
| | |/ /  
| |/| |   
| * | |   26004f9 Merge pull request #106 from generic-github-user/cmdline-args
| |\ \ \  
| | * \ \   60d04c5 Merge branch 'master' into cmdline-args
| | |\ \ \  
| | |/ / /  
| |/| | |   
| * | | |   2d42f8a Merge pull request #105 from generic-github-user/session
| |\ \ \ \  
| | * \ \ \   a35074a Merge branch 'master' into session
| | |\ \ \ \  
| | |/ / / /  
| |/| | | |   
| * | | | |   c518284 Merge branch 'master' of github.com:generic-github-user/CA2
| |\ \ \ \ \  
| | * \ \ \ \   e8a265c Merge pull request #98 from generic-github-user/list-printing
| | |\ \ \ \ \  
| | | * | | | | 3bb0357 fix types and add llist_print function
| | | * | | | | c4acc00 add llist_map function
| * | | | | | | 3c640c5 generate code statistics and include in README
| |/ / / / / /  
| | | * | | | f1366bf store timeinfo for session structs
| | | * | | |   dea8ca1 Merge branch 'session' of github.com:generic-github-user/CA2 into session
| | | |\ \ \ \  
| | | | * \ \ \   3e37b78 Merge pull request #103 from generic-github-user/time
| | | | |\ \ \ \  
| | | | | * | | | 8852e0a track creation and modification times for states and simulations
| | | | | * | | | 99817a1 add include guard
| | | | | * | | | fe5993d add timeinfo.c
| | | | | * | | | 59a4b7d add struct for storing information about object creation and modification times
| | | * | | | | | 9108656 add some comments
| | | |/ / / / /  
| | | * | | | | ef14a63 create global session object to store selection and other information
| | | | | * | |   e24188a Merge pull request #104 from generic-github-user/long-args
| | | | | |\ \ \  
| | | | | | * \ \   42cd04a Merge pull request #101 from generic-github-user/progress-bar
| | | | | | |\ \ \  
| | | | | | | | * | cf7af38 add percent completion indicator
| | | | | | | | * | 81399b7 add support for continuous re-rendering of progress bars
| | | | | | | | * | 9584a53 fix some bugs with progress bars
| | | | | | | | * | a5f06fa add unicode option for progress bars
| | | | | | | | * | 3854cd6 fix some name conflicts and scoping issues
| | | | | | | |/ /  
| | | | | | | * |   8abb462 Merge branch 'long-args' into progress-bar
| | | | | | | |\ \  
| | | | | | | |/ /  
| | | | | | |/| |   
| | | | | | * | | 7bc5981 parse long-form command options
| | | | | |/ / /  
| | | | | * | | a04a531 fix more segfaults, print sets of states
| | | | | * | | 7882b7f improve state output and fix segmentation faults
| | | | | * | | ab3529d update print_state function and send generated state to stdout
| | | | | * | | cc225af add logging verbosity setting
| | | | | * | | b8f2bb2 add some more comments
| | | | | * | | 47d0b77 add h (help) flag
| | | | | * | | c38c79f refactor example commands
| | | | | * | | be5066a add flag for running CA2 command
| | | | | * | | d9782eb move (some) todos
| | | | | * | | f04dd1f use getopt to parse command-line arguments
| | | | | * | | 434bb2c fix name generation code and run make
| | | | | * | | a9e3d48 minor bug fixes
| | | | | * | | 4474a52 add osme more comments
| | | | | * | | 8a94b67 store state names as struct field
| | | | | * | | 459f375 add function for generating state/pattern names (i.e., ASCII encodings)
| | | |_|/ / /  
| | |/| | | |   
| | | | | * | a06ac7d refactor simulation code using progress bar type
| | | | | * | e4d1c59 add generic progress bar construct
| | |_|_|/ /  
| |/| | | |   
| * | | | | 05454ba generate markdown table of contents for README
| * | | | | aacd1cf add more comments (misc)
| |/ / / /  
| * | / / dd3da91 add comments to simulation.h
| | |/ /  
| |/| |   
| * | | 7cfa70b add listview struct
| * | | 02f46c3 add comments to list.h
| |/ /  
| * | b1694d9 merge cleanup
| * |   64ab0e5 Merge pull request #84 from generic-github-user/compute-tracking
| |\ \  
| | * \   263f902 Merge branch 'master' of github.com:generic-github-user/CA2 into compute-tracking
| | |\ \  
| | |/ /  
| |/| |   
| * | | 589df3e remove extraneous code and comments
| | * | c921513 track compute usage by list functions
| | * | 5db1bdb add graph struct compute tracking
| | * |   1c9b4e9 Merge pull request #83 from generic-github-user/free-objects
| | |\ \  
| | | * \   28a1309 Merge branch 'compute-tracking' of github.com:generic-github-user/CA2 into free-objects
| | | |\ \  
| | | |/ /  
| | |/| |   
| | * | | 45aa070 add update_array function for recomputing array size in memory
| | * | | 837da5f fix simulation size tracking
| | * | | 177138b store state size
| | | * |   e497c97 Merge branch 'list' into free-objects
| | | |\ \  
| | | | * | 9f2dcfa add some comments
| | | * | | cd919cf Merge pull request #82 from generic-github-user/list
| | | |\| | 
| | | | * |   51f741a Merge branch 'free-objects' into list
| | | | |\ \  
| | | | |/ /  
| | | |/| |   
| | | * | |   cdbfccd Merge pull request #79 from generic-github-user/graph-wrapper
| | | |\ \ \  
| | | | * \ \   63cf044 Merge branch 'free-objects' into graph-wrapper
| | | | |\ \ \  
| | | | |/ / /  
| | | |/| | |   
| | | * | | | 754815d add free_manifold
| | | | * | | f968e7a add function for generating subgraphs based on distance from a given node
| | | | * | | 3c853d7 store edges in graph struct
| | | | * | | 2a053b3 add comments to graph.h
| | | | * | | 4092685 add some comments
| | | | * | | 34fed20 add new_graph function (constructor) and update graph structs on node initialization
| | | |/ / /  
| | | * | | 36f134f add free_array function
| | | * | | efee335 add free_state function
| | | * | | 7c9c47c Add function for freeing memory used for storing a simulation
| | |/ / /  
| | | * | 456c0bf add list.h
| | | * | 3fd6d92 add llist_remove function
| | | * | 80b7a22 store stack of available indices to store data in
| | | * | d53027a add free_llist function
| | | * | a13b3fd add function for adding elements to dynamic lists
| | | * | e91c22f add list struct
| | | * | 20c22cb add test struct
| | | * | 555003e add reduce command example
| | | * | 505015a misc. updates to make sure things don't break
| | | * | 95d39bf add (limited) reduce command for combining a set of data along an axis/property
| | | * | d502404 add function for states extending binary array addition
| | | * | cd83b56 add revised array summary generator function
| | | * | d3f1f04 rewrite simulation code to store an array of state pointers
| | | * | dc92609 add generic reduce function
| | |/ /  
| |/| |   
| * | | 62ff192 misc README changes
| |/ /  
| * | 9d183cf fix selection pointer issues
| * | 6515b20 segment states in CGOL-like rules
| * | b47888e support other format string codes
| * | 4fa6b15 make hashing structures and functions generic
| * | 04c57b2 add missing include statements
| * | f24e39c more misc. updates and adjustments
| * | 777cb9f miscellaneous
| * | c0407f7 fix logging/printing indentation
| * | 212dd02 add function for generating type name strings
| * | 1397a03 add type struct
| * | 98c7b17 misc README updates
| * | 1f7f1a0 highlight string values
| * | edfa90c add plotting code for array objects
| * | f9c1f06 add command for getting property from a collection of objects
| * | c2907e7 parse headers describing raw array data
| * | 645536d misc
| * | 636dbd9 add state_info function
| * | 90a87dd improve logging code in command processor
| * | 1259318 add information about templates with parameters
| * | 65bd06b support use of format strings in printx
| * | 614ca14 add assert function
| * | 26fa299 fix dependencies
| * | f57a138 add array axis labels
| * | 2638d6d add general information about project structure
| * | 45dc547 add plotting command examples
| * | 5d45ca3 add more commands
| * | 4e3ae14 add more info about installation process
| * | 76a12e8 fix other include paths
| * | 4bfb6aa add more information about build process to generated files
| * | 82d9cb5 add rest of C source files
| * | 2bafeb1 add information about global command options
| * | 1e44c5e move PTR_REDUCE macro
| * | e42dd87 extract EXTRACT macro
| * | a106b4b move ARRAY_OP macro
| * | f81a848 miscellaneous (mainly updating makefile to use new directory structure)
| * | 17ff503 add more command info
| * | 6631bd7 move some commands to dedicated template files
| * | 748a956 fix relative paths in include statements
| * | 59106d8 add other source files
| * | 57baaa0 add logging to build script
| * | 1e863ec add build timestamps
| * | 501f662 Search for templates within subdirectories
| * | 5bb7ef9 update .gitignore
| * | 498d54e move each set of scripts to its own subdirectory
| * | 5e20ae7 add randomstate command template
| * | dbca2f7 add array_reduce template and generate corresponding function body
| * | 7b28117 add PNG generation script from https://www.nayuki.io/page/tiny-png-output
| * | df1f2d1 add support for templates with arguments
| * | 1e7e4fc Add some source files (.c0)
| * | 3828ecb fix issues with build script
| * | 38f0ebb add build script for generating processed C files from templates
| * | b65b788 rework command processor to store all selections in a single variable
| * | 0fa3add use pointers in simulation functions
| * | 37da57b refactor state functions to return pointers
| * | d6d016f add plotting command
| * | 4289b6f Add function for storing arrays in memory
| * | b6f5f60 adjust plot styling
| * | d3cd40d add simple plotting script for data serialized from program
| * | 280d510 miscellaneous
| * | b343a6d move image generation functions
| * | 6ff574e move command processing functions
| * | b76640c move fill_slice
| * | 1dfdb4b extract main include statements
| * | 1350cef move output helper functions
| * | 19779bb move other simulation functions
| * | 4eed1c2 move rule structs to header file
| * | 2a46984 move other array functions
| * | 59bbf4b clean up ca.c
| * | 0daefbc move rule data structure code and functions to new file
| * | f2041db add more examples to README
| * | a0d2b30 Store indices of array elements (for sparse arrays)
| * | 4d7f778 fix issues with graph node maintenance (mainly allocating memory for in/out node lists)
| * | 0bf2d78 Add functions for working with linked lists
| * | 564d9ad add basic graph types and functions
| * | be54c72 only display progress bar if not displaying simulation in stdout
| * | e852495 add command for printing summary table of simulation
| * | fd32c1e add some comments
| * | fa1ec66 add neighborhood struct constructor
| * | 8befc3d refactor using state constructor function (and fix simulation segmentation fault)
| * | d4cef4a Add quit command
| * | 82b6328 update makefile
| * | 7feba1d misc
| * | b9ea0f7 add helpers module
| * | 67863b1 move hash table structures and functions to new files
| * | 0690080 misc reorganization
| * | e3596fb move state struct and functions
| * | 284ed4c move other array functions
| * | 08a1508 add include guards
| * | e19d32d update makefile
| * | e34b09c move array and vector code
| * | cf1d6c7 Improve space and compute tracking
| * | d9b9311 misc
| * | 50ee2b2 Add function for generating subpatterns from a state
| * | 40a4681 add random manifold generator
| * | 7e70c34 Add examples section
| * | a036bca use correct state size/remove placeholders
| * | 4442901 Add functions for interacting with hash tables
| * | 7cc8b30 Add hash table struct and constructor function
| * | 147ca78 Add hashing functions
| * | faeef56 add (unfinished) array slicing function
| * | 7e33082 misc
| * | cf3fb20 add state constructor
| * | 86ed3a6 move color data conversion functions to new file
| * | dfe1338 store age of each cell in simulation struct
| * | b7da814 miscellaneous
| * | 3f03adf adjust vector struct, usage of pointers, etc.
| * | 30dee0b fix get_coord and add vec_to_array function
| * | 64dc5a5 add colored output/visualization
| * | a9d853c allow printing with unicode block characters
| * | 319c9e8 Add color conversion functions
| * | 0409100 clean up extraneous code
| * | 2743074 add abbreviated versions of other structs (thank god for vim macros)
| * | e70618b use typedef to clean up notation for some structs
| * | 74c05d3 add command for generating images from states
| * | 5a5a793 add function for filling in slice of array
| * | b7b406e add makefile
| * | 1d034b8 update README
| * | 1cfab31 misc
| * | 2e16c95 add array summarization function
| * | 86ba82c Add print command
| * | 561bc35 add array min and max functions
| * | 725009d Add (unfinished) functions for displaying information about simulations
| * | 7da1536 reorganization
| * | af51d95 Add function for getting property from a collection of states
| * | 43acb1b Add structs for representing geometry and automata rules
| * | 8c343a7 misc
| * | b5092bd Add function for generating inline plots of simulations
| * | a7d6283 add function for testing state equality
| * | 2c278a1 Add information about new commands
| * | 8e4678f Add command for enumerating possible cellular automata states
| * | 53e1999 Add function for cloning states
| * | 719eb68 Add min and max commands
| * | acfe348 Store summary information about states in structs
| * | f7faf14 Add functions for finding state in a set of states with the largest/smallest value for a given property
| * | 54cc27e improve logging
| * | c8825ca define binary operations on arrays
| * | 3ed7778 Restructure some functions to use pointers instead of struct values
| * | acc6ebe Include summary information about state in output file
| * | 11f0434 Add function for counting neighbors of each cell
| * | 170673f Add command flag for printing simulation to stdout
| * | e2edcac misc adjustments
| * | 259375b fix indentation and other issues
| * | 25226ed add collapse command for reducing a simulation to its final state
| * | b25db92 write to persistent log file
| * | 4ff5b09 more refactoring
| * | 395eab5 minor refactoring
| * | f36af65 clean up code
| * | ea5c041 Track compute used for each simulation instance
| * | 676fdfe Allow writing collections of states to files
| * | 4e3a004 Handle optional command arguments
| * | c9db92f add .gitignore
| * | cab7a48 allow simulation on a collection of states
| * | dd03ae7 add indentation to improve readability
| * | 8bf8e41 Add README introduction
| * | b7443aa Support creating collections of states
| * | 7c68337 Add progress bar
| * | 45ac33a Move state printing function
| * | 2447e66 Add simulate command
| * | 69499ec Refactor simulation code
| * | 758c04d Add simulation helper functions
| * | 2980bc6 misc
| * | 93be2bb refactoring
| * | 8bb91d2 cleanup
| * | fd5a602 Add comments
| * | bb599cb Use state wrapper struct
| * | 0ff1106 Move neighbor-counting code
| * | 1f63735 Add information about command argument types
| * | e56e404 Add command list
| * | 9cadc5b Add README
| * | 8c164d3 Miscellaneous
| * | 56a1f0b Add basic interactive command handling
| * | 18d59f5 Add function for generating string from CA state
| * | 27a8a40 Factor out random state generation
| * | 42494ca Implement reduce function for arrays
| * | d1496de Refactor with array_get and array_set functions
| * | 16fafe8 Track number of operations performed during simulation
| * | b4856d0 Add some comments
| * | 904cf8c Add placeholder structs
| * | b885f49 add some sample commands (not yet implemented)
| * | 6dbe3b8 Add array handling code
| * | efe3228 add vector struct code
| * | f5e7f14 Add simple logging
| * | 2fa643a Add base cellular automata code
|  /  
* |   19a8fbf (origin/repo-import, repo-import) Merge branch 'attractors'
|\ \  
| * | 3d84b25 (origin/attractors, attractors) move /attractors to avoid horrid merge conflict with master
| * | 2de24e5 split source into smaller modules
| * | 51ec827 clean up code slightly and reflow docstrings
| * | 937d5d4 add alternate version of source with IPython markers stripped out
* | |   5ee1074 Merge branch 'meta'
|\ \ \  
| * \ \   d230ab4 Merge branch 'metadata' into meta
| |\ \ \  
| * | | | 9f2f770 add simple logging to build script
| | | | | * d2d8a9d (origin/metadata, metadata) label remaining projects
| | | | | * 30d4b02 add labels to more projects
| | | |_|/  
| | |/| |   
| | * | | 543b65e list languages for newly added projects
| | * | | 12e734d add labels to some recently merged projects
| | * | | c440a60 reflow label descriptions
| |/ / /  
| * | | fd5fc44 add newly merged projects
| * | | ead61a5 add some whitespace (to save my eyes)
| | | | * 7cd1a74 (origin/py-style, py-style) update build script to comply with style guide
| | | | * 68449db generate list of Python style issues
| |_|_|/  
|/| | |   
* | | | bc39063 group math-related projects
* | | | 473374c more reorganization
* | | | f1e8e9d install flake8 for Python code style checking
* | | | 9b89c9a make pipenv global
* | | |   44c8305 Merge branch 'symbolic-approximation'
|\ \ \ \  
| * \ \ \   4b1cddd (origin/symbolic-approximation, symbolic-approximation) Add 'symbolic-approximation/' from commit '0f13e032a9e67289d08f9c9d1ae3d44df7c67c8b'
| |\ \ \ \  
| | * | | | 0f13e03 Update requirements.txt
| | * | | | 9c7e043 Add project overview
| | * | | | c074561 reformat function signature
| | * | | | 001d1ed Other misc. testing
| | * | | | e7bff9c Visualizing/plotting unary functions
| | * | | | 6ec5fb9 Add function for evaluating an expression tree given 1 or more inputs
| | * | | | e2796ed Add some interesting functions discovered during testing
| | * | | | b3df58e Testing plot_symbolic function
| | * | | | e337174 Add function for applying a 2-parameter function over a coordinate plane for visualization
| | * | | | a131df5 Testing equation (and corresponding LaTeX) generation
| | * | | | b2da12c Support LaTeX generation for unary operations
| | * | | | 34e9966 Add function for converting math symbol/expression tree to LaTeX markup
| | * | | | 15d8610 (Optionally) limit which substitutions are allowed in later recursive calls
| | * | | | 3963d12 Add function for generating mathematical expressions based on grammar
| | * | | | 57c73c3 Reformat expressions list
| | * | | | 72e9611 Add symbols/rewriting rules for polynomial generation test
| | * | | | 61e5a45 Add values (integers, variables, nested functions, etc.)
| | * | | | cb547e4 Add function for evaluating math functions without throwing exceptions
| | * | | | 1db6163 Add trigonometric functions
| | * | | | fe8886a Add functions and LaTeX markup corresponding to mathematical operators
| | * | | | d6dd8ae Add unary operations
| | * | | | df288d0 Add (some) binary operators
| | * | | | 914c529 Add base grammars for simple mathematical expressions
| | * | | | 708dfa4 Create requirements.txt
| | * | | | 8191407 Add imports
| | * | | | 6c229a2 Create symbolic-approximation.py
| | * | | | 4b277fc Initial commit
| |  / / /  
* | | | |   72bb24d Merge branch 'random-walks'
|\ \ \ \ \  
| * \ \ \ \   cece20a (origin/random-walks, random-walks) Add 'combinatorics/random-walks/' from commit '2161e80fa68cc45e7fdffb19563234f3f3ddf638'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | 2161e80 Create requirements.txt
| | * | | |   46c6fd6 Merge branch 'master' of https://github.com/generic-github-user/random-walks
| | |\ \ \ \  
| | | * | | | 0be0d78 Create LICENSE
| | * | | | | 4df404b Update .gitignore
| | |/ / / /  
| | * | | | 9316953 Add generated config files
| | * | | | 0d88531 Add nbdev config files
| | * | | | a58459b Create settings.ini
| | * | | | e72b073 Create .gitignore
| |  / / /  
* | | | | 6fcb3a6 more directory reorganization
* | | | | 7315e96 move programming languages to their own directory
* | | | | 6ed43ee rebuild
* | | | |   528ae77 Merge branch 'decision-tree-experiments'
|\ \ \ \ \  
| * \ \ \ \   e27d633 (origin/decision-tree-experiments, decision-tree-experiments) Add 'decision-tree-experiments/' from commit 'de82ab7095144d67bfa763a637e5f976ece23354'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | de82ab7 use new dimension argument format
| | * | | | 5444e17 add testing code for game board of n dimensions
| | * | | | e1e949a fix old xyz handling
| | * | | | e7aedd8 fix checkArray()
| | * | | | 7ebea5b add spacing option and fix accidental type() overwrite
| | * | | | 440d906 update grid handling in board display function
| | * | | | 854e432 refactor checkArray() recursively
| | * | | | 3766cf7 add function to play out random game (mostly for testing visual componenets)
| | * | | | 4d72d51 update board checking function
| | * | | | c5b9ca6 update board printing function
| | * | | | cab36d8 testing for new dimension handling
| | * | | | 0bd12dc method for interspersing array (from https://stackoverflow.com/a/5921708)
| | * | | | dc1a7b1 update move() function
| | * | | | bf2ab5a fix default player list argument
| | * | | | e0da3e1 update legal() method to work with new dimension handling
| | * | | | 15b3af2 add default players + players argument in constructor
| | * | | | a37888d adding support for arbitrary board dimensions
| | * | | | 88cda04 add docstrings
| | * | | | a7bdf75 rename some variables
| | * | | | 901828a add argument for infinite max/min
| | * | | | 4ad929d add infinite max/min values as implemented in https://www3.ntu.edu.sg/home/ehchua/programming/java/javagame_tictactoe_ai.html
| | * | | | b67eeb2 more minor adjustments and tests
| | * | | | 2feab6b misc
| | * | | | c13aabf add method to get best subnode based on whether turn of node's board state is player or opponent
| | * | | | 70137ac fix bug in max/min subnode functions
| | * | | | 4def796 fix center move function
| | * | | | d330d74 implement minimax algorithm
| | * | | | daf9a93 move DecisionTree class
| | * | | | ba8597b Create README.md
| | * | | | aeb18b2 add method to find the nearest explored game state in the decision tree
| | * | | | b466c6c slightly refactor legal move checking
| | * | | | 7f6fa8b move node class to new file
| | * | | | ef9ca44 move RowGame class to new file
| | * | | | 5ba2730 ignore pyc files
| | * | | | 1ace03c add "start" argument to initialize decision tree with a given state (root node)
| | * | | | c9af82d add magic method to get the difference between two boards
| | * | | | 78ae2d3 misc
| | * | | | 1f41d43 add RowGame.center()
| | * | | | 7e04ce3 add argument to specify start turn
| | * | | | c73d741 add methods to get list of all subnodes from tree or node
| | * | | | c104006 miscellaneous
| | * | | | abcd89e add top-down tree backpropagation
| | * | | | 02afd40 add tree printing for decision trees
| | * | | | c1b7156 add decision tree backpropagator
| | * | | | 5823f95 add node backpropagator
| | * | | | ec4957c add option to print grid between cells in board
| | * | | | 921f6ad more tests
| | * | | | 7c2341c fix bug that caused board checking function to always return 0 (instead of the actual winner)
| | * | | | 8b860ea fix diagonal transposition
| | * | | | b626354 return result after making random move
| | * | | | ef9da66 add stringification method
| | * | | | d12b3a2 add method to get terminating nodes
| | * | | | 5acfb8f terminate branch (don't generate further game states) if a player wins
| | * | | | 70b69d6 add simple game tree generation functionality to DecisionTree class
| | * | | | f6c6c52 add method for counting all subnodes of node
| | * | | | 3e03dd4 fix a couple bugs relating to empty board space checking
| | * | | | e8c91fc add function to recursively generate subnodes in decision tree (future possible game states)
| | * | | | 31057cc add node class (for decision tree generation)
| | * | | | 79f984d comments
| | * | | | a7b51e3 testing code
| | * | | | 45e147b add method to play a random move (out of all the free spaces on the board)
| | * | | | 059e860 add method to make next move given coordinates
| | * | | | b70c9d9 add a method to check if a specified move is legal (in board and no move was already made there)
| | * | | | 20f3ca2 track current turn and add method to move to next turn
| | * | | | 08f294d add comments
| | * | | | 3e7734b improve board rendering
| | * | | | 1a540e8 add diagonal win checks
| | * | | | c3b8279 add simple display method
| | * | | | 56cdf89 add method to check for wins in rows/columns of a game board
| | * | | | 1edcb09 add player class (might not be used)
| | * | | | f3dae20 fix module name
| | * | | | 0a7ab3b add clone method
| | * | | | 8330ec2 init and add RowGame class
| |  / / /  
* | | | |   edc9864 Merge branch 'icon-encoder'
|\ \ \ \ \  
| * \ \ \ \   6a2d4c0 (origin/icon-encoder, icon-encoder) Add 'icon-encoder/' from commit '010a3b2ec9fabc58d2ce4e8756eb8a3e6a6c1d15'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | 010a3b2 Add more testing screenshots
| | * | | | 158b61e 100 random generated images
| | * | | | 0c25b80 Single generated sample visualization
| | * | | | c2b9ce5 Comment out outdated image generation code
| | * | | | 9c4e302 Add KL-Divergence loss
| | * | | | b831e2b Use weighted average of training sample latent distributions to generate paramters for generated image
| | * | | | e0cb0d8 Random generated image
| | * | | | ad8de1c Add function for generating random tensor between two provided tensors
| | * | | | 2c227c1 Remove unused code
| | * | | | 9139faf Use TensorFlow dataset system for processing training data
| | * | | | 29c0293 Move loss calculation function definition out of training loop
| | * | | | f76eba9 Use optimizer.minimize instead of model.fit for training combined autoencoder model
| | * | | | e634823 Separate encoder and decoder into two models
| | * | | | b39c2ff More comments
| | * | | | 13709ea Add plot of 100 reconstructed favicon images
| | * | | | 47058b6 Add some testing screenshots
| | * | | | b03be6c Add library/module information
| | * | | | b3e4ce8 Add links to TensorFlow
| | * | | | 4165226 Add shallowness control variable
| | * | | | 5cd111f Add some comments
| | * | | | 0b5de57 Add information about project to README
| | * | | | d77f832 Add more print statements
| | * | | | 008cebe Ignore logs used for TensorBoard
| | * | | | 6907003 Clip output tensor values before rendering to avoid Matplotlib clamp warnings
| | * | | | cf09b53 Catch errors thrown during image loading
| | * | | | c14f174 Add num_layers variable for organization
| | * | | | c622dd0 Add some print statements
| | * | | | 1e58ba3 Fix layer generation math and add layer ratio control
| | * | | | 71ed8b9 TensorBoard stuff
| | * | | | 6e25c18 Add automatic layer generation
| | * | | | 17d1204 Revert conv layers
| | * | | | 895d2a0 Add convolutions in compressor network (bottleneck)
| | * | | | a6b346d Add more settings
| | * | | | a31b12c Settings
| | * | | | 63f498a Add more layers
| | * | | | afb368a Wait for user input to close window
| | * | | | 855007d Animate plot with updated image reconstruction as the model is trained
| | * | | | 5d7c305 Execute rendering function on a callback after each training epoch
| | * | | | 823482d Don't use sigmoid on the output layer
| | * | | | cddc066 Add resolution settings
| | * | | | 648c702 Add model compiling and training
| | * | | | e280e8b Convert image data to tensor
| | * | | | 83b71e6 Use eager execution
| | * | | | b7da195 Fix image resizing
| | * | | | 0e6ca90 Update image data format to work with TensorFlow
| | * | | | f74209d Add basic TensorFlow autoencoder model
| | * | | | 22e46ab Loading images from data folder
| | * | | | 257444e Hide icon data
| | * | | | 6a4e895 Initial commit
| |  / / /  
* | | | |   47dad1c Merge branch 'micronotes'
|\ \ \ \ \  
| * \ \ \ \   f50a5fe (origin/micronotes, micronotes) Add 'micronotes/' from commit 'ad86c8d09d7daf3b22ed0ba2368ae81926edf8cf'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | ad86c8d Added demo screenshots to README
| | * | | | 85bbbf7 Added micronotes introduction to README
| | * | | | d93101f Added comments to code
| | * | | | 65b4100 Two small changes
| | * | | | 1269be5 Moved Issues and Alternatives sections in README
| | * | | | 163e72a Reorganized some README headers
| | * | | | 0655404 Added information about footnote styling to README.md
| | * | | | 19c0ae9 Removed verbose transition/styling information
| | * | | | f9a3762 Added link to README in demo file
| | * | | | b5dd885 Added installation instructions section to README.md
| | * | | | f75e2a5 Added instructions for adding footnotes using micronotes to README.md
| | * | | | 0e5553b Added Alternatives section to README.md
| | * | | | 636ac4f Update LICENSE
| | * | | | 62960cf Added requirements information
| | * | | | d53f278 Added Issues section to README
| | * | | | f875ddb Added smooth scrolling for footnote links
| | * | | | 30fc8ca Moved one link into a footnote
| | * | | | 55d65db Split demo HTML into many lines
| | * | | | 40fc2bb Added example of link inside footnote
| | * | | | bb0773c Added links to script download and hosted version
| | * | | | 9a31cdc Removed outdated max-width and max-height properties
| | * | | | 940b1bb Added custom HTML and CSS examples to demo
| | * | | | 838944c Added example of long footnote
| | * | | | 4e15bd8 Nested footnotes are now displayed correctly in the footnote listing section
| | * | | | d106468 Fixed visibility issue
| | * | | | 8ceabd1 Added more examples to demo
| | * | | | 495c54b Added more styling to demo
| | * | | | a7a5212 Footnotes at bottom of page are now displayed inline with footnote content
| | * | | | 0928630 Added more styling to demo
| | * | | | 407793c Added link styling
| | * | | | 7c7d24e Added styling to note boxes
| | * | | | 8153c66 Whoops
| | * | | | a3b224f Added list of footnotes
| | * | | | 804d93d Note boxes will no longer appear when hovered over
| | * | | | e8af862 Added more examples
| | * | | | c5b464b Added example snippet to HTML
| | * | | | e827dfe Notes no longer disappear when hovered over
| | * | | | d24d3e9 Numbers and notes have corresponding IDs
| | * | | | 2ec28c2 Added reference to script (micronotes.js) in HTML
| | * | | | fbe0df4 Added note_index
| | * | | | 804effb Added shortcode replacement
| | * | | | 96f26ed Updated replace function
| | * | | | d4c0984 Added box-sizing: border-box;
| | * | | | e4a2325 Added stylesheet information to head
| | * | | | b0a3452 Add string replacement function
| | * | | | 032c8f1 Added HTML boilerplate code
| | * | | | 205bad4 Added main files
| | * | | | d91db7b Initial commit
| |  / / /  
* | | | |   a469ea6 Merge branch 'music-generation-experiments'
|\ \ \ \ \  
| * \ \ \ \   a3fe0ee (origin/music-generation-experiments, music-generation-experiments) Add 'music-generation-experiments/' from commit '5076d205423990d3f401bcdda15cc1665fdf467c'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | 5076d20 Update .gitignore
| | * | | | 13e2f78 add interlay method
| | * | | | a35dad9 add merge() method
| | * | | | 59a3ae6 add clear() method
| | * | | | 29e05a3 allow recursive melody reversal
| | * | | | eba419a add comments
| | * | | | 71f4b2d add docstrings
| | * | | | d9c7b7f add comments
| | * | | | c3b1288 add dirs parameter
| | * | | | daaf0c2 raise errors
| | * | | | 1127dea refactor
| | * | | | a95764b update variable names
| | * | | | dd0d858 if tuples are given as arguments, randomly choose from range between provided values
| | * | | | 8e7d8f1 provide more random arguments to Scale constructor
| | * | | | 77e1cee add default argument dictionary
| | * | | | 17a89c5 refactoring
| | * | | | df71f60 update code to use inherited methods instead of creating another class instance
| | * | | | 2ae99b4 add target length option for composition generator
| | * | | | 887e2d2 add method for getting length of melody in seconds
| | * | | | 1689427 cleanup
| | * | | | 5f3da53 move scale class to its own file
| | * | | | c451bee add more options to generate() method
| | * | | | 12966ea pass tempo and velocity to melody randomizer
| | * | | | 7d2e01b misc
| | * | | | d68f773 add scale skip parameter
| | * | | | 0d2863e add repetition of some sections in composition generator
| | * | | | 84a128f add randomized scales
| | * | | | 1ca23f6 add sequential melody generation (alternative to recursive/nested model)
| | * | | | 4bb5101 add velocity randomization
| | * | | | 1921862 small fixes & cleanup
| | * | | | 55cd6da randomize each melody's tempo
| | * | | | 5e8be24 add option to randomly pitch shift some sections of the composition
| | * | | | 47219fe randomly reverse some sections
| | * | | | 3c61598 randomly generate chords
| | * | | | 1eea646 cleanup
| | * | | | b8d6f83 store lists of generated melodies and randomly decide whether to reuse or create new ones
| | * | | | b39dd55 fix missing variable name
| | * | | | a8bc13c refactoring
| | * | | | 50c634e add slight random variation in length of notes/chords to emulate human playing
| | * | | | 339453f add chord tempo calculation
| | * | | | 3f9de57 add melody reversal method
| | * | | | 15f4474 expand demo with different types of chord constructors
| | * | | | ef92f8a minor refactoring
| | * | | | dc40037 add flexible chord construction (via Python-style interval or custom indices)
| | * | | | 8f2156e allow note constructor to accept str or int argument (passed to Pitch constructor)
| | * | | | fa16a0f refactor demo code
| | * | | | 131db41 add string support for Chord constructor (this is passed to the Note constructor, then Pitch)
| | * | | | 31b544d add print_tree method
| | * | | | 2de4597 miscellaneous
| | * | | | ebaf3aa add demo function
| | * | | | ddcf570 add docstrings
| | * | | | ce2ef66 misc.
| | * | | | 025a41d add() convenience method
| | * | | | cad0a21 fix bug by which changing one melody would change the rest
| | * | | | a425b50 add generate function wrapper
| | * | | | f659fcc add recursive music generation function
| | * | | | e1b7188 add offset between melody repetitions
| | * | | | b30f1b2 testing new features
| | * | | | a49010b add clone function to Melody class
| | * | | | a86df66 add melody key signature
| | * | | | 2878f2a add step/shift method to change all notes in melody
| | * | | | bb0ccfe fix note length calculation
| | * | | | 388a2f9 fix chord scales
| | * | | | 8ff7b5d add play() method
| | * | | | 4c41e87 create Chord class
| | * | | | 7a24356 allow key signature as argument to note initialization function
| | * | | | c0a9e46 add step helper method
| | * | | | 28a666c add quantization of randomized note lengths
| | * | | |   2588c00 Merge branch 'master' of https://github.com/generic-github-user/music-generation-experiments
| | |\ \ \ \  
| | | * | | | cd8d891 Create README.md
| | * | | | | 79ed36d add note clipping option (to prevent overlap for instruments that reverberate longer)
| | * | | | | be2230e add instrument parameter
| | * | | | | e2eed64 add stop method
| | |/ / / /  
| | * | | | 5b74411 add repeat_melody method
| | * | | | 8358eaf add nesting of melodies (i.e., melody > melodies > notes)
| | * | | | 6922b8d move Composition class
| | * | | | fa757e5 move Melody class
| | * | | | eccf70a extract Note class
| | * | | | de37f89 ignore .pyc files
| | * | | | d5c40f4 move pitch class to independent file
| | * | | | 554ca2a add note length randomization
| | * | | | 528ff85 add code for testing melodies
| | * | | | 0bcdd19 create helper methods in Composition class
| | * | | | 86045bc create melody class
| | * | | | d4eaa57 add option to provide player to note in play() method
| | * | | | 25b6692 add comments to Note class
| | * | | | 2ca1b16 update scale generation function
| | * | | | 89d50d5 update play_note() to use new classes
| | * | | | d7d41b1 miscellaneous
| | * | | | 92e6dd7 add printout function to Note class
| | * | | | 54c0d08 add function to apply key signature to note ("B_E_" would transform B to B flat and E to E flat)
| | * | | | 674ad63 add method to play instance of note class
| | * | | | 5250ac5 add method to get length in seconds of a note
| | * | | | 69f04c3 create Note class
| | * | | | 29ba0ca add function to print pitch information
| | * | | | 0298c82 add method for getting name of numeric pitch
| | * | | | 5c90e66 add method for stepping pitch up or down
| | * | | | 4cdfb81 add handling for numeric pitches
| | * | | | b49df32 create Pitch class
| | * | | | 9f55f43 add universal natural list
| | * | | | d12d0f8 add universal note list
| | * | | | eeabb34 add method to get base note from pitch
| | * | | | b60b105 miscellaneous
| | * | | | e780b19 add function to get note name from pitch value
| | * | | | 312a48a add play_note()
| | * | | | 7d5acae add key signature
| | * | | | 4ce1e56 add method for direct pitch adjustment
| | * | | | b36ecb5 create Composition class
| | * | | | 809342a add note length option to scale()
| | * | | | 4e1d2e3 add velocity option to scale()
| | * | | | 709ca16 add option for scales of chords
| | * | | | d629133 add simple chord function
| | * | | | e4f37c4 add support for note lookup by string (ex. "C.3"; C in octave 3)
| | * | | | 2e66bda add note to number conversion (refer to https://computermusicresource.com/midikeys.html)
| | * | | | c2cfca8 make scale function
| | * | | | 00f8a50 ignore audio files/note samples
| | * | | | b31df02 working pygame test
| | * | | | 63cee72 tests with other libraries/modules
| | * | | | 6fc5548 testing pygame sound module
| | * | | | e398c6f testing with prerecorded notes
| | * | | | fa02294 initial testing
| |  / / /  
* | | | |   56fcacf Merge branch 'grammars'
|\ \ \ \ \  
| * \ \ \ \   b4d62c9 (origin/grammars, grammars) Add 'grammars/' from commit 'e7c0dafc022ced163dc4fc106ba012b087d6ef75'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | e7c0daf add Set type
| | * | | | 0d0b402 add Rule type, etc.
| | * | | | 7316d49 add String struct and associated functions
| | * | | | 4042db6 add Cargo info files
| | * | | | 0caff94 add type summary to README
| | * | | | 6b4aee9 add generic Symbol struct and relevant implementations
| | * | | | f89bfd1 add README
| |  / / /  
* | | | | 260f322 rebuild
* | | | |   99e04fa Merge branch 'cogbench'
|\ \ \ \ \  
| * \ \ \ \   4ecddf0 (origin/cogbench, cogbench) Add 'cogbench/' from commit 'bc24a4b4c1c4654d7df83f15f484325ed4631838'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | bc24a4b Add methods for min/max test
| | * | | | 7f0d4ee Add min/max finding test
| | * | | | 8fdc343 Include computed test scores in scatter plot
| | * | | | dc02f31 Calculate summary scores for keyboard alternation test
| | * | | | 9519565 Add command for generating plots from test data
| | * | | | e11bb2a miscellaneous
| | * | | | f3335f5 Add test upgrading method
| | * | | | 843e687 Add method for executing key alternation test
| | * | | | 3081e49 Add key alternation test class
| | * | | | 524278a Add function for getting commands/inputs from the user and storing data
| | * | | | 98b70b0 Add error message if invalid test name/substring is entered
| | * | | | edf97b0 Add quit command (for ending sessions)
| | * | | | 2f6b1e2 Add function for handling command strings
| | * | | | fd38a20 Add upgrade method for setting/generating missing properties of deserialized objects
| | * | | | d3a384e Add Database class
| | * | | | 3ef4260 Add enhanced String class (borrwed from shelf codebase)
| | * | | | 02d7ec0 Add database pickling/serialization functions (borrowed from shelf repo)
| | * | | | 2e49664 Add list of test classes and name strings
| | * | | | 5930060 Add Session class
| | * | | | aab98d1 Add local/utility script imports
| | * | | | 4bbeb28 utility script imports
| | * | | | 234a131 Add Test base class
| | * | | | f3441aa Add Device class
| | * | | | f781ddf Add module imports
| | * | | | 468ab91 nbdev config files
| | * | | | 329a849 Create settings.ini
| | * | | | ca18fe9 Create .gitignore
| |  / / /  
* | | | |   e9ba0cd Merge branch 'punchcard'
|\ \ \ \ \  
| * \ \ \ \   bec5700 (origin/punchcard, punchcard) Add 'punchcard/' from commit 'cac5504d88e1fe090e33c993aaca485b2b4aef51'
| |\ \ \ \ \  
| | |/ / / /  
| |/| | | |   
| | * | | | cac5504 add sum function
| | * | | | 6ad60d9 miscellaneous
| | * | | | 2aef61d Add method for getting NumPy array from DataObject
| | * | | | 99b2587 Add length method
| | * | | | 4998870 Add index function
| | * | | | e790db4 Add function for converting range(s) into DataObjects
| | * | | | a570dd6 add simple product method
| | * | | | a182233 Add helper magic methods
| | * | | | fa5c489 misc
| | * | | | 76ae4f0 Add convenience method for reversing iterable DataObjects
| | * | | | 17c89f7 Add method for removing specified characters/substrings
| | * | | | 1ba02d1 add search method
| | * | | | 512d4d3 add more headers
| | * | | | 593e786 Add method for applying arbitrary function to DataObject
| | * | | | b0846f9 add range generator (and alias)
| | * | | | e0fd3d0 add slice generator
| | * | | | c10a530 add max function
| | * | | | 064022d add min function
| | * | | | af1ef3f Add split method (mainly for strings)
| | * | | | 3f2c4ca more testing
| | * | | | c2fec00 Add Cartesian product function
| | * | | | a4fdc4f Add copy method
| | * | | | b3c088d add repr function
| | * | | | e01cc1c Add DataObject printing function
| | * | | | 22f4819 Add parametrized decorator factory function
| | * | | | 505e172 Add static function memoization wrapper (not bound to a particular class instance)
| | * | | | f0a51fd Test displaying mathematical expressions with LaTeX typesetting
| | * | | | f32a384 Add generic memoization wrapper function (and decorator to generate a wrapper for a specific method)
| | * | | | ebb2a8a misc. testing
| | * | | | e499df3 Add function for casting a DataObject to a different type
| | * | | | 90cdcf0 Add some comments
| | * | | | 96771c7 todos
| | * | | | 32e28f2 Add list of planned features
| | * | | | 200bd8a Add function for mapping another function over iterable DataObject
| | * | | | 2dcca37 Add function for generating hashes of lists and nested lists
| | * | | | 29df7d9 Add function for generating string representation of DataObject (and, optionally, other properties)
| | * | | | dfed1bf Add function for adding generic functions to the DataObject class
| | * | | | b7e7c54 Generate hash and ID for data stored in class instance
| | * | | | 352823b Infer datatype if none is provided
| | * | | | f9b23e8 Add DataObject class
| | * | | | 67abfec add Cache class
| | * | | | 94fed05 Add other imports
| | * | | | 438b821 Add list of planned optimization (both time and space) features
| | * | | | 9607afc Add base imports
| | * | | | 79e28cd add project introduction
| | * | | | e009b03 Initial commit
| |  / / /  
* | | | |   9418862 (origin/wordtetris, wordtetris) Add 'wordtetris/' from commit 'a0082a46cc686cda5f5d395c82cc2904640f4ac8'
|\ \ \ \ \  
| |/ / / /  
|/| | | |   
| * | | | a0082a4 Skip checking empty rows for matches in word list
| * | | | 5374910 Add more comments
| * | | | 806c527 Add comments to step method
| * | | | 7c40466 Check for words along diagonals
| * | | | 9e6490c Add keypress handling/controls
| * | | | 9a0bacb Add vscode metadata
| * | | | b8f82ce Add main game loop
| * | | | 3c98eef Add Game class stringification method
| * | | | 715f7e6 Add a new block when the current active block has landed
| * | | | 255fad2 Add word detection code
| * | | | e1c5a6a Add code for generating new blocks/letters
| * | | | 3c88174 Add method for updating instance variables for Game class
| * | | | 930692f Add Game class
| * | | | 95df6f4 miscellaneous
| * | | | 318e64c Add other Block class methods
| * | | | 1222f63 Add methods for moving blocks downward
| * | | | 61bfe6c Add method for checking if a block can move down
| * | | | 5d3e172 Add block class
| * | | | ab049a3 Calculate frequencies of individual symbols/characters from word list
| * | | | ca1fa3c Generate word list from nltk corpus/frequency data
| * | | | 8944bba Load text corpus with nltk
| * | | | 82c2e82 Add main script and imports
| * | | | a9c81e5 Initial commit
|  / / /  
| | | | * 6235d69 (origin/pythings, pythings) comply with style guide
| | | | *   ba50b31 Merge branch 'pythings-docgen' into pythings
| | | | |\  
| | | | | * 7ae5e7f (origin/pythings-docgen, pythings-docgen) add option for hiding sections without content
| | | | * |   a2bde6f Merge branch 'pythings-docs' into pythings
| | | | |\ \  
| | | | * | | f3a2e31 (origin/pythings-restructuring, pythings-restructuring) move Animal and File examples
| | | | * | | 0da9689 move some examples to separate files
| | | | * | | cd4c463 move custom type classes to a separate module
| | | | | | | * b71af72 (origin/self-avoiding-walks, self-avoiding-walks) reflow text
| | | | | | | * f28000f move notebook information/resources to dedicated README.md
| | | | | | | | *   4a5cbd2 (origin/code-quality, code-quality) merge updated upstream
| | | | | | | | |\  
| |_|_|_|_|_|_|_|/  
|/| | | | | | | |   
* | | | | | | | | 87cae90 (origin/tetris-variants, tetris-variants) rebuild README
* | | | | | | | |   92aa751 (origin/alexandria, alexandria) Add 'alexandria/' from commit '69b7e1b300e9283e158220c33a3258c1d9213973'
|\ \ \ \ \ \ \ \ \  
| * | | | | | | | | 69b7e1b add return values
| * | | | | | | | | 6f5a48f fixed bug adding duplicate tags each time Collection.find() was run
| * | | | | | | | | 36f5ef0 test simple search based on NLP query
| * | | | | | | | | 1b042cc add simple search parameter extraction
| * | | | | | | | | ec47cb8 add spacy dependency parsing for NLP commands
| * | | | | | | | | 1b93aef fix tag printing (add lookup by ID)
| * | | | | | | | | 3fb216b add base64_encoding parameter
| * | | | | | | | | 4ca55f6 add compress level setting
| * | | | | | | | | 1e40705 fix data serialization
| * | | | | | | | | 15852c4 use IDs in place of references to Tag objects within Page objects
| * | | | | | | | | 14551c0 add parameter defining percentage of nodes to display in the network visualization
| * | | | | | | | | 98dc2af Include time of backup in archive
| * | | | | | | | | 7a255aa cleanup
| * | | | | | | | | e1c700b store persistent list of common keywords
| * | | | | | | | | 23c6bf3 add more statistics
| * | | | | | | | | bce2e32 add UUIDs
| * | | | | | | | | 8581aa4 add method to open a random page
| * | | | | | | | | 7b2d008 add hide_labels parameter and fix keyword updating (after subpage extraction)
| * | | | | | | | | 5df3b79 handle keyword extraction in the Collection that contains the pages; this allows sorting keywords by frequency, for example to only use the most common 10 or 20 as tags
| * | | | | | | | | dc9a580 some adjustments to network visualization
| * | | | | | | | | 6a6904b miscellaneous
| * | | | | | | | | 609d397 add Collection statistics/summary method
| * | | | | | | | | 6b6908d add keyword extraction parameter
| * | | | | | | | | 2206ef3 add network graph visualization
| * | | | | | | | | e2c01c0 add headers
| * | | | | | | | | ea929ea exclude common terms from automatic tags/keywords
| * | | | | | | | | 5f3620f add colored text output
| * | | | | | | | | 26af0c8 add keyword extraction from urls/page titles
| * | | | | | | | | 6a1678d basic Collection loading functionality
| * | | | | | | | | d4bf396 only create tags once
| * | | | | | | | | 188468d refactoring
| * | | | | | | | | e4da588 extraction of frozen/suspended pages
| * | | | | | | | | 3f5e5db allow saving collections to text files
| * | | | | | | | | 8cea88b add bookmark content retrieval/archiving
| * | | | | | | | | 7976a58 add string/print methods
| * | | | | | | | | 94a1e5a add Rule class
| * | | | | | | | | 8691562 add convenience method for tagging pages if their titles or urls contain a string
| * | | | | | | | | 0c5de41 add visualization method
| * | | | | | | | | 57701b5 automatically create tag if string (tag name) is provided
| * | | | | | | | | fb1db27 extract url parameters
| * | | | | | | | | f14a12e allow Collection subscripting
| * | | | | | | | | 2276d9f add tagging method for Collections (and other adjustments)
| * | | | | | | | | 3605df2 add Tag class
| * | | | | | | | | ee71d96 add Collection filtering method
| * | | | | | | | | 44af073 add multiple pages by url/info string
| * | | | | | | | | 1987929 add Page class
| * | | | | | | | | 3efb256 add Collection class
| * | | | | | | | | 9199623 add basic text file import
| * | | | | | | | | 451c9cf update gitignore
| * | | | | | | | | bb6078b ignore bookmark files
| * | | | | | | | | 5fb5c54 Initialize
|  / / / / / / / /  
* | | | | | | | |   c5baf58 Merge branch 'roulette-curves'
|\ \ \ \ \ \ \ \ \  
| * \ \ \ \ \ \ \ \   f8f9d1e (origin/roulette-curves, roulette-curves) Add 'roulette-curves/' from commit 'bff39483afb0b93e2355e5511840cdb34af5f021'
| |\ \ \ \ \ \ \ \ \  
| | * | | | | | | | | bff3948 handle parent spinner rotation offset
| | * | | | | | | | | eab4e25 handle parent spinner coordinate offset
| | * | | | | | | | | 38c4cc5 add radius alias ("r")
| | * | | | | | | | | faab331 fix theta handling
| | * | | | | | | | | aefff2f allow specifying draw method from the top down
| | * | | | | | | | | 2b11433 fix dimension argument processing
| | * | | | | | | | | b59f7f4 add "method" argument (to specify how the current spinner should interact with the provided canvas)
| | * | | | | | | | | 9e655c0 add add() method
| | * | | | | | | | | 11074ab add testing code
| | * | | | | | | | | decae2f add step method to update all spinners in roulette (and optionally update canvas/render)
| | * | | | | | | | | 3f4a9d3 add method to render a Roulette object by recursively calling draw() on its spinners
| | * | | | | | | | | 1db476b add base Roulette curve class
| | * | | | | | | | | 2df838f import other modules
| | * | | | | | | | | c7dbd92 implement render enable/disable option for spinner
| | * | | | | | | | | 42dd4c0 add method to draw point in spinner
| | * | | | | | | | | b47f97c add step method to rotate Spinner class instance
| | * | | | | | | | | 07da274 add spinner class base
| | * | | | | | | | | 32a3608 add point rotation functions (https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302)
| | * | | | | | | | | 930b155 Add line generator (https://stackoverflow.com/a/47381058)
| | * | | | | | | | | 29364e1 initial commit
| |  / / / / / / / /  
* | | | | | | | | |   967b02d (origin/locus, locus) Add 'locus/' from commit 'f551492651c1738d04ce93285d0bd85df1d79ed7'
|\ \ \ \ \ \ \ \ \ \  
| |/ / / / / / / / /  
|/| | | | | | | | |   
| * | | | | | | | | f551492 Add .deepsource.toml
| * | | | | | | | | 5a319e9 add some documentation
| * | | | | | | | | 35467ff add identity operator
| * | | | | | | | | 81fa473 add more operators
| * | | | | | | | | 7788c3e cleanup
| * | | | | | | | | cab8640 lots more refactoring
| * | | | | | | | | 6373cb9 more refactoring
| * | | | | | | | | 107c528 refactoring
| * | | | | | | | | 486dd0d add operator class
| * | | | | | | | | a33e142 add comments
| * | | | | | | | | f3b3f2b More testing + fix issue with data buffer persisting from one check to another
| * | | | | | | | | e54940f add one-directional operators
| * | | | | | | | | ee6c9ac add display method
| * | | | | | | | | 38f5b0f add Locus class
| * | | | | | | | | c9a5623 improve printout (all rows have even widths)
| * | | | | | | | | 827b320 add exponentiation operator
| * | | | | | | | | 8491fad fix bug causing incorrect evaluation past first interpreter iteration
| * | | | | | | | | 6c901da add iteration parameter
| * | | | | | | | | 7c56fbe add more operations
| * | | | | | | | | c736242 rewrite interpreter
| * | | | | | | | | 3e50859 first interpreter attempt
| * | | | | | | | | cd4c816 initial code
|  / / / / / / / /  
* | | | | | | | |   e0d58a6 (origin/cellular-automata-experiments, cellular-automata-experiments) Add 'cellular-automata-experiments/' from commit '0085b8ab5516e8f6156c4ec0c46ea4bb12f03361'
|\ \ \ \ \ \ \ \ \  
| * | | | | | | | | 0085b8a add improved tag parser (this was written a while ago, is somewhat messy, and will most likely be replaced)
| * | | | | | | | | 4b17c48 add function to split string into numeric and non-numeric sections
| * | | | | | | | | 69b796c update templates
| * | | | | | | | | 9f15721 add docstring to Search constructor
| * | | | | | | | | 7e17eae update docstring to use new format
| * | | | | | | | | 6759449 add example tags
| * | | | | | | | | 091f96a program-specific terms and abbreviations
| * | | | | | | | | 6dc4fb6 add docstrings for other parameters
| * | | | | | | | | 69f0ae0 add docstring
| * | | | | | | | | afbd935 global replacements
| * | | | | | | | | c3a7d9d add simple docstrings
| * | | | | | | | | e0b3510 expand docstring
| * | | | | | | | | fa1a030 parse symbols (e.g., >=, <, etc.)
| * | | | | | | | | 9f38c82 add parameter documentation template
| * | | | | | | | | 9145370 parse ranges for numeric parameters
| * | | | | | | | | 5565a7b add list of commonly used symbols
| * | | | | | | | | b4bb833 parse base parameter type
| * | | | | | | | | 52612db parameter documentation processor
| * | | | | | | | | 43f227f refactor method doc processing
| * | | | | | | | | ed5029d only extract docstring if top-level object
| * | | | | | | | | 3194216 more refactoring
| * | | | | | | | | b8703d0 add function to automatically generate section
| * | | | | | | | | 283a4d3 clean up template path definition
| * | | | | | | | | 57efc45 refactoring
| * | | | | | | | | 14e03fe misc
| * | | | | | | | | 752980a process parameter descriptions
| * | | | | | | | | 2df7965 save result when done processing documentation
| * | | | | | | | | 921c694 add subsection parsing
| * | | | | | | | | 8648a22 add simple parser to loop through lines in docstring and check for headers
| * | | | | | | | | ef1c10a add function to extract data from parameter list/annotations
| * | | | | | | | | 7a35482 add function to strip leading tabs from lines
| * | | | | | | | | 8255382 add function to detect leading whitespace
| * | | | | | | | | 4be0651 automatically document class methods
| * | | | | | | | | b40236f automatically document classes
| * | | | | | | | | aa6948e read template files into strings
| * | | | | | | | | 906e8de add doc gen settings
| * | | | | | | | | f069ca3 add class documentation template
| * | | | | | | | | aeb6a88 create .gitignore
| * | | | | | | | | e68c654 add method documentation template
| * | | | | | | | | 6dc09cd start documentation generator script
| * | | | | | | | | 7e00f48 testing different features
| * | | | | | | | | a6d5189 add short summary of features
| * | | | | | | | |   9bc1b3b Merge branch 'master' of https://github.com/generic-github-user/cellular-automata-experiments
| |\ \ \ \ \ \ \ \ \  
| | * | | | | | | | | 3432ec7 Create README.md
| * | | | | | | | | | 4060db2 3D voxel display of cellular automata across timesteps
| * | | | | | | | | | e243d61 optionally store each state/timestep of simulation
| * | | | | | | | | | 3b29733 record total time cell is "alive" over course of simulation
| |/ / / / / / / / /  
| * | | | | | | | | 18c4098 add return value option
| * | | | | | | | | 897d493 add option to apply function before displaying
| * | | | | | | | | fa3d6fc add display method
| * | | | | | | | | cf2fd03 add generations parameter
| * | | | | | | | | 9a71c64 testing code
| * | | | | | | | | be4716a add some other sample goals
| * | | | | | | | | 8eb3531 check for provided pattern before processing
| * | | | | | | | | 849790f allow custom search goal (e.g., highest/lowest final population, average cell age, etc.)
| * | | | | | | | | 3e1671d add option to end early if exact match is found
| * | | | | | | | | 7a06934 add option to search every generation of cellular automata (or just specified one)
| * | | | | | | | | 1ae81fc testing Search class and methods
| * | | | | | | | | 357cd78 create list of axes that includes hyperparameter and metric names
| * | | | | | | | | dc50332 add another (simpler) test search pattern
| * | | | | | | | | cc392ea add search function
| * | | | | | | | | d4d23a7 randomize generations if tuple/list is provided
| * | | | | | | | | 6763281 add a test search pattern
| * | | | | | | | | 2562a55 convert pattern to kernel (replace 0s with -1s to select against regions with live cells that should be empty)
| * | | | | | | | | 7bf5b95 add clone function
| * | | | | | | | | db13fc7 add Search class
| * | | | | | | | | 29ebfbf only plot first 3 dimensions
| * | | | | | | | | 8c31c77 add (working) parameter for setting number of steps in simulation
| * | | | | | | | | 0b22632 add hyperparameters (independent variables) to visualization
| * | | | | | | | | f8cd54b fix issue with initial random size calculation
| * | | | | | | | | ca26df8 update default hyperparameters
| * | | | | | | | | 727bace add axis labels
| * | | | | | | | | 9d91ea3 use randomizer in Automata constructor
| * | | | | | | | | 6de0e3e collect and store additional arguments
| * | | | | | | | | d44e722 add more defaults
| * | | | | | | | | b0c0e22 handle parameters in simulation loop
| * | | | | | | | | 8f7d502 add merging of default hyperparameters with provided ones
| * | | | | | | | | 6e97ba2 bug fixes
| * | | | | | | | | a977d94 allow random selection of trial to display
| * | | | | | | | | 4cee829 add argument for size of initial random noise
| * | | | | | | | | c706be3 add argument to set chance of cell starting out living or dead
| * | | | | | | | | 6d2e3da add non-numpy reduction functions (like getting only the last value of the metric)
| * | | | | | | | | 5f096da automatically apply population reduction function
| * | | | | | | | | c694fb3 adjust plot settings
| * | | | | | | | | bcd4f0d use generations hyperparameter
| * | | | | | | | | 331b594 track average number of neighbors per cell over time
| * | | | | | | | | 44a7344 define some functions for reducing axes
| * | | | | | | | | f6dab1f fix typo
| * | | | | | | | | 19b4b55 improved collection and processing of simulation data
| * | | | | | | | | 4efe7cc add line graph display for more simple datasets
| * | | | | | | | | 050460c improve description of metrics
| * | | | | | | | | 4c11a8d allow display of 3 metrics with 3D scatter plot
| * | | | | | | | | 2161962 add comments
| * | | | | | | | | 014792f add docstrings
| * | | | | | | | | 6c7406e add more parameters
| * | | | | | | | | 7cd077d add better logging
| * | | | | | | | | a60f6fe testing code for simulation aggregator
| * | | | | | | | | 0e869df add method to display results as 2D scatter plot
| * | | | | | | | | 46fedc3 add method to run cellular automata simulations and collect results
| * | | | | | | | | 9709d4a add other parameters to Aggregator class
| * | | | | | | | | 4445179 add default hyperparameters and reporting metrics
| * | | | | | | | | 7faabec fix age reporting when using scipy convolution method
| * | | | | | | | | 21d1764 rename variable for clarity
| * | | | | | | | | 6e9525b allow user to change pen width with -/= keys
| * | | | | | | | | 44843a7 pass args to subclass
| * | | | | | | | | 63d24ae allow integer as "size" parameter for cellular automata world
| * | | | | | | | | 1774034 add double-click for pausing simulation
| * | | | | | | | | ecf0e7a minor refactoring
| * | | | | | | | | b6541ff remove cells using right click and drag
| * | | | | | | | | f2f0417 various testing and debugging
| * | | | | | | | | 7c28576 add Aggregator class to run sets of simulations with different settings
| * | | | | | | | | 7e451d4 allow user to place cells with the mouse
| * | | | | | | | | aada32d make temp an instance variable
| * | | | | | | | | 7eac30b add option for using vectorized 2D convolutions to process cellular automata
| * | | | | | | | | 7ed1ffa add convenience class for Conway's Game of Life
| * | | | | | | | | 5c5090b add neighborhood (slice size) parameter
| * | | | | | | | | 3672f8b add parameters for cellular automata rules
| * | | | | | | | | ccea94b allow coloring of cells by number of neighbors
| * | | | | | | | | 139b97e track average cell age over time
| * | | | | | | | | 66231df track age of each cell
| * | | | | | | | | 214d25e track generation and total cell processing
| * | | | | | | | | 44d0a48 add render parameter
| * | | | | | | | | ef44f16 add population tracking over time
| * | | | | | | | | 85d022a content parameter (for providing cellular automata world)
| * | | | | | | | | 38590db add dimension inference from cell width and world size
| * | | | | | | | | e80daca add time report
| * | | | | | | | | 11151ed add simulate() method
| * | | | | | | | | c26ed73 optimize with np.where()
| * | | | | | | | | 7c737e5 add simulation renderer
| * | | | | | | | | c67ac2b add function step/evolve simulation
| * | | | | | | | | c94d74c add more properties
| * | | | | | | | | 47eaccb add cellular automata class base
| * | | | | | | | | 92bee0b create Scene class
| * | | | | | | | | 535ee82 tkinter canvas boilerplate code
|  / / / / / / / /  
* | | | | | | | |   44398e3 (origin/foldz, foldz) Add 'foldz/' from commit '5d15ef12e8690b0164d0b6d7cd926165df4a6e71'
|\ \ \ \ \ \ \ \ \  
| * | | | | | | | | 5d15ef1 Create CONTRIBUTING.md
| * | | | | | | | | 4e02f1a more geometry classes
| * | | | | | | | | f887829 Update some generated/config files
| * | | | | | | | | 5ba6b34 Create README.md
| * | | | | | | | | 2bd5391 Build docs
| * | | | | | | | | 1a2831d reorganize imports
| * | | | | | | | | 7c7e068 Add more Polygon class methods
| * | | | | | | | | 8691f74 Testing/notes
| * | | | | | | | | 9a4b0b3 Add code for randomly folding polygonal curve/linkage using custom geometry classes
| * | | | | | | | | 3e9d1ed Add function for checking intersection of two line segments
| * | | | | | | | | 18eba8b Add string methods
| * | | | | | | | | d9391cf Add function for solving system of linear equations
| * | | | | | | | | e8bcfc3 Add functions for calculating midpoint, slope, and y-intercept of line segment
| * | | | | | | | | f21ddf2 Add method for randomly folding a linkage/polygonal curve
| * | | | | | | | | 66c3e02 Add other (reused) geometry classes
| * | | | | | | | | 4905641 Move code for updating position axis variables (x, y, ...) to dedicated method
| * | | | | | | | | fe0fbd2 Add function for getting list of a linkage's self-intersection points
| * | | | | | | | | 7c28ecc Add function for checking if a linkage intersects itself at any point
| * | | | | | | | | 316ad0a Add function for rotating all line segments in one "side" of a linkage/chain
| * | | | | | | | | fc4302a Add Event class
| * | | | | | | | | 4e4fd31 Add method for rendering Foldable object geometry to SVG
| * | | | | | | | | 6c68639 add autogenerated scripts
| * | | | | | | | | 99ec506 Add "Foldable" class
| * | | | | | | | | e930432 Add generated config files
| * | | | | | | | | 39daefb Add methods for common math operations to Point class
| * | | | | | | | | 1156911 Add manifold class
| * | | | | | | | | 0f15058 Add geometry classes
| * | | | | | | | | df891fd Create fold.py
| * | | | | | | | | efa2042 Create settings.ini
| * | | | | | | | | 95da766 Add setup files
| * | | | | | | | | 9377900 Initial commit
|  / / / / / / / /  
* | | | | | | | | bc866cb Merge branch 'meta'
|\| | | | | | | | 
| * | | | | | | |   86e3465 Merge branch 'programming-puzzles' into meta
| |\ \ \ \ \ \ \ \  
| | * \ \ \ \ \ \ \   9b64bbe (origin/programming-puzzles, programming-puzzles) Add 'programming-puzzles/' from commit '3ec6e42ee6bc8513a57a10b970e7d56724ab6113'
| | |\ \ \ \ \ \ \ \  
| | | * | | | | | | | 3ec6e42 Add .deepsource.toml
| | | * | | | | | | | b5dc423 Update puzzles.ipynb
| | | * | | | | | | | 4fe4fc5 testing
| | | * | | | | | | | b1406ea add divide-and-conquer method for computing large factorials
| | | * | | | | | | | be6bee8 compute sample results and plot
| | | * | | | | | | | 2f6d189 add Python versions of functions
| | | * | | | | | | | 5319bf2 additional tiling challenges
| | | * | | | | | | | c599a41 add base for logical inference programming puzzle
| | | * | | | | | | | 5a38040 Add memoized factorial function
| | | * | | | | | | | b065504 Update puzzles.py
| | | * | | | | | | | 7bf9155 add factorial-length problem
| | | * | | | | | | | ae33a57 add extensions of chessboard tiling puzzle
| | | * | | | | | | | 77a1eb6 add chessboard/domino tiling problem
| | | * | | | | | | | 3ab107b Add simple solution to first puzzle
| | | * | | | | | | | 8a9c663 Add function for checking if an integer string contains its square root
| | | * | | | | | | | 1c244ea Add puzzle (and first attempt at solving)
| | | * | | | | | | | 7b6accd Add introduction
| | | * | | | | | | | e717c5c Create .gitignore
| | | * | | | | | | | d9a7a7b Create puzzles.ipynb
| | | * | | | | | | | b366e13 Initial commit
| | |  / / / / / / /  
| * | | | | | | | |   4efe011 (origin/visual-computing-simulation, visual-computing-simulation) Add 'visual-computing-simulation/' from commit 'a9c03dd593f10544ffee4f536d8b9be2fd99f307'
| |\ \ \ \ \ \ \ \ \  
| | |/ / / / / / / /  
| |/| | | | | | | |   
| | * | | | | | | | a9c03dd set input cells and random cells before simulating logic components
| | * | | | | | | | fed497d generate array from input text (schematic)
| | * | | | | | | | 7d55787 Add parameters/settings and other variables
| | * | | | | | | | d2a2c89 auto-generate colors (or colormap indices) for specific operators
| | * | | | | | | | 0036c07 add input/output operators (symbols)
| | * | | | | | | | 00fc4b7 add operator symbols for moving data around
| | * | | | | | | | 37448aa add some basic logical operators
| | * | | | | | | | 5df768d Add sample logic circuit schematic (full binary adder)
| | * | | | | | | | 18abf7f Add list of relative coordinates for adjacent cells
| | * | | | | | | | baa9d48 Create simulation.py
| | * | | | | | | | 6e540a4 Create .gitignore
| |  / / / / / / /  
| * | | | | | | | 16026a6 add status of newly integrated projects
| * | | | | | | | f47d8ed add some notes on methodology/repository organization
| * | | | | | | | 35e2315 add some badges for decoration
* | | | | | | | | 00eef5c rebuild README
* | | | | | | | |   0ee232e Merge branch 'project-summary'
|\ \ \ \ \ \ \ \ \  
| |_|/ / / / / / /  
|/| | | | | | | |   
| * | | | | | | |   c9f4af8 (origin/project-summary, project-summary) Add 'project-summary/' from commit 'd124f5466d516d8b08ae97c2e25c9d7f8ff6c7c3'
| |\ \ \ \ \ \ \ \  
| | |/ / / / / / /  
| |/| | | | | | |   
| | * | | | | | | d124f54 add information about API tokens
| | * | | | | | | 3b820a3 add more comments
| | * | | | | | | fb35d84 refactor with functions
| | * | | | | | | 2a64f5a Add completion percentages to some columns
| | * | | | | | | 35eac7f clean up unused code
| | * | | | | | | 77b60b0 Add License column to table
| | * | | | | | | c5a1aab add comments
| | * | | | | | | de3aff9 Align specific columns by name
| | * | | | | | | 43286e4 Add link to create a new issue in a repository
| | * | | | | | | 349305f shorten long repo descriptions
| | * | | | | | | bcf3e7a Add notebook source
| | * | | | | | | 2f2d1a3 Update .gitignore
| | * | | | | | | 9fd60eb save generated table to file
| | * | | | | | | 6bfcd08 add repo creation timestamp (and sort by milliseconds since epoch, newest first)
| | * | | | | | | 274405a format topics
| | * | | | | | | 873083d add function for truncating topics list/other lists of strings
| | * | | | | | | 02ce1b6 add API request headers
| | * | | | | | | d2001af save cache and display result
| | * | | | | | | 3c14684 generate table row for each repository
| | * | | | | | | 3a8701e load cached data from local file
| | * | | | | | | c5466a3 add function for formatting table cell correctly
| | * | | | | | | b24f964 generate table header
| | * | | | | | | e385d80 add list of fields to display in table
| | * | | | | | | 62b90b0 add function to look up file tree for each repository and check if a README exists
| | * | | | | | | be0b17b get API token from local file
| | * | | | | | | 89feb16 ignore cache files
| | * | | | | | | 2fce435 get list of repositories using GitHub REST API
| | * | | | | | | fdddd47 Create summarize.py
| | * | | | | | | 664d7e0 add checkpoints to gitignore
| | * | | | | | | a2077ff change encoding
| | * | | | | | | 937c3f8 Add gitignore
| |  / / / / / /  
* | | | | | | |   52fb267 Add 'attractors/' from commit '7b772bba73545e2ce98916e458b16b2fc44f2bfb'
|\ \ \ \ \ \ \ \  
| |/ / / / / / /  
|/| | | | | | |   
| * | | | | | | 7b772bb Create requirements.txt
| * | | | | | | e029682 Add return values to docstrings
| * | | | | | | 8bc5ed7 Add descriptions of Roulette_Curve.__init__ parameters
| * | | | | | | 6f81593 Add transform_point method docstring
| * | | | | | | d5278ac Add docstring for draw_point method (of RouletteCurve class)
| * | | | | | | 9525410 Add line function docstring
| * | | | | | | 34921bf Re-build documentation
| * | | | | | | 450a98d Add credits to nbdev/Jupyter (Lab)
| * | | | | | | aa40ccc Add links to documentation and license
| * | | | | | | 615aa3d add other unit tests
| * | | | | | | 48581fe Add more tests/parameter value validation
| * | | | | | | b4fbddd Add tests to transform_point
| * | | | | | | 6d752ad Add tests to render method
| * | | | | | | 3ff041e Update index.html
| * | | | | | | 3bf1a05 Set theme jekyll-theme-cayman
| * | | | | | | 381efa9 Update setup.py
| * | | | | | | 42ed524 Correct min required Python version
| * | | | | | | 2611599 Add explicit list of dependencies
| * | | | | | | ceb6e06 Change license
| * | | | | | | 514614e Add list of dependencies
| * | | | | | | 89d7b20 Add some keywords
| * | | | | | | c9f6203 temporarily allow docs build without specifying license in settings.ini
| * | | | | | | fa6a696 Update docs build
| * | | | | | | 78b506d Add (Jupyter/IPython) notebook sources
| * | | | | | | 021db5f Refactor rendering method into smaller functions and add other parameters/settings
| * | | | | | | 044e009 While running simulation, periodically check if time limit has been exceeded (and end simulation if it has been)
| * | | | | | | 778bca7 Add option for simultaneously simulating and rendering system
| * | | | | | | a4f93bf Add docstring (and parameter descriptions) to simulate method
| * | | | | | | b5f72f3 Add method that runs JIT-compiled simulate_accelerated function
| * | | | | | | 1d41b9b Add simulate_accelerated docstring
| * | | | | | | bb85787 Create LICENSE.md
| * | | | | | | 72c52cc Add descriptions of specific mode parameter values
| * | | | | | | 7d2bc1c Add render method docstring
| * | | | | | | 0ff9870 miscellaneous tweaks & placeholders
| * | | | | | | b142bec Create home_sidebar.yml
| * | | | | | | 13a3a76 misc
| * | | | | | | c811047 Create settings.ini
| * | | | | | | e07a117 Generate README from index.ipynb
| * | | | | | | ba71172 Create _config.yml
| * | | | | | | 1150bd4 Add function for drawing line with start/stop points
| * | | | | | | e35b373 Create setup.py
| * | | | | | | f5bb104 Update metadata
| * | | | | | | 629ce3f add docstring
| * | | | | | | eebe459 Store rendering offset as instance attribute
| * | | | | | | c586ba8 Add necessary imports
| * | | | | | | e8a7e24 Build docs homepage and add generated images from examples
| * | | | | | | 2579fe0 Build docs
| * | | | | | | 08ada38 Create CONTRIBUTING.md
| * | | | | | | df7662e Add helper function for getting (some) properties of class instance as a dict
| * | | | | | | da84e55 Add function for clearing a RouletteCurve object's points
| * | | | | | | ebe2807 add some more instance variables
| * | | | | | | 29f4123 Add function for accelerated simulation using Numba JIT compilation/vectorization
| * | | | | | | fc37d8f Update metadata
| * | | | | | | 4616fb3 Add "dist" mode for rendering evolution of system
| * | | | | | | 07a87e1 Add relative-angle based simulation method
| * | | | | | | 54a9dd5 Prepare rotation matrices in advance
| * | | | | | | bc4b9a8 Add instance properties/variables for tracking history of pivot locations and segment angles
| * | | | | | | 9f2810d JIT-compile functions with Numba
| * | | | | | | 9a77e63 Add function for rotating point about another point given an angle
| * | | | | | | 3c3cbca Add function for efficiently generating rotation matrix for a given angle (in radians)
| * | | | | | | 6968a90 Add function for rendering points as image/heatmap
| * | | | | | | 00000e0 Add helper function for replacing tuples in iterables (e.g., in function arguments) with the result of passing the tuples as arguments to a random number generator
| * | | | | | | 09bed59 Add function for generating roulette curve points from parameters
| * | | | | | | 58d03ef Add nbdev config files
| * | | | | | | 1c95580 Create _nbdev.py
| * | | | | | | 01b1062 Randomly select segment lengths and speeds if not provided
| * | | | | | | fd88b91 Add RouletteCurve class
| * | | | | | | 7326d79 Create core.py
| * | | | | | | de3b718 Initial commit
|  / / / / / /  
* | | | | | | f13f7d4 add new projects (integrated from other repos)
* | | | | | |   b0d2a7a Merge branch 'master' into meta
|\ \ \ \ \ \ \  
| * | | | | | | 81dab70 rebuild README
| * | | | | | |   b5aa9c5 Merge branch 'python-experiments'
| |\ \ \ \ \ \ \  
| | * \ \ \ \ \ \   d7ccb72 (origin/python-experiments, python-experiments) Add 'python-experiments/' from commit '23fef38879b5506c943e59ca2ab26f54f3c7b4ec'
| | |\ \ \ \ \ \ \  
| | | * | | | | | | 23fef38 Add sample code snippet (prime number generator)
| | | * | | | | | | 322e349 Add experiment summary
| | | * | | | | | | d44bc2a Create requirements.txt
| | | * | | | | | | 169c1f5 Create symbolic-algebra.ipynb
| | | * | | | | | | e95faf7 Testing
| | | * | | | | | | e4f24e3 automatically assign default variables/symbols
| | | * | | | | | | f8c4e6b Generate magic methods for common math operations
| | | * | | | | | | e07648d Add Symbol class
| | | * | | | | | | 6831c90 Add operator class-specific string methods
| | | * | | | | | | aaac70c Add operator (sub)class
| | | * | | | | | | 252fea8 Add string conversion methods
| | | * | | | | | | 306a37e Testing dynamic/automated variable creation
| | | * | | | | | | 61212b7 Add Expression class
| | | * | | | | | | 059d0f7 Create symbolic-algebra.py
| | | * | | | | | | 75a92f8 add transform combination testing limit
| | | * | | | | | | 36fefdd support application of iterable transform to list (e.g., of words in input string) instead of only text
| | | * | | | | | | aacb1f5 add alternative test strings
| | | * | | | | | | e7b7551 Track number of transform combinations checked
| | | * | | | | | | 4d78d27 Search combinations of varying lengths (1 to max)
| | | * | | | | | | fde46d0 Add notebook version of code
| | | * | | | | | | e67419b Loop through possible combinations of string transformations and test them on examples
| | | * | | | | | | b83b8d1 add names of string transformations
| | | * | | | | | | bf339eb add example string mappings
| | | * | | | | | | 8e3cc58 Iteratively replace nested type keywords with their corresponding regular expressions
| | | * | | | | | | 7eab638 add more test statements/operations
| | | * | | | | | | 3950f53 add list of possible string operations
| | | * | | | | | | db6dff5 Create .gitignore
| | | * | | | | | | 9651aa2 Add function for repeating a value/array a certain number of times along multiple axes
| | | * | | | | | | fa4fab0 add function for generating iterated function string
| | | * | | | | | | a103acc Create automacro.py
| | | * | | | | | | 542f748 Add regexes for common statements and expressions
| | | * | | | | | | 74102bb Add test statements
| | | * | | | | | | 96314b9 Add imports
| | | * | | | | | | 4dd0635 Create README.md
| | | * | | | | | | 5798ff2 Create LICENSE.md
| | | * | | | | | | 9d5a9ec Create .gitattributes
| | |  / / / / / /  
| * | | | | | | |   0e79829 Merge branch 'python-snippets'
| |\ \ \ \ \ \ \ \  
| | * \ \ \ \ \ \ \   bbbe213 (origin/python-snippets, python-snippets) Add 'python-snippets/' from commit 'a20f7f9b234b69a275ae6828e941c5e9b9d692f3'
| | |\ \ \ \ \ \ \ \  
| | | |/ / / / / / /  
| | |/| | | | | | |   
| | | * | | | | | | a20f7f9 Add IPython/Jupyter notebook version of code
| | | * | | | | | | 8d35040 Add function for generating change given an amount of money as an input
| | | * | | | | | | 0811f4c add list of coins/bills and corresponding amounts
| | | * | | | | | | 53063c3 Add function for determining the smallest combination of multiples of some given values needed to produce a larger number
| | | * | | | | | | 4e548bb add function for making word plural
| | | * | | | | | | cbcd32e add function for generating text list from list of items
| | | * | | | | | | 521ade9 add title-case function
| | | * | | | | | | 3607532 Add nested list flattening function
| | | * | | | | | | 3ed717f Add prime-generating function
| | | * | | | | | | 56e0766 Create .gitignore
| | | * | | | | | | 302a9df Create README.md
| | | * | | | | | | e0f62ac Initial commit
| | |  / / / / / /  
| * | | | | | | |   e5ff69d Merge branch 'quickplot'
| |\ \ \ \ \ \ \ \  
| | |_|/ / / / / /  
| |/| | | | | | |   
| | * | | | | | |   e5cb7aa (origin/quickplot, quickplot) Add 'quickplot/' from commit 'f6d19babdcb793315ea41aa53d6e2fa3f9569c1c'
| | |\ \ \ \ \ \ \  
| | | * | | | | | | f6d19ba Create requirements.txt
| | | * | | | | | | 717a0fb Add colorbar
| | | * | | | | | | da4b275 misc. (plot style, instance attributes, etc.)
| | | * | | | | | | be9f990 Add method for generating contour plots
| | | * | | | | | | 0ab62c7 Add 2D histogram helper method
| | | * | | | | | | 091c446 more docstrings
| | | * | | | | | | 16626c5 add method docstrings
| | | * | | | | | | 5af863a miscellaneous testing code/unused code
| | | * | | | | | | 6ccbce4 tweak (default) plot settings
| | | * | | | | | | 5b79824 Support float value for "annotate" argument
| | | * | | | | | | 44b08bd Test contour plot generation
| | | * | | | | | | f91d4c8 add test plot
| | | * | | | | | | 560a52f add heuristic for automatically repositioning labels to minimize overlap
| | | * | | | | | | 6bf2e6e Add helper Array class (wraps np.ndarray)
| | | * | | | | | | 495c58d Randomly sample points and add annotations showing their coordinates
| | | * | | | | | | 27f8dea Add method for generating Python code (non-dependent on quickplot) that builds equivalent plot
| | | * | | | | | | 539d026 Automatically set axis labels and scales for each spatial dimension (x, y or x, y, z)
| | | * | | | | | | c4246cc Add method for adding coordinate labels/annotations to scatter plots
| | | * | | | | | | c780f35 Add helper methods for generating grids of indices
| | | * | | | | | | 501e8f5 Add function for randomly sampling slices of array
| | | * | | | | | | cc47a25 Adjust scatter plot marker sizes based on number of points in plot if use_density is set to True
| | | * | | | | | | 2ef3f8e Add some todos
| | | * | | | | | | c6bb19b Handle projection argument (2d, 3d, polar)
| | | * | | | | | | 53f14d9 generate plot
| | | * | | | | | | 65996da Process plot settings/options (substitute aliases and values)
| | | * | | | | | | 74bde2e Add heuristic for determining whether log scale should be used for a given axis
| | | * | | | | | | a00532d Add method for generating plot
| | | * | | | | | | 590b89e Add Plot class
| | | * | | | | | | 304d5f2 Add imports
| | | * | | | | | | b584639 Add project summary
| | | * | | | | | | 9fdcd7c Initial commit
| | |  / / / / / /  
| * | | | | | | |   cd2322b Add 'fractals/' from commit '6d1b5081d64ae55a4b05bce0fcba1a5bacb23633'
| |\ \ \ \ \ \ \ \  
| | |/ / / / / / /  
| |/| | | | | | |   
| | * | | | | | | 6d1b508 minor bug fixes
| | * | | | | | | 1867fa4 Add option ("direct") to draw the fractal to pixel grid while generating it
| | * | | | | | | c706288 add random transforms applied to points before moving toward vertex
| | * | | | | | | 58ac046 add option for multiple interpolation ratios (i.e., randomly select what percentage of the distance is travelled from the current location to the selected vertex)
| | * | | | | | | 8cfe054 more testing
| | * | | | | | | 5e53a9d add more transforms/functions for iterative generator
| | * | | | | | | 8e0a005 add render method
| | * | | | | | | 7d17460 add generate method (not yet complete)
| | * | | | | | | 94d75be add iterated function-based fractal class
| | * | | | | | | aedf008 add Attractor (super)class
| | * | | | | | | 540d731 cleanup
| | * | | | | | | 18d4e08 miscellaneous
| | * | | | | | | 6dcdf94 fix random rule generator and add random number of sides
| | * | | | | | | d14c515 add random rule/restriction generation for vertex selection
| | * | | | | | | d3b3478 add SierpinskiTriangle convenience class
| | * | | | | | | 25d40ff add info strings to ChaosGame methods
| | * | | | | | | 3b51f6c add method to divide line into equal segments
| | * | | | | | | e511c16 add "jump" distance parameter
| | * | | | | | | ef14a70 add looping point distance function
| | * | | | | | | 36ad665 add function-based point evaluation
| | * | | | | | | 6a79708 add different point coloring methods
| | * | | | | | | 7b066ef add simple rules limiting vertex selection
| | * | | | | | | eebe672 correct orientation
| | * | | | | | | d03714e add render method
| | * | | | | | | 3e54a41 add generate method
| | * | | | | | | f3a2471 add ChaosGame class
| | * | | | | | | 14222ca add automatic rounding to handle floating point error
| | * | | | | | | 1eafc08 add polygon string method
| | * | | | | | | cea799d add point print method
| | * | | | | | | 73b69ac Add RegularPolygon class
| | * | | | | | | 829cedb Add Polygon class
| | * | | | | | | 82528f9 add move and rotate methods to Line class
| | * | | | | | | 032b547 add Line class
| | * | | | | | | de316ad add 2d rotation about a point
| | * | | | | | | 2ac41ca add move method
| | * | | | | | | e680af9 add point class
| | * | | | | | | 93515f9 add info for Fractal.autozoom method
| | * | | | | | | 735ba4c testing other random parameters
| | * | | | | | | 6671bae add random arguments
| | * | | | | | | 118ab90 reorganize method arguments
| | * | | | | | | 7c9e37d cleanup
| | * | | | | | | b011fbe reorganize fractal generation and rendering system
| | * | | | | | | 00f2e1d refactoring (create generate method)
| | * | | | | | | 3dea437 Add info string for Fractal class (and other tests)
| | * | | | | | | 3686270 add documentation for Fractal.scale method
| | * | | | | | | d6d2a35 add cmap parameter
| | * | | | | | | 085ef99 add display method
| | * | | | | | | 1954999 improve default arguments
| | * | | | | | | 4d9edf7 add automatic extraction of interesting section of fractal (based on variance)
| | * | | | | | | ea8665f add method for evaluating variance of different sections of fractal render
| | * | | | | | | 30cd739 create Fractal class
| | * | | | | | | 75cd945 fix smooth coloring algorithm (scale to maximum iteration values)
| | * | | | | | | 68a5a56 testing smooth coloring function (normalized iteration count)
| | * | | | | | | bcb77fd add main header
| | * | | | | | | 1664f0f add parameter to combine multiple axes into a single image
| | * | | | | | | e68dd6b add global parameter for number of interpolation steps
| | * | | | | | | 349f026 add fractal metadata interpolation
| | * | | | | | | 1196268 re-add .gitignore
| | * | | | | | |   2eeeb28 Merge pull request #1 from generic-github-user/master
| | |\ \ \ \ \ \ \  
| | | * \ \ \ \ \ \   f0a1f04 Merge branch 'master' of https://github.com/generic-github-user/fractals
| | | |\ \ \ \ \ \ \  
| | | | * | | | | | | d60e3b8 ignore checkpoint files
| | | | * | | | | | | 0fe1dfc metadata
| | | | * | | | | | | a395688 Set up basic fractal generation function
| | | |  / / / / / /  
| | | * | | | | | | c60dc9f ignore checkpoint files
| | | * | | | | | | d5f15bb metadata
| | | * | | | | | | e1b8d3e Set up basic fractal generation function
| | |/ / / / / / /  
| | * / / / / / / 20315a0 Initial commit
| |  / / / / / /  
| * | | | | | |   c9ac18e Merge branch 'self-avoiding-walks'
| |\ \ \ \ \ \ \  
| | | |_|_|_|/ /  
| | |/| | | | |   
| | * | | | | |   ab98020 Add 'shelf/' from commit 'c1d707c4638d2c5c1f682a82d4fee4cc286aea43'
| | |\ \ \ \ \ \  
| | | * | | | | | c1d707c Add (brief) installation section to README
| | | * | | | | | d8f2e27 Add checkboxes to indicate feature development status
| | | * | | | | | 732844e Add more features to README
| | | * | | | | | 8966af8 misc.
| | | * | | | | | a7b01d6 Add comments
| | | * | | | | | 346699f Add util function docstrings
| | | * | | | | | c889065 Include statistics about size of pickled library representation (both compressed and uncompressed)
| | | * | | | | | 59731e6 Compress backup files
| | | * | | | | | 32a721a Move object pickling/string conversion to a separate function
| | | * | | | | | d5783de Add comma separators to printed statistics
| | | * | | | | | be8494d Add timestamps to export filenames
| | | * | | | | | 85403aa Include common terms in note exports
| | | * | | | | | 78500d6 Improve term extraction/filtering
| | | * | | | | | d0b9172 Store references to terms in note instances
| | | * | | | | | c0b1ece Fix other dependencies
| | | * | | | | | bb498ca Add missing import statements
| | | * | | | | | 2b6981e Move some more functions out of main script
| | | * | | | | | 0f17161 Move classes to separate scripts for ease of development
| | | * | | | | | c3ccb21 Allow sorting notes by length (in chracters) or number of words
| | | * | | | | | db5933b Add store option (if False, the loaded library will be returned instead of assigning to a variable)
| | | * | | | | | d3244ba Add changed() method
| | | * | | | | | 224f00a miscellaneous
| | | * | | | | | 6ae92ad Add command for displaying summary statistics about note library
| | | * | | | | | 1533de4 Add truncate method
| | | * | | | | | edbe195 Add regex search command
| | | * | | | | | d974a5a Store timestamp as String class instance
| | | * | | | | | 07d9570 Add method for generating text colored with ANSI escape sequences
| | | * | | | | | 681304a Add command for exploring data saved in backup files
| | | * | | | | | 8ac4c9d Add helper class with additional string methods
| | | * | | | | | 9b8f28f Add comments
| | | * | | | | | 6572cc5 Use note template to generate Markdown export files
| | | * | | | | | 0240d1e Add command for removing a specified value
| | | * | | | | | 8c4e314 Add note template for Markdown exports
| | | * | | | | | be697b9 Fix bug in ranking code
| | | * | | | | | 759413c Add option for providing numeric arguments to commands
| | | * | | | | | 8c01b11 Exclude numeric results
| | | * | | | | | 66a736c Allow weighting by length in characters or words/tokens of each candidate
| | | * | | | | | d24598b Add method for recalculating rankings based on saved comparisons
| | | * | | | | | 74f0467 Add note sorting command
| | | * | | | | | 574bf32 Add note ranking command
| | | * | | | | | 223612e Add more features to list
| | | * | | | | | e6cf2cf Add ranking method for interactively sorting notes by a specified attribute
| | | * | | | | | 9e45fb8 Add library and note class upgrade methods
| | | * | | | | | 2841536 Add upgrade method that generates missing fields in loaded objects
| | | * | | | | | f8ea828 Add log parameter
| | | * | | | | | 91748df Miscellaneous
| | | * | | | | | 3d6e2cd Minor tweaks to extract_terms() method
| | | * | | | | | 9b411d8 Allow returning a minimum number of results (i.e., the n closest notes to the target note)
| | | * | | | | | 96bcd78 Move database file path to Session object
| | | * | | | | | 5a564b5 Add comments to extract_terms method
| | | * | | | | | 4c688e6 Add function for extracting common terms and phrases from note library
| | | * | | | | | 7a5786a Slight backup adjustments
| | | * | | | | | 39df917 Add Markdown export feature
| | | * | | | | | fd4828d Add simple backup functionality
| | | * | | | | | ce161d0 Add feature list (subject to change)
| | | * | | | | | 62483cc Update gitignore
| | | * | | | | | c553feb Add comments
| | | * | | | | | 16c18c6 Add function for interactive command usage/note creation
| | | * | | | | | cc19a2d Add Tag class
| | | * | | | | | cd14f3b Add note class methods
| | | * | | | | | 3d55a57 Add Note class
| | | * | | | | | 97c6174 Add function for finding similar notes using edit distance metrics/fuzzy string search
| | | * | | | | | a2cbac0 Add method for adding note instances to libraries
| | | * | | | | | f89f7c3 Add library saving and loading functions
| | | * | | | | | 6496b66 Add Library class for storing collections of notes
| | | * | | | | | 4945aee Add base class for notes, tags, etc.
| | | * | | | | | 88a085f Add command line argument parser with argparse
| | | * | | | | | 5ca6668 Add README
| | | * | | | | | a84cbc9 Add shelf.py (will contain main scripts and command handler)
| | | * | | | | | ccf74ea Initial commit
| | |  / / / / /  
| | * | | | | |   122a13d Add 'self-avoiding-walks/' from commit 'fef229a276c71f444187311be874343f8f800651'
| | |\ \ \ \ \ \  
| | | |/ / / / /  
| | |/| | | | |   
| | | * | | | | fef229a add some more notes
| | | * | | | | e371d20 more terms
| | | * | | | | 62a88ee add links to other papers and threads regarding Hamiltonian paths/grid graphs
| | | * | | | | 9ea5be8 add more graph theory terms
| | | * | | | | 108e901 add more research links/OEIS entries
| | | * | | | | fad47a4 add option for allowing path to cross edges
| | | * | | | | 9f2de9a add notes
| | | * | | | | 2deeb5a add list of relevant search terms/keywords
| | | * | | | | ca1a668 add some more relevant links
| | | * | | | | 43ea396 Add option for randomizing tree search
| | | * | | | | 68984d6 Add depth-first tree search-based path discovery
| | | * | | | | 065443c add comments
| | | * | | | | 8d9db36 fix path length calculation
| | | * | | | | 073caac add more parameters
| | | * | | | | 93fd54c Add single-step backtracking
| | | * | | | | ddf2432 Update self-avoiding-walk.ipynb
| | | * | | | | 3f60f6b add supplementary materials
| | | * | | | | 96a373e add links to research papers on self-avoiding walks
| | | * | | | | dc6ddc3 miscellaneous
| | | * | | | | 5201167 improve visualization and add todos/future research topics
| | | * | | | | 707c1b3 optimize with Numba
| | | * | | | | c873064 Add Numba-compatible bounding function
| | | * | | | | 2ab0a8c Add links to threads about self-avoiding walks
| | | * | | | | 96a4cfe add notebook that mirrors script
| | | * | | | | 6c08921 add some graphs
| | | * | | | | 8af71f2 Add simulation code
| | | * | | | | cb90fc3 Create .gitignore
| | | * | | | | 901fa9d generate list of possible steps
| | | * | | | | fd08d33 Create self-avoiding-walk.py
| | | * | | | | df3371b Initial commit
| | |  / / / /  
| * | | | | |   d568adc Merge branch 'epidemic-modelling'
| |\ \ \ \ \ \  
| | * \ \ \ \ \   09e55e9 (origin/epidemic-modelling, epidemic-modelling) Add 'epidemic-modelling/' from commit '8794b9f38532e498fc65ec9f3f4ef1d0bf39e744'
| | |\ \ \ \ \ \  
| | | |/ / / / /  
| | |/| | | | |   
| | | * | | | | 8794b9f Add function for updating Person class instance
| | | * | | | | 3ff9ef5 Add method for simulating virus test (with optional inaccuracy)
| | | * | | | | ade18fc Add Person class
| | | * | | | | 7e2cecc Add Population class
| | | * | | | | b621561 Add History class
| | | * | | | | 6b35fc9 Create README.md
| | | * | | | | ec86c67 Add helper functions
| | | * | | | | 7b27941 Add string conversion methods
| | | * | | | | 2397043 Add Pathogen class
| | | * | | | | c8539af Create epidemic-modelling.py
| | | * | | | | 616c49a Initial commit
| | |  / / / /  
| * | | | | |   9fbb532 (origin/physics, physics) Add 'physics/' from commit '59e45d7f25b0ad89938a37317695b7f7428c8b68'
| |\ \ \ \ \ \  
| | |/ / / / /  
| |/| | | | |   
| | * | | | |   59e45d7 Merge branch 'master' of https://github.com/generic-github-user/ascii-physics-sim
| | |\ \ \ \ \  
| | | * | | | | af2e589 Set theme jekyll-theme-cayman
| | * | | | | | 6d13213 add command for building documentation with pdoc
| | |/ / / / /  
| | * | | | | 5d66559 build documentation
| | * | | | | 95db5a9 Create README.md
| | * | | | | 3a1698e add rotation and angular velocity tracking to object class
| | * | | | | 4ff543e move a few helper classes to a separate file
| | * | | | | f985adf cleanup
| | * | | | | 23a3949 Split code into multiple files to make development go smoother
| | * | | | | b25b5b8 remove unused Vec class code
| | * | | | | 8a3b05b more documentation
| | * | | | | 7ed8107 document Object class
| | * | | | | b2ff6e5 Material class documentation
| | * | | | | 95dd809 Add some documentation to Renderer class (via https://pdoc.dev/)
| | * | | | | 9432df7 add 4D helper class, might remain unused
| | * | | | | 2d6531b add some comments
| | * | | | | 1228562 ignore compiled python files
| | * | | | | bd1ee5d only get rtype once
| | * | | | | 1c0a248 property storage placeholder classes
| | * | | | | 16644ba remove unused scalar code
| | * | | | | 05d1c71 miscellanous, pt. II
| | * | | | | 38c9409 add motion delta handling
| | * | | | | 71770c9 updated simulation code to handle new renderer
| | * | | | | 03d3979 update default renderer settings
| | * | | | | aedc313 recursive self-call in rendering function (used with python canvas until I can find a workaround)
| | * | | | | cf58193 placeholders for opengl and cairo graphics (planning to implement in future)
| | * | | | | 28e57cc add canvas renderer (can currently only handle circles)
| | * | | | | 353b507 add line (ASCII) renderer
| | * | | | | a450729 method for looking up ASCII characters corresponding to incline angles
| | * | | | | 23d274f new frame rendering function
| | * | | | | ce12913 material class updates
| | * | | | | 91829ac more materials properties
| | * | | | | 8162a90 add output concatenation method
| | * | | | | 19d7819 initialization code for new (tkinter) canvas based renderer
| | * | | | | 256c7ac miscellaneous
| | * | | | | a233646 clean out old tests
| | * | | | | aba91cb create Name class (not entirely sure yet if this will be used)
| | * | | | | 2b5ffe4 unused code
| | * | | | | 81fb3f4 update random scene generation function
| | * | | | | 8f57703 add clear parameter to randomize() method
| | * | | | | c48dcd0 add more material properties
| | * | | | | 62bba49 more TODOs
| | * | | | | 294d6b1 create gitignore
| | * | | | | fbd5e32 add Angle class
| | * | | | | 1526692 add method to calculate angles of tangent lines around circle perimeter (still eneds some debugging)
| | * | | | | 80572b9 default for geometry parts should be a list
| | * | | | | 12440b9 testing python opengl bindings per https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/
| | * | | | | cef00b5 tests/todos
| | * | | | | aaea382 reorganize rendering functions
| | * | | | | dfc830c GlyphSet helper class
| | * | | | | 92ceed9 just in case
| | * | | | | cea2d5d Cleanup
| | * | | | | 2db9988 Add camera class
| | * | | | | c9af190 Add world and cluster classes
| | * | | | | 38d3414 multiple small updates/fixes
| | * | | | | eb6f2d9 Add simulation and renderer placeholder classes
| | * | | | | 848762d Add matter class
| | * | | | | 3d6a5fd Add material class
| | * | | | | cea2d2f Add circle class
| | * | | | | 2ba9137 Add Polygon class
| | * | | | | 10cc8c0 Add specialized subclasses of Geometry
| | * | | | | fef43d8 Add Geometry class
| | * | | | | 445cede fix gravity (sim was using the old .x/.y notation)
| | * | | | | 8c15a89 more tests
| | * | | | | 074f9ed decommission old classes and create aliases for new Tensor class
| | * | | | | cbe9dd9 add random scene generator
| | * | | | | 3922def add unit class
| | * | | | | 0d172b1 clean out some obsolete math functions
| | * | | | | 3a4db46 Add general tensor class + begin transitioning to NumPy arrays
| | * | | | | 4e3a800 add more tests
| | * | | | | 1e3126e add gravity function (currently unused)
| | * | | | | 781e589 some TODOs
| | * | | | | bcd4169 add more operations to scalar class
| | * | | | | 48e92d1 Non-reductive distance function
| | * | | | | be3e739 Default mass scalar for objects
| | * | | | | 819d278 Clean up math operation functions
| | * | | | | 148a842 Additional scene properties
| | * | | | | 34b148b Vec class distance function
| | * | | | | d78659c add position vector to object class (with backwards-compatible x & y properties)
| | * | | | | 22625ea add printing functions to Vec class
| | * | | | | 89a56dd add square and reduce (sum) functions to Vec class
| | * | | | | 76527af each utility function (Vec class)
| | * | | | | 46bb26b add some basic math functions to vector class
| | * | | | | 962a6ef add clone function to vector class
| | * | | | | 148b51a add scalar class
| | * | | | | 2bab5d6 use time in position change calculation
| | * | | | | d584521 handle edge wrapping
| | * | | | | c99287f add scene size handling
| | * | | | | 7800ef1 add unit dict to scene class
| | * | | | | 7f47595 clean up render testing code
| | * | | | | 32776ef start with random velocity
| | * | | | | ae15d1e update rendering function
| | * | | | | 5301e39 add velocity property to object class
| | * | | | | f999721 add physics stepping function
| | * | | | | b589acd create vector class
| | * | | | | 7c0d750 add simple renderer
| | * | | | | 109dda7 main scene/object classes
| | * | | | | 658d809 Initial commit
| |  / / / /  
* | | | | | 59d62c0 reflow branch list
* | | | | | 111afe0 add summaries of recent branches
* | | | | | 37a73d4 extract commands corresponding to template strings (moved to substitutions.yaml)
|/ / / / /  
* | | | |   79a8246 Merge branch 'packings'
|\ \ \ \ \  
| * \ \ \ \   f1932de (origin/packings-rust, origin/packings, packings-rust, packings) Merge remote-tracking branch 'packings/main' into packings
| |\ \ \ \ \  
| | * | | | | 9c38413 move files to subdirectory to allow merge with monorepo
| | * | | | | 58292da Refactor add_center
| | * | | | | ba9e195 Add README
| | * | | | | 07e0436 change some return types, etc
| | * | | | | b6180ba Add function for placing center block
| | * | | | | 63035a3 Add missing compute counters
| | * | | | | 61e06f0 Add global list of allocated polyominoes
| | * | | | | 33dda73 Add polyomino optimization function
| | * | | | | 0012982 cleanup
| | * | | | | 40dcb04 minor refactoring
| | * | | | | f1177db Add templates for other functions
| | * | | | | a1d2330 add node and graph structs
| | * | | | | da4d468 Generate and display sample polyominoes
| | * | | | | 74e6b8d update polyomino indexing scheme
| | * | | | | 7190a04 miscellaneous
| | * | | | | c9db171 Add main function
| | * | | | | e1af71e Add function for randomly removing blocks
| | * | | | | 0840c72 Add helper function for removing blocks
| | * | | | | b2931b7 Add function for adding blocks to polyomino (while maintaining both the geometric data structure and index)
| | * | | | | e037be9 Add function for finding available memory to store pointer to new index (vector) in
| | * | | | | 0071f44 add polyomino equivalence function
| | * | | | | ae8b76c Add randomized function for expanding polyominoes
| | * | | | | bbb3d8d Add function for computing perimeter of polyomino
| | * | | | | 9366309 Add function for counting adjacent blocks
| | * | | | | 4737686 misc
| | * | | | | fa74741 Add function for checking polyomino equivalence up to translation
| | * | | | | 33d8129 Add function for generating and counting polyominoes (in place)
| | * | | | | 36f893f Add function for getting pointers to all candidate cells in a polyomino representation
| | * | | | | 3d33edf Add function for testing whether 2 (aligned) polyominoes overlap
| | * | | | | 22d781b Add helper functions
| | * | | | | f246748 Add functions for releasing dynamically allocated memory (used to store arrays and polyominoes)
| | * | | | | b59d30b misc
| | * | | | | d54b2ce Add polyomino printing function
| | * | | | | 56ab5c9 Add function for safely getting pointer to a block from a polyomino
| | * | | | | e3b44b9 Add polyomino struct and constructor
| | * | | | | cb12b75 Add function for creating arrays
| | * | | | | 06f770b add TODOs
| | * | | | | 52de5b6 Add function for populating array with value
| | * | | | | 0e82000 Add ANSI escape codes for printing colored text
| | * | | | | 7e4c2a5 add vector and array structs
| | * | | | | dd5fcc5 Add C-based version of system
| | * | | | | c533d05 refactoring
| | * | | | | 79a95b4 Add method for removing squares from polyominoes
| | * | | | | 9eaa77e Add method for building larger polyominos by adding squares to edges
| | * | | | | f71322b Add str method to Polyomino class
| | * | | | | c2bf715 Add method for expanding polyomino representation to correct size
| | * | | | | 5fac011 Add Polyomino class
| | * | | | | c6c3b2d Add class for representing collections of polyominoes
| | * | | | | a48bce8 add packings.py
| | * | | | | f49d0c1 Initial commit
| |  / / / /  
* | | | | |   c203f54 Merge branch 'meta'
|\ \ \ \ \ \  
| |/ / / / /  
|/| | | | |   
| * | | | | 3217348 add labels to other projects in this monorepo
| * | | | | b5b027a add list of labels/topics to some projects
| * | | | | 6763501 add language information for some projects
| * | | | | f558afc add diagram of repository branching history
| * | | | | 2200f35 minor reorganization (added location indicators to some items)
| * | | | | e0f70c4 add descriptions of some status labels
| * | | | | 56384bf add info about some external repositories
| * | | | | bf2f053 add metadata for other projects
| * | | | | 224ffa9 add information about some projects' statuses
| * | | | | b66eca8 update formatting
| * | | | | a2166a6 add branch summaries
* | | | | | f798b6e update stats (again
* | | | | |   21fde43 Merge remote-tracking branch 'graphs/graphs'
|\ \ \ \ \ \  
| * | | | | | 228ea98 (origin/graphs, graphs) fix merge prep from last commit (on /giraffe)
| * | | | | | 343af69 move Randomizer class
| * | | | | | ee2e5d3 more cleanup and restructuring
| * | | | | | 59ace1a more cleanup
| * | | | | | c3cae9d Extract GridGraph and Node classes and move manual tests to a new script
| * | | | | | f104f12 move graph classes out of notebook
| * | | | | | 2aacd20 Push all current changes to new branch
| * | | | | | 41b74e9 Add method for sampling from distribution
| * | | | | | 49027ae add Randomizer class
| * | | | | | b5df399 Allow returning of grouped nodes/subnodes generated by add_node method using return_node='inner'
| * | | | | | 75a4c3a Add option to use edge weights in adjacency matrix
| * | | | | | dfdf267 Add parameters for specifying which node to return
| * | | | | | 1f310b0 add dictionary of default edge drawing parameters
| * | | | | | 28e4896 add more dependencies
| * | | | | | 6cfe5a0 Add parameters for weighted edges in RandomGraph
| * | | | | | 5c369c9 Add function for generating an adjacency matrix for a given graph
| * | | | | | c9d66a4 Add subclass for creating complete graphs
| * | | | | | be10448 Split Graph class methods across multiple cells
| * | | | | | 6bf7a1a Handle errors sometimes thrown when drawing graph edges
| * | | | | | 10a4055 Add method for merging two graphs' nodes
| * | | | | | 205ab95 add subclass for generating simple random graphs
| * | | | | | d7c7a0f Add metadata properties to node in constructor method
| * | | | | | 7ddc2a2 Pass metadata and other parameters to add_node and Node.init calls
| * | | | | | 226fdb9 misc
| * | | | | | e6ce8a6 Use updated Graph.find() method parameter syntax
| * | | | | | a7dcf53 Iteratively generate sequence and add nodes to the graph
| * | | | | | f0fee45 miscellaneous testing code
| * | | | | | d2bedb0 add node and edge visualization parameters (these are passed to pyvis)
| * | | | | | a72c8ba Add improved node coloring
| * | | | | | 4b850f7 Add example with sequences of arithmetic operations iterated on random inputs
| * | | | | | 290d1e0 delegate node initialization to add_nodes method
| * | | | | | 2b180ce Add example visualizing relationships between subsequences of a string
| * | | | | | b221f61 misc
| * | | | | | 87420c2 Allow searching for nodes matching one or more arbitrary conditions using find() function
| * | | | | | efdf97c Add node class method for adding another node that shares a group with the first
| * | | | | | 85a14e9 Get text nodes from a path along the corpus graph
| * | | | | | 75565d5 Add method for finding adjacent nodes to a given node (ones which are grouped with the target node)
| * | | | | | b5fce3f Testing
| * | | | | | 6830ca9 Pass kwargs to single-node method
| * | | | | | b1150b6 Add convenience methods/builtins
| * | | | | | c8ff4fb Add methods for randomly selecting nodes from a graph object
| * | | | | | ad34e36 Sample non-overlapping sets of sentences from text
| * | | | | | 88b2d4a Create giraffe.ipynb
| * | | | | | 47db551 Miscellaneous testing
| * | | | | | 759e849 Create a test graph and generate visualization
| * | | | | | e060960 Update class method names
| * | | | | | efa4b14 Calculate degree of node
| * | | | | | d871f40 add Node class
| * | | | | | 5e33396 Add method for adding multiple nodes from an iterable at once
| * | | | | | 3a8b19f Accept primitive arguments to Graph.add_node()
| * | | | | | 6efdac5 Allow node object as parameter to Graph.add_node() method
| * | | | | | 3602df1 Add method for adding a node to a graph given a list containing the node's value and other nodes it groups
| * | | | | | 44e39fb Add node search function
| * | | | | | f90cc0d Visualize graph edges
| * | | | | | 7fcae2c Update .gitignore
| * | | | | | 5c3de0d Add function for visualizing nodes with pyvis
| * | | | | | 409699a Add graph class
| * | | | | | f5f79a2 Sample sentences from the text corpus and calculate similarity values
| * | | | | | 482dd0e Load and process text corpus
| * | | | | | e43c4a4 Create giraffe.py
| * | | | | | 8fc0278 Create .gitignore
|  / / / / /  
* | | | | |   355b795 Merge remote-tracking branch 'keyboard-dyamics/main'
|\ \ \ \ \ \  
* | | | | | | eb37c98 update stats
* | | | | | |   baf623b Merge branch 'leetcode'
|\ \ \ \ \ \ \  
| |_|/ / / / /  
|/| | | | | |   
| | | | | | * d36cb4c rename ambiguous variable
| | | |_|_|/  
| | |/| | |   
| | * | | | 70c22af (origin/keyboard-dynamics, keyboard-dynamics) restructure to allow merging with main repo
| | * | | | d40a3fa Scale key location coordinates by keyboard length parameter
| | * | | | 56fe8fb Move code for computing cost of moving to new position to a dedicated function
| | * | | | a267602 Add more testing strings
| | * | | | 09bc3b5 Add other common characters/keys
| | * | | | f67da44 Add parameter for setting random seed
| | * | | | 2a12769 Add scatter plot (#1)
| | * | | | 3090b99 Move random string generation code to a new function
| | * | | | 951d5f8 Generate grouped bar plot displaying different metrics for each test string
| | * | | | caf5143 Generate histogram visualizing distributions of typing difficulty scores
| | * | | | 8ab38f5 Add function for randomly generating some strings and calculating corresponding scores
| | * | | | a76db9d Add README
| | * | | | d050a0a Add simplistic logging
| | * | | | d0d327c Add method for calculating typing cost assuming each character is typed using the nearest available pointer/finger
| | * | | | dd8de9e Add function for calculating "effort" needed to type a given string
| | * | | | 973dc46 ad some test strings
| | * | | | 37250bb Add querty keyboard layout as array of characters
| | * | | | c28b6c3 Add keyboard.py and main imports
| | * | | | 2228ef7 Initial commit
| |  / / /  
| | | | | * e123491 (origin/pythings-docs, pythings-docs) reflow README.md paragraphs/lists
| | | | |/  
| | | |/|   
| | | * | 0d8beb3 update "Branches" section formatting
| | | * | bc0be55 add rest of pythings-related branches
| | | * | 66f19a0 wrap long lines in source when generating README (some sections are painful to reflow in vim)
| | | * | 425a393 add summaries of most pythings sub-branches
| | |/ /  
| | * | c7c5d36 add mermaid diagram summarizing organization of project internals
| | * | ac7026c add some installation and usage information
| | * | f44982c add summary of features
| | * |   ba8c2c0 Merge branch 'pythings-comments' into pythings-docs
| | |\ \  
| | | * | 7f97e98 (origin/pythings-comments, pythings-comments) add some comments
| | * | | 3abd74a add more docstrings
| | * | | 84c7a90 add docstrings to Type class
| | | | | * 187577b (origin/lc-comments, lc-comments) more comments
| | | | | * 3325b35 more misc comments
| | | | | * 2d78667 add comments to spiral matrix solution
| | | | | * da4c7af add comments to checkZeroOnes
| | | | | * eb715df (origin/leetcode, leetcode) add new solutions from 08-28
| | | | | * e089b51 add solution for efficient search of partially sorted matrix
| | |_|_|/  
| |/| | |   
| * | | | 28728c8 more LC solutions
| * | | | 3f2ed2b add two more solutions from today
| * | | | 20e00db add solution for "shuffle string"
| | | | | * d3c9469 (origin/py-obf-cli, py-obf-cli) allow input file argument to obfuscator
| | | | | * 7968d3f use pipenv
| | | | | * 0b6257b (origin/python-obfuscator, python-obfuscator) move old python obfuscator to designated subdirectory
| | | | | * b93eec0 more cleanup and reorganization
| | | | | * b3c063a (origin/obfuscation, obfuscation) reflow comments and docstrings for vim
| | | | | * af06cfa extract TODOs
| |_|_|_|/  
|/| | | |   
* | | | | 3b30833 reorganize imported files and rebuild
* | | | |   b679244 Merge remote-tracking branch 'obfuscation/master'
|\ \ \ \ \  
| |/ / / /  
|/| | | |   
| * | | | 6e6a09b Add .deepsource.toml
| * | | | 5f8657a sort candidate keywords by length and combine into phrases/identifiers
| * | | | 3ced50b generate some random strings from keyword list
| * | | | f91e529 add function for generating identifiers from keyword list
| * | | | 2d3d055 add context parameter to other nodes
| * | | | 931e507 add some more preset keywords
| * | | | 94af7db add docstring
| * | | | ba3ec96 todo
| * | | | 2fd468f add function for converting an AST node to a string representation (for the network visualization)
| * | | | 16b1021 include context (ctx) parameter when generating AST nodes
| * | | | 8c01f65 add function for random string capitalization
| * | | | 30fe5be fix bug causing incorrect string encoding when the same pattern appeared more than once in the string
| * | | | 82a2feb add inverse trig functions (and corresponding domains/acceptable input ranges)
| * | | | d0e239d generate additional keywords from own source code
| * | | | e074cd2 extract keywords from builtin functions
| * | | | f512740 add list of terms to generate filler strings with
| * | | | edd38be add function to check strings for numbers
| * | | | 291eb7f add function to remove basic punctuation from a string
| * | | | 9cfbf3f misc
| * | | | e911d0f add function for splitting camel case identifiers
| * | | | 306ba49 use normal characters (ASCII letters + numbers) for string generation
| * | | | cedcec0 code reformatter adjustments
| * | | | 96035e6 todos
| * | | | 1d6b74c improve repairing of statements split between multiple lines
| * | | | d9722ce add comments
| * | | | caa7c16 miscellaneous
| * | | | c0f22af add trigonometric function-based encoding of numerical expressions
| * | | | 89938d8 add license
| * | | | 296cd06 store arity (number of arguments) of transform functions
| * | | | bc0f4f1 allow iterable parameter to randomly select number of characters to generate
| * | | | a32511a move function
| * | | | 0c37aa1 update line ending with correct character (was previously always "=")
| * | | | 462182d more TODOs
| * | | | afcb905 allow lambda wrapping for types other than int
| * | | | 97bda16 add other node descriptors
| * | | | 8e9ef8d misc
| * | | | a6a1efc add some descriptors to convert AST nodes to PyVis network nodes
| * | | | faa352a add docstring
| * | | | 5030aaa add more comments
| * | | | 0b51680 add comments
| * | | | 19db2b3 miscellaneous
| * | | | 669ee7f chain lists/tuples together after segmenting
| * | | | 8288d78 use addition to concatenate some strings
| * | | | 01b8a7e add method to get the first existing property of an object from a list
| * | | | aefee78 add function for evaluating attribute string (e.g., "property.detail")
| * | | | b3c9a6a add PyVis Network subclass for saving HTML without opening in the browser
| * | | | fb07d3e rewrite imports (and corresponding references) with aliased names
| * | | | 18cc48a replace repeating patterns in some strings with expressions representing the pattern
| * | | | 0bad3c4 misc
| * | | | 931ae31 limit size of generated strings
| * | | | 0affab7 fix broken line endings in certain variable assignments
| * | | | ec84fc9 add function for generating a small syntax tree with a source code template
| * | | | 4917cb5 add charset parameter
| * | | | 78ba06b add boolean inequalities
| * | | | 53bd64d add methods for detecting repeating substrings/patterns in strings
| * | | | 1773acd add more test statements
| * | | | 113dcf8 encode some strings with generated replacements
| * | | | 1073d51 add boolean equality conditions
| * | | | e649777 handle unhashable types
| * | | | 986ff05 traverse child nodes
| * | | | bf5387a randomly subdivide lists and tuples
| * | | | d3b8e3c determine number of segments from string length
| * | | | a784cb3 allow variable number of iterations
| * | | | a880a04 generate obfuscated script and save to another file
| * | | | 194bcf6 randomly rewrite some attributes (e.g., thing.property) with getattr()
| * | | | c32c662 add node rewriter class that updates each node in the syntax tree
| * | | | 7543b1d get script content and parse with ast module
| * | | | 5b58338 use boolean inverse
| * | | | 65ae56a generate booleans from integers
| * | | | 9379436 convert some booleans to AND / OR expressions
| * | | | b4b072e encode booleans by generating numerical comparisons
| * | | | bdffbed add comments
| * | | | b2fda53 use random string indexing to encode some integer constants
| * | | | f287182 use string length to represent some integers
| * | | | 07cd2e9 more todos
| * | | | fbbada5 segment strings into a random number of sections (and join via + or .join())
| * | | | 5c51184 randomly wrap some expressions in lambda functions
| * | | | 2a95677 only round if original value was an int
| * | | | b13fbbb automatically round non-int values
| * | | | a4ceccb avoid divisions by 0
| * | | | 74770e9 convert number to equivalent expression
| * | | | 8458f7b add some TODOs
| * | | | e517fe7 add list of equivalent boolean expressions
| * | | | 8413d89 add list of numerical transforms and iterable types
| * | | | dd69d64 add more test statements
| * | | | a9ed633 add sample program (prime number generator)
| * | | | 07b11ab add imports
| * | | | e3895f9 initial commit
|  / / /  
* | | | 0f01ae9 auto-update information in README
* | | |   bc14df2 Merge pull request #4 from generic-github-user/pythings
|\ \ \ \  
| | | | | *   18b9ea7 (origin/pythings-convert, pythings-convert) Merge branch 'pythings' into pythings-convert
| | | | | |\  
| | |_|_|_|/  
| |/| | | |   
| | | | | * ee936c2 add support for yaml serialization of custom classes
| | | | | * 028b73f add docstring to conversion method ("to")
| | | | | * 6556137 add draft of simple conversion method (needs testing and revision)
| | | | | | * 0e62249 (origin/pythings-srclinks, pythings-srclinks) generate sample output with src link
| | | | | | * 5848867 generate relative path of source file and insert link
| | | | | |/  
| | | | |/|   
| | | | * | bac0cf8 improve documentation for Rect example class
| | |_|/ /  
| |/| | |   
| | | | | * b1c05cd (origin/pythings-diagrams, pythings-diagrams) add methods to generated diagrams
| | | | | * 4f5724d add simple class diagramming capacity
| | | |_|/  
| | |/| |   
| | * | | fb6db1d add/update docstrings
| | |/ /  
| | * / 159b3dc generate markdown documentation for class methods
| |/ /  
| * | aa71cd5 (origin/pythings-decorator, pythings-decorator) improve Rect example
| * | 40b5f48 get methods from decorated classes
| * | 06de76d add helper class for representing functions/methods
| * | a4bab2a allow use of Class as a decorator for normal(-ish) Python classes
| * | 2644ee3 add Attr class for partial attribute annotations
| * | 845ff2d add very simple Rust-like Option type
| * | adbaf2b add Contact class example (unfinished)
| * | 99fd7de add Rect class example
| * | 007d5a4 more docstrings
| * | fb3d430 add some docstrings
| * |   44aaf9e Merge branch 'pythings' into pythings-docs
| |\ \  
| | * | 59f2652 miscellaneous
| | * |   74dc6e7 Merge branch 'pythings-examples' into pythings
| | |\ \  
| | | |/  
| | |/|   
| | | * 09fee96 (origin/pythings-examples, pythings-examples) add some class-level examples for Point
| | | * f03cd50 more Point examples
| | | * 91c75ca add some examples for Point class [example]
| | | * 97f299b add geometric point class example
| | | * c70204a improve class documentation generation
| | | * ab7e097 add Attribute class
| | | * 5ea0e1a add base for class documentation generation method (helpers not yet implemented)
| | | * 77b3e7c add method for converting refinement types to readable string summaries
| | * |   0c6689c Merge branch 'pythings-docs' into pythings
| | |\ \  
| | * | | 74892d6 add some comments
| | | |/  
| | |/|   
| | * | e30db92 add another (more elaborate) class example
| | * | 2ed2ca4 add example of generated class (mainly for testing)
| | * | 14704d0 add helper methods to metaclass (Class)
| | * | 2428a66 add basic metaclass
| | * | 96c1acf add some utility types corresponding to python builtins
| | * | 363cbe8 generate compound types using common comparison operators
| | * | 919338f add pipenv metadata files
| | * | 5f08546 add OperationType (represents an expression in a type specifier for more complex compound types)
| | * | c2a86c1 add refinement type that imbues another type with a predicate
| * | | ba3d524 add summary of desirable features in a metaprogramming mini-framework like this one
| | |/  
| |/|   
| * | ef5185f add TOC, stats, and file tree to project README
| * | b6a4539 add some theoretical considerations
| * | 813e5e7 add more info to README
| |/  
| * 8088e25 add union type that represents any one of two or more distinct types
| * 841d7f7 add imports and type boilerplate
| * bd5d50d add pythings README.md
| | * c0ab375 (origin/geometry, geometry) clean up comments and unused code
| | * 03ebc7e add basic geometry classes (borrowed from FoldZ)
| |/  
|/|   
| | * 62adad8 (origin/wordle-sentence, wordle-sentence) add basic wordle-like game
| |/  
|/|   
* | 8ab3e16 (origin/wordle-variants, origin/unicode-art, wordle-variants, unicode-art) generate summary of directory structure
* | b1aac54 add code statistics (generated by cloc)
|/  
* c0ef098 add other recent projects as submodules
* 13318fd add some test submodules
* f6145c1 add README

```
