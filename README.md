# main

An experimental [monorepo](https://en.wikipedia.org/wiki/Monorepo) for some of
my projects. Most of the existing projects that I've cloned into this
repository will continue to be developed independently in their corresponding
repositories, but I'm hoping to ameliorate some of the code duplication issues
and other maintenance headaches I've run into recently.

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


cloc|github.com/AlDanial/cloc v 1.82  T=0.04 s (2451.8 files/s, 411364.1 lines/s)
--- | ---

Language|files|blank|comment|code
:-------|-------:|-------:|-------:|-------:
HTML|9|999|0|3400
Python|45|823|1127|2600
Markdown|26|291|0|2073
Jupyter Notebook|6|0|2772|980
Bourne Shell|2|77|102|449
C|1|73|92|353
JSON|1|0|0|185
YAML|4|2|0|138
vim script|2|10|13|15
TOML|2|4|1|14
Rust|1|2|2|13
--------|--------|--------|--------|--------
SUM:|99|2281|4109|10220


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
├── epidemic-modelling
│   ├── epidemic-modelling.py
│   ├── LICENSE
│   └── README.md
├── finch
│   └── README.md
├── fractals
│   ├── fractals.ipynb
│   └── README.md
├── generic-github-user
│   ├── docs
│   │   ├── _config.yml
│   │   └── index.md
│   └── README.md
├── graphs
│   ├── completegraph.py
│   ├── giraffe.ipynb
│   ├── giraffe.py
│   ├── graph.py
│   ├── gridgraph.py
│   ├── manual_testing.py
│   ├── node.py
│   ├── randomgraph.py
│   └── randomizer.py
├── keyboard-dynamics
│   ├── keyboard.py
│   ├── LICENSE
│   └── README.md
├── leetcode
│   ├── 1436.py
│   ├── 1528.py
│   ├── 1869.py
│   ├── 39.py
│   └── 796.py
├── obfuscation
│   ├── caterpillar.py
│   └── LICENSE.md
├── packings
│   ├── packings.c
│   ├── packings.py
│   └── README.md
├── physics
│   ├── docs
│   │   ├── _config.yml
│   │   ├── geometry.html
│   │   ├── helpers.html
│   │   ├── index.html
│   │   ├── main.html
│   │   ├── material.html
│   │   ├── object.html
│   │   ├── renderer.html
│   │   ├── scene.html
│   │   └── tensor.html
│   ├── geometry.py
│   ├── helpers.py
│   ├── main.py
│   ├── material.py
│   ├── object.py
│   ├── README.md
│   ├── renderer.py
│   ├── scene.py
│   ├── scripts
│   │   └── build-docs.txt
│   └── tensor.py
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
├── pythings
│   ├── build.py
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── pythings.py
│   ├── README.md
│   └── README.src.md
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
├── quickplot
│   ├── quickplot.py
│   └── requirements.txt
├── README.md
├── README.src.md
├── self-avoiding-walks
│   ├── self-avoiding-walk.ipynb
│   └── self-avoiding-walk.py
├── shelf
│   ├── base.py
│   ├── library.py
│   ├── LICENSE
│   ├── md_template.md
│   ├── note.py
│   ├── README.md
│   ├── session.py
│   ├── shelf.py
│   ├── stringb.py
│   ├── term.py
│   └── utils.py
├── substitutions.yaml
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

32 directories, 120 files

```

## History

```
* 81dab70 (origin/master, master) rebuild README
*   b5aa9c5 Merge branch 'python-experiments'
|\  
| *   d7ccb72 (origin/python-experiments, python-experiments) Add 'python-experiments/' from commit '23fef38879b5506c943e59ca2ab26f54f3c7b4ec'
| |\  
| | * 23fef38 Add sample code snippet (prime number generator)
| | * 322e349 Add experiment summary
| | * d44bc2a Create requirements.txt
| | * 169c1f5 Create symbolic-algebra.ipynb
| | * e95faf7 Testing
| | * e4f24e3 automatically assign default variables/symbols
| | * f8c4e6b Generate magic methods for common math operations
| | * e07648d Add Symbol class
| | * 6831c90 Add operator class-specific string methods
| | * aaac70c Add operator (sub)class
| | * 252fea8 Add string conversion methods
| | * 306a37e Testing dynamic/automated variable creation
| | * 61212b7 Add Expression class
| | * 059d0f7 Create symbolic-algebra.py
| | * 75a92f8 add transform combination testing limit
| | * 36fefdd support application of iterable transform to list (e.g., of words in input string) instead of only text
| | * aacb1f5 add alternative test strings
| | * e7b7551 Track number of transform combinations checked
| | * 4d78d27 Search combinations of varying lengths (1 to max)
| | * fde46d0 Add notebook version of code
| | * e67419b Loop through possible combinations of string transformations and test them on examples
| | * b83b8d1 add names of string transformations
| | * bf339eb add example string mappings
| | * 8e3cc58 Iteratively replace nested type keywords with their corresponding regular expressions
| | * 7eab638 add more test statements/operations
| | * 3950f53 add list of possible string operations
| | * db6dff5 Create .gitignore
| | * 9651aa2 Add function for repeating a value/array a certain number of times along multiple axes
| | * fa4fab0 add function for generating iterated function string
| | * a103acc Create automacro.py
| | * 542f748 Add regexes for common statements and expressions
| | * 74102bb Add test statements
| | * 96314b9 Add imports
| | * 4dd0635 Create README.md
| | * 5798ff2 Create LICENSE.md
| | * 9d5a9ec Create .gitattributes
* |   0e79829 Merge branch 'python-snippets'
|\ \  
| * \   bbbe213 (origin/python-snippets, python-snippets) Add 'python-snippets/' from commit 'a20f7f9b234b69a275ae6828e941c5e9b9d692f3'
| |\ \  
| | |/  
| |/|   
| | * a20f7f9 Add IPython/Jupyter notebook version of code
| | * 8d35040 Add function for generating change given an amount of money as an input
| | * 0811f4c add list of coins/bills and corresponding amounts
| | * 53063c3 Add function for determining the smallest combination of multiples of some given values needed to produce a larger number
| | * 4e548bb add function for making word plural
| | * cbcd32e add function for generating text list from list of items
| | * 521ade9 add title-case function
| | * 3607532 Add nested list flattening function
| | * 3ed717f Add prime-generating function
| | * 56e0766 Create .gitignore
| | * 302a9df Create README.md
| | * e0f62ac Initial commit
* |   e5ff69d Merge branch 'quickplot'
|\ \  
| * \   e5cb7aa (quickplot) Add 'quickplot/' from commit 'f6d19babdcb793315ea41aa53d6e2fa3f9569c1c'
| |\ \  
| | * | f6d19ba Create requirements.txt
| | * | 717a0fb Add colorbar
| | * | da4b275 misc. (plot style, instance attributes, etc.)
| | * | be9f990 Add method for generating contour plots
| | * | 0ab62c7 Add 2D histogram helper method
| | * | 091c446 more docstrings
| | * | 16626c5 add method docstrings
| | * | 5af863a miscellaneous testing code/unused code
| | * | 6ccbce4 tweak (default) plot settings
| | * | 5b79824 Support float value for "annotate" argument
| | * | 44b08bd Test contour plot generation
| | * | f91d4c8 add test plot
| | * | 560a52f add heuristic for automatically repositioning labels to minimize overlap
| | * | 6bf2e6e Add helper Array class (wraps np.ndarray)
| | * | 495c58d Randomly sample points and add annotations showing their coordinates
| | * | 27f8dea Add method for generating Python code (non-dependent on quickplot) that builds equivalent plot
| | * | 539d026 Automatically set axis labels and scales for each spatial dimension (x, y or x, y, z)
| | * | c4246cc Add method for adding coordinate labels/annotations to scatter plots
| | * | c780f35 Add helper methods for generating grids of indices
| | * | 501e8f5 Add function for randomly sampling slices of array
| | * | cc47a25 Adjust scatter plot marker sizes based on number of points in plot if use_density is set to True
| | * | 2ef3f8e Add some todos
| | * | c6bb19b Handle projection argument (2d, 3d, polar)
| | * | 53f14d9 generate plot
| | * | 65996da Process plot settings/options (substitute aliases and values)
| | * | 74bde2e Add heuristic for determining whether log scale should be used for a given axis
| | * | a00532d Add method for generating plot
| | * | 590b89e Add Plot class
| | * | 304d5f2 Add imports
| | * | b584639 Add project summary
| | * | 9fdcd7c Initial commit
| |  /  
* | |   cd2322b (fractals) Add 'fractals/' from commit '6d1b5081d64ae55a4b05bce0fcba1a5bacb23633'
|\ \ \  
| |/ /  
|/| |   
| * | 6d1b508 minor bug fixes
| * | 1867fa4 Add option ("direct") to draw the fractal to pixel grid while generating it
| * | c706288 add random transforms applied to points before moving toward vertex
| * | 58ac046 add option for multiple interpolation ratios (i.e., randomly select what percentage of the distance is travelled from the current location to the selected vertex)
| * | 8cfe054 more testing
| * | 5e53a9d add more transforms/functions for iterative generator
| * | 8e0a005 add render method
| * | 7d17460 add generate method (not yet complete)
| * | 94d75be add iterated function-based fractal class
| * | aedf008 add Attractor (super)class
| * | 540d731 cleanup
| * | 18d4e08 miscellaneous
| * | 6dcdf94 fix random rule generator and add random number of sides
| * | d14c515 add random rule/restriction generation for vertex selection
| * | d3b3478 add SierpinskiTriangle convenience class
| * | 25d40ff add info strings to ChaosGame methods
| * | 3b51f6c add method to divide line into equal segments
| * | e511c16 add "jump" distance parameter
| * | ef14a70 add looping point distance function
| * | 36ad665 add function-based point evaluation
| * | 6a79708 add different point coloring methods
| * | 7b066ef add simple rules limiting vertex selection
| * | eebe672 correct orientation
| * | d03714e add render method
| * | 3e54a41 add generate method
| * | f3a2471 add ChaosGame class
| * | 14222ca add automatic rounding to handle floating point error
| * | 1eafc08 add polygon string method
| * | cea799d add point print method
| * | 73b69ac Add RegularPolygon class
| * | 829cedb Add Polygon class
| * | 82528f9 add move and rotate methods to Line class
| * | 032b547 add Line class
| * | de316ad add 2d rotation about a point
| * | 2ac41ca add move method
| * | e680af9 add point class
| * | 93515f9 add info for Fractal.autozoom method
| * | 735ba4c testing other random parameters
| * | 6671bae add random arguments
| * | 118ab90 reorganize method arguments
| * | 7c9e37d cleanup
| * | b011fbe reorganize fractal generation and rendering system
| * | 00f2e1d refactoring (create generate method)
| * | 3dea437 Add info string for Fractal class (and other tests)
| * | 3686270 add documentation for Fractal.scale method
| * | d6d2a35 add cmap parameter
| * | 085ef99 add display method
| * | 1954999 improve default arguments
| * | 4d9edf7 add automatic extraction of interesting section of fractal (based on variance)
| * | ea8665f add method for evaluating variance of different sections of fractal render
| * | 30cd739 create Fractal class
| * | 75cd945 fix smooth coloring algorithm (scale to maximum iteration values)
| * | 68a5a56 testing smooth coloring function (normalized iteration count)
| * | bcb77fd add main header
| * | 1664f0f add parameter to combine multiple axes into a single image
| * | e68dd6b add global parameter for number of interpolation steps
| * | 349f026 add fractal metadata interpolation
| * | 1196268 re-add .gitignore
| * |   2eeeb28 Merge pull request #1 from generic-github-user/master
| |\ \  
| | * \   f0a1f04 Merge branch 'master' of https://github.com/generic-github-user/fractals
| | |\ \  
| | | * | d60e3b8 ignore checkpoint files
| | | * | 0fe1dfc metadata
| | | * | a395688 Set up basic fractal generation function
| | |  /  
| | * | c60dc9f ignore checkpoint files
| | * | d5f15bb metadata
| | * | e1b8d3e Set up basic fractal generation function
| |/ /  
| * / 20315a0 Initial commit
|  /  
* |   c9ac18e Merge branch 'self-avoiding-walks'
|\ \  
| * \   ab98020 (origin/self-avoiding-walks, self-avoiding-walks) Add 'shelf/' from commit 'c1d707c4638d2c5c1f682a82d4fee4cc286aea43'
| |\ \  
| | * | c1d707c Add (brief) installation section to README
| | * | d8f2e27 Add checkboxes to indicate feature development status
| | * | 732844e Add more features to README
| | * | 8966af8 misc.
| | * | a7b01d6 Add comments
| | * | 346699f Add util function docstrings
| | * | c889065 Include statistics about size of pickled library representation (both compressed and uncompressed)
| | * | 59731e6 Compress backup files
| | * | 32a721a Move object pickling/string conversion to a separate function
| | * | d5783de Add comma separators to printed statistics
| | * | be8494d Add timestamps to export filenames
| | * | 85403aa Include common terms in note exports
| | * | 78500d6 Improve term extraction/filtering
| | * | d0b9172 Store references to terms in note instances
| | * | c0b1ece Fix other dependencies
| | * | bb498ca Add missing import statements
| | * | 2b6981e Move some more functions out of main script
| | * | 0f17161 Move classes to separate scripts for ease of development
| | * | c3ccb21 Allow sorting notes by length (in chracters) or number of words
| | * | db5933b Add store option (if False, the loaded library will be returned instead of assigning to a variable)
| | * | d3244ba Add changed() method
| | * | 224f00a miscellaneous
| | * | 6ae92ad Add command for displaying summary statistics about note library
| | * | 1533de4 Add truncate method
| | * | edbe195 Add regex search command
| | * | d974a5a Store timestamp as String class instance
| | * | 07d9570 Add method for generating text colored with ANSI escape sequences
| | * | 681304a Add command for exploring data saved in backup files
| | * | 8ac4c9d Add helper class with additional string methods
| | * | 9b8f28f Add comments
| | * | 6572cc5 Use note template to generate Markdown export files
| | * | 0240d1e Add command for removing a specified value
| | * | 8c4e314 Add note template for Markdown exports
| | * | be697b9 Fix bug in ranking code
| | * | 759413c Add option for providing numeric arguments to commands
| | * | 8c01b11 Exclude numeric results
| | * | 66a736c Allow weighting by length in characters or words/tokens of each candidate
| | * | d24598b Add method for recalculating rankings based on saved comparisons
| | * | 74f0467 Add note sorting command
| | * | 574bf32 Add note ranking command
| | * | 223612e Add more features to list
| | * | e6cf2cf Add ranking method for interactively sorting notes by a specified attribute
| | * | 9e45fb8 Add library and note class upgrade methods
| | * | 2841536 Add upgrade method that generates missing fields in loaded objects
| | * | f8ea828 Add log parameter
| | * | 91748df Miscellaneous
| | * | 3d6e2cd Minor tweaks to extract_terms() method
| | * | 9b411d8 Allow returning a minimum number of results (i.e., the n closest notes to the target note)
| | * | 96bcd78 Move database file path to Session object
| | * | 5a564b5 Add comments to extract_terms method
| | * | 4c688e6 Add function for extracting common terms and phrases from note library
| | * | 7a5786a Slight backup adjustments
| | * | 39df917 Add Markdown export feature
| | * | fd4828d Add simple backup functionality
| | * | ce161d0 Add feature list (subject to change)
| | * | 62483cc Update gitignore
| | * | c553feb Add comments
| | * | 16c18c6 Add function for interactive command usage/note creation
| | * | cc19a2d Add Tag class
| | * | cd14f3b Add note class methods
| | * | 3d55a57 Add Note class
| | * | 97c6174 Add function for finding similar notes using edit distance metrics/fuzzy string search
| | * | a2cbac0 Add method for adding note instances to libraries
| | * | f89f7c3 Add library saving and loading functions
| | * | 6496b66 Add Library class for storing collections of notes
| | * | 4945aee Add base class for notes, tags, etc.
| | * | 88a085f Add command line argument parser with argparse
| | * | 5ca6668 Add README
| | * | a84cbc9 Add shelf.py (will contain main scripts and command handler)
| | * | ccf74ea Initial commit
| |  /  
| * |   122a13d Add 'self-avoiding-walks/' from commit 'fef229a276c71f444187311be874343f8f800651'
| |\ \  
| | |/  
| |/|   
| | * fef229a add some more notes
| | * e371d20 more terms
| | * 62a88ee add links to other papers and threads regarding Hamiltonian paths/grid graphs
| | * 9ea5be8 add more graph theory terms
| | * 108e901 add more research links/OEIS entries
| | * fad47a4 add option for allowing path to cross edges
| | * 9f2de9a add notes
| | * 2deeb5a add list of relevant search terms/keywords
| | * ca1a668 add some more relevant links
| | * 43ea396 Add option for randomizing tree search
| | * 68984d6 Add depth-first tree search-based path discovery
| | * 065443c add comments
| | * 8d9db36 fix path length calculation
| | * 073caac add more parameters
| | * 93fd54c Add single-step backtracking
| | * ddf2432 Update self-avoiding-walk.ipynb
| | * 3f60f6b add supplementary materials
| | * 96a373e add links to research papers on self-avoiding walks
| | * dc6ddc3 miscellaneous
| | * 5201167 improve visualization and add todos/future research topics
| | * 707c1b3 optimize with Numba
| | * c873064 Add Numba-compatible bounding function
| | * 2ab0a8c Add links to threads about self-avoiding walks
| | * 96a4cfe add notebook that mirrors script
| | * 6c08921 add some graphs
| | * 8af71f2 Add simulation code
| | * cb90fc3 Create .gitignore
| | * 901fa9d generate list of possible steps
| | * fd08d33 Create self-avoiding-walk.py
| | * df3371b Initial commit
* |   d568adc Merge branch 'epidemic-modelling'
|\ \  
| * \   09e55e9 (origin/epidemic-modelling, epidemic-modelling) Add 'epidemic-modelling/' from commit '8794b9f38532e498fc65ec9f3f4ef1d0bf39e744'
| |\ \  
| | |/  
| |/|   
| | * 8794b9f Add function for updating Person class instance
| | * 3ff9ef5 Add method for simulating virus test (with optional inaccuracy)
| | * ade18fc Add Person class
| | * 7e2cecc Add Population class
| | * b621561 Add History class
| | * 6b35fc9 Create README.md
| | * ec86c67 Add helper functions
| | * 7b27941 Add string conversion methods
| | * 2397043 Add Pathogen class
| | * c8539af Create epidemic-modelling.py
| | * 616c49a Initial commit
* |   9fbb532 (origin/physics, physics) Add 'physics/' from commit '59e45d7f25b0ad89938a37317695b7f7428c8b68'
|\ \  
| |/  
|/|   
| *   59e45d7 Merge branch 'master' of https://github.com/generic-github-user/ascii-physics-sim
| |\  
| | * af2e589 Set theme jekyll-theme-cayman
| * | 6d13213 add command for building documentation with pdoc
| |/  
| * 5d66559 build documentation
| * 95db5a9 Create README.md
| * 3a1698e add rotation and angular velocity tracking to object class
| * 4ff543e move a few helper classes to a separate file
| * f985adf cleanup
| * 23a3949 Split code into multiple files to make development go smoother
| * b25b5b8 remove unused Vec class code
| * 8a3b05b more documentation
| * 7ed8107 document Object class
| * b2ff6e5 Material class documentation
| * 95dd809 Add some documentation to Renderer class (via https://pdoc.dev/)
| * 9432df7 add 4D helper class, might remain unused
| * 2d6531b add some comments
| * 1228562 ignore compiled python files
| * bd1ee5d only get rtype once
| * 1c0a248 property storage placeholder classes
| * 16644ba remove unused scalar code
| * 05d1c71 miscellanous, pt. II
| * 38c9409 add motion delta handling
| * 71770c9 updated simulation code to handle new renderer
| * 03d3979 update default renderer settings
| * aedc313 recursive self-call in rendering function (used with python canvas until I can find a workaround)
| * cf58193 placeholders for opengl and cairo graphics (planning to implement in future)
| * 28e57cc add canvas renderer (can currently only handle circles)
| * 353b507 add line (ASCII) renderer
| * a450729 method for looking up ASCII characters corresponding to incline angles
| * 23d274f new frame rendering function
| * ce12913 material class updates
| * 91829ac more materials properties
| * 8162a90 add output concatenation method
| * 19d7819 initialization code for new (tkinter) canvas based renderer
| * 256c7ac miscellaneous
| * a233646 clean out old tests
| * aba91cb create Name class (not entirely sure yet if this will be used)
| * 2b5ffe4 unused code
| * 81fb3f4 update random scene generation function
| * 8f57703 add clear parameter to randomize() method
| * c48dcd0 add more material properties
| * 62bba49 more TODOs
| * 294d6b1 create gitignore
| * fbd5e32 add Angle class
| * 1526692 add method to calculate angles of tangent lines around circle perimeter (still eneds some debugging)
| * 80572b9 default for geometry parts should be a list
| * 12440b9 testing python opengl bindings per https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/
| * cef00b5 tests/todos
| * aaea382 reorganize rendering functions
| * dfc830c GlyphSet helper class
| * 92ceed9 just in case
| * cea2d5d Cleanup
| * 2db9988 Add camera class
| * c9af190 Add world and cluster classes
| * 38d3414 multiple small updates/fixes
| * eb6f2d9 Add simulation and renderer placeholder classes
| * 848762d Add matter class
| * 3d6a5fd Add material class
| * cea2d2f Add circle class
| * 2ba9137 Add Polygon class
| * 10cc8c0 Add specialized subclasses of Geometry
| * fef43d8 Add Geometry class
| * 445cede fix gravity (sim was using the old .x/.y notation)
| * 8c15a89 more tests
| * 074f9ed decommission old classes and create aliases for new Tensor class
| * cbe9dd9 add random scene generator
| * 3922def add unit class
| * 0d172b1 clean out some obsolete math functions
| * 3a4db46 Add general tensor class + begin transitioning to NumPy arrays
| * 4e3a800 add more tests
| * 1e3126e add gravity function (currently unused)
| * 781e589 some TODOs
| * bcd4169 add more operations to scalar class
| * 48e92d1 Non-reductive distance function
| * be3e739 Default mass scalar for objects
| * 819d278 Clean up math operation functions
| * 148a842 Additional scene properties
| * 34b148b Vec class distance function
| * d78659c add position vector to object class (with backwards-compatible x & y properties)
| * 22625ea add printing functions to Vec class
| * 89a56dd add square and reduce (sum) functions to Vec class
| * 76527af each utility function (Vec class)
| * 46bb26b add some basic math functions to vector class
| * 962a6ef add clone function to vector class
| * 148b51a add scalar class
| * 2bab5d6 use time in position change calculation
| * d584521 handle edge wrapping
| * c99287f add scene size handling
| * 7800ef1 add unit dict to scene class
| * 7f47595 clean up render testing code
| * 32776ef start with random velocity
| * ae15d1e update rendering function
| * 5301e39 add velocity property to object class
| * f999721 add physics stepping function
| * b589acd create vector class
| * 7c0d750 add simple renderer
| * 109dda7 main scene/object classes
| * 658d809 Initial commit
| * 9308577 (refs/stash) WIP on master: 79a8246 Merge branch 'packings'
|/| 
| * 6d17452 index on master: 79a8246 Merge branch 'packings'
|/  
| * 59d62c0 (HEAD -> meta, origin/meta) reflow branch list
| * 111afe0 add summaries of recent branches
| * 37a73d4 extract commands corresponding to template strings (moved to substitutions.yaml)
|/  
*   79a8246 Merge branch 'packings'
|\  
| *   f1932de (origin/packings-rust, origin/packings, packings-rust, packings) Merge remote-tracking branch 'packings/main' into packings
| |\  
| | * 9c38413 move files to subdirectory to allow merge with monorepo
| | * 58292da Refactor add_center
| | * ba9e195 Add README
| | * 07e0436 change some return types, etc
| | * b6180ba Add function for placing center block
| | * 63035a3 Add missing compute counters
| | * 61e06f0 Add global list of allocated polyominoes
| | * 33dda73 Add polyomino optimization function
| | * 0012982 cleanup
| | * 40dcb04 minor refactoring
| | * f1177db Add templates for other functions
| | * a1d2330 add node and graph structs
| | * da4d468 Generate and display sample polyominoes
| | * 74e6b8d update polyomino indexing scheme
| | * 7190a04 miscellaneous
| | * c9db171 Add main function
| | * e1af71e Add function for randomly removing blocks
| | * 0840c72 Add helper function for removing blocks
| | * b2931b7 Add function for adding blocks to polyomino (while maintaining both the geometric data structure and index)
| | * e037be9 Add function for finding available memory to store pointer to new index (vector) in
| | * 0071f44 add polyomino equivalence function
| | * ae8b76c Add randomized function for expanding polyominoes
| | * bbb3d8d Add function for computing perimeter of polyomino
| | * 9366309 Add function for counting adjacent blocks
| | * 4737686 misc
| | * fa74741 Add function for checking polyomino equivalence up to translation
| | * 33d8129 Add function for generating and counting polyominoes (in place)
| | * 36f893f Add function for getting pointers to all candidate cells in a polyomino representation
| | * 3d33edf Add function for testing whether 2 (aligned) polyominoes overlap
| | * 22d781b Add helper functions
| | * f246748 Add functions for releasing dynamically allocated memory (used to store arrays and polyominoes)
| | * b59d30b misc
| | * d54b2ce Add polyomino printing function
| | * 56ab5c9 Add function for safely getting pointer to a block from a polyomino
| | * e3b44b9 Add polyomino struct and constructor
| | * cb12b75 Add function for creating arrays
| | * 06f770b add TODOs
| | * 52de5b6 Add function for populating array with value
| | * 0e82000 Add ANSI escape codes for printing colored text
| | * 7e4c2a5 add vector and array structs
| | * dd5fcc5 Add C-based version of system
| | * c533d05 refactoring
| | * 79a95b4 Add method for removing squares from polyominoes
| | * 9eaa77e Add method for building larger polyominos by adding squares to edges
| | * f71322b Add str method to Polyomino class
| | * c2bf715 Add method for expanding polyomino representation to correct size
| | * 5fac011 Add Polyomino class
| | * c6c3b2d Add class for representing collections of polyominoes
| | * a48bce8 add packings.py
| | * f49d0c1 Initial commit
* |   c203f54 Merge branch 'meta'
|\ \  
| |/  
|/|   
| * 3217348 add labels to other projects in this monorepo
| * b5b027a add list of labels/topics to some projects
| * 6763501 add language information for some projects
| * f558afc add diagram of repository branching history
| * 2200f35 minor reorganization (added location indicators to some items)
| * e0f70c4 add descriptions of some status labels
| * 56384bf add info about some external repositories
| * bf2f053 add metadata for other projects
| * 224ffa9 add information about some projects' statuses
| * b66eca8 update formatting
| * a2166a6 add branch summaries
* | f798b6e update stats (again
* |   21fde43 Merge remote-tracking branch 'graphs/graphs'
|\ \  
| * | 228ea98 (origin/graphs, graphs) fix merge prep from last commit (on /giraffe)
| * | 343af69 move Randomizer class
| * | ee2e5d3 more cleanup and restructuring
| * | 59ace1a more cleanup
| * | c3cae9d Extract GridGraph and Node classes and move manual tests to a new script
| * | f104f12 move graph classes out of notebook
| * | 2aacd20 Push all current changes to new branch
| * | 41b74e9 Add method for sampling from distribution
| * | 49027ae add Randomizer class
| * | b5df399 Allow returning of grouped nodes/subnodes generated by add_node method using return_node='inner'
| * | 75a4c3a Add option to use edge weights in adjacency matrix
| * | dfdf267 Add parameters for specifying which node to return
| * | 1f310b0 add dictionary of default edge drawing parameters
| * | 28e4896 add more dependencies
| * | 6cfe5a0 Add parameters for weighted edges in RandomGraph
| * | 5c369c9 Add function for generating an adjacency matrix for a given graph
| * | c9d66a4 Add subclass for creating complete graphs
| * | be10448 Split Graph class methods across multiple cells
| * | 6bf7a1a Handle errors sometimes thrown when drawing graph edges
| * | 10a4055 Add method for merging two graphs' nodes
| * | 205ab95 add subclass for generating simple random graphs
| * | d7c7a0f Add metadata properties to node in constructor method
| * | 7ddc2a2 Pass metadata and other parameters to add_node and Node.init calls
| * | 226fdb9 misc
| * | e6ce8a6 Use updated Graph.find() method parameter syntax
| * | a7dcf53 Iteratively generate sequence and add nodes to the graph
| * | f0fee45 miscellaneous testing code
| * | d2bedb0 add node and edge visualization parameters (these are passed to pyvis)
| * | a72c8ba Add improved node coloring
| * | 4b850f7 Add example with sequences of arithmetic operations iterated on random inputs
| * | 290d1e0 delegate node initialization to add_nodes method
| * | 2b180ce Add example visualizing relationships between subsequences of a string
| * | b221f61 misc
| * | 87420c2 Allow searching for nodes matching one or more arbitrary conditions using find() function
| * | efdf97c Add node class method for adding another node that shares a group with the first
| * | 85a14e9 Get text nodes from a path along the corpus graph
| * | 75565d5 Add method for finding adjacent nodes to a given node (ones which are grouped with the target node)
| * | b5fce3f Testing
| * | 6830ca9 Pass kwargs to single-node method
| * | b1150b6 Add convenience methods/builtins
| * | c8ff4fb Add methods for randomly selecting nodes from a graph object
| * | ad34e36 Sample non-overlapping sets of sentences from text
| * | 88b2d4a Create giraffe.ipynb
| * | 47db551 Miscellaneous testing
| * | 759e849 Create a test graph and generate visualization
| * | e060960 Update class method names
| * | efa4b14 Calculate degree of node
| * | d871f40 add Node class
| * | 5e33396 Add method for adding multiple nodes from an iterable at once
| * | 3a8b19f Accept primitive arguments to Graph.add_node()
| * | 6efdac5 Allow node object as parameter to Graph.add_node() method
| * | 3602df1 Add method for adding a node to a graph given a list containing the node's value and other nodes it groups
| * | 44e39fb Add node search function
| * | f90cc0d Visualize graph edges
| * | 7fcae2c Update .gitignore
| * | 5c3de0d Add function for visualizing nodes with pyvis
| * | 409699a Add graph class
| * | f5f79a2 Sample sentences from the text corpus and calculate similarity values
| * | 482dd0e Load and process text corpus
| * | e43c4a4 Create giraffe.py
| * | 8fc0278 Create .gitignore
|  /  
* |   355b795 Merge remote-tracking branch 'keyboard-dyamics/main'
|\ \  
| * | 70c22af restructure to allow merging with main repo
| * | d40a3fa Scale key location coordinates by keyboard length parameter
| * | 56fe8fb Move code for computing cost of moving to new position to a dedicated function
| * | a267602 Add more testing strings
| * | 09bc3b5 Add other common characters/keys
| * | f67da44 Add parameter for setting random seed
| * | 2a12769 Add scatter plot (#1)
| * | 3090b99 Move random string generation code to a new function
| * | 951d5f8 Generate grouped bar plot displaying different metrics for each test string
| * | caf5143 Generate histogram visualizing distributions of typing difficulty scores
| * | 8ab38f5 Add function for randomly generating some strings and calculating corresponding scores
| * | a76db9d Add README
| * | d050a0a Add simplistic logging
| * | d0d327c Add method for calculating typing cost assuming each character is typed using the nearest available pointer/finger
| * | dd8de9e Add function for calculating "effort" needed to type a given string
| * | 973dc46 ad some test strings
| * | 37250bb Add querty keyboard layout as array of characters
| * | c28b6c3 Add keyboard.py and main imports
| * | 2228ef7 Initial commit
|  /  
* | eb37c98 update stats
* |   baf623b Merge branch 'leetcode'
|\ \  
| |/  
|/|   
| | * e123491 (origin/pythings-docs, pythings-docs) reflow README.md paragraphs/lists
| | | * 187577b (origin/lc-comments, lc-comments) more comments
| | | * 3325b35 more misc comments
| | | * 2d78667 add comments to spiral matrix solution
| | | * da4c7af add comments to checkZeroOnes
| | | * eb715df (origin/leetcode, leetcode) add new solutions from 08-28
| | | * e089b51 add solution for efficient search of partially sorted matrix
| | |/  
| |/|   
| * | 28728c8 more LC solutions
| * | 3f2ed2b add two more solutions from today
| * | 20e00db add solution for "shuffle string"
| | | * d3c9469 (origin/py-obf-cli, py-obf-cli) allow input file argument to obfuscator
| | | * 7968d3f use pipenv
| | | * 0b6257b (origin/python-obfuscator, python-obfuscator) move old python obfuscator to designated subdirectory
| | | * b93eec0 more cleanup and reorganization
| | | * b3c063a (origin/obfuscation, obfuscation) reflow comments and docstrings for vim
| | | * af06cfa extract TODOs
| |_|/  
|/| |   
* | | 3b30833 reorganize imported files and rebuild
* | |   b679244 Merge remote-tracking branch 'obfuscation/master'
|\ \ \  
| |/ /  
|/| |   
| * | 6e6a09b Add .deepsource.toml
| * | 5f8657a sort candidate keywords by length and combine into phrases/identifiers
| * | 3ced50b generate some random strings from keyword list
| * | f91e529 add function for generating identifiers from keyword list
| * | 2d3d055 add context parameter to other nodes
| * | 931e507 add some more preset keywords
| * | 94af7db add docstring
| * | ba3ec96 todo
| * | 2fd468f add function for converting an AST node to a string representation (for the network visualization)
| * | 16b1021 include context (ctx) parameter when generating AST nodes
| * | 8c01f65 add function for random string capitalization
| * | 30fe5be fix bug causing incorrect string encoding when the same pattern appeared more than once in the string
| * | 82a2feb add inverse trig functions (and corresponding domains/acceptable input ranges)
| * | d0e239d generate additional keywords from own source code
| * | e074cd2 extract keywords from builtin functions
| * | f512740 add list of terms to generate filler strings with
| * | edd38be add function to check strings for numbers
| * | 291eb7f add function to remove basic punctuation from a string
| * | 9cfbf3f misc
| * | e911d0f add function for splitting camel case identifiers
| * | 306ba49 use normal characters (ASCII letters + numbers) for string generation
| * | cedcec0 code reformatter adjustments
| * | 96035e6 todos
| * | 1d6b74c improve repairing of statements split between multiple lines
| * | d9722ce add comments
| * | caa7c16 miscellaneous
| * | c0f22af add trigonometric function-based encoding of numerical expressions
| * | 89938d8 add license
| * | 296cd06 store arity (number of arguments) of transform functions
| * | bc0f4f1 allow iterable parameter to randomly select number of characters to generate
| * | a32511a move function
| * | 0c37aa1 update line ending with correct character (was previously always "=")
| * | 462182d more TODOs
| * | afcb905 allow lambda wrapping for types other than int
| * | 97bda16 add other node descriptors
| * | 8e9ef8d misc
| * | a6a1efc add some descriptors to convert AST nodes to PyVis network nodes
| * | faa352a add docstring
| * | 5030aaa add more comments
| * | 0b51680 add comments
| * | 19db2b3 miscellaneous
| * | 669ee7f chain lists/tuples together after segmenting
| * | 8288d78 use addition to concatenate some strings
| * | 01b8a7e add method to get the first existing property of an object from a list
| * | aefee78 add function for evaluating attribute string (e.g., "property.detail")
| * | b3c9a6a add PyVis Network subclass for saving HTML without opening in the browser
| * | fb07d3e rewrite imports (and corresponding references) with aliased names
| * | 18cc48a replace repeating patterns in some strings with expressions representing the pattern
| * | 0bad3c4 misc
| * | 931ae31 limit size of generated strings
| * | 0affab7 fix broken line endings in certain variable assignments
| * | ec84fc9 add function for generating a small syntax tree with a source code template
| * | 4917cb5 add charset parameter
| * | 78ba06b add boolean inequalities
| * | 53bd64d add methods for detecting repeating substrings/patterns in strings
| * | 1773acd add more test statements
| * | 113dcf8 encode some strings with generated replacements
| * | 1073d51 add boolean equality conditions
| * | e649777 handle unhashable types
| * | 986ff05 traverse child nodes
| * | bf5387a randomly subdivide lists and tuples
| * | d3b8e3c determine number of segments from string length
| * | a784cb3 allow variable number of iterations
| * | a880a04 generate obfuscated script and save to another file
| * | 194bcf6 randomly rewrite some attributes (e.g., thing.property) with getattr()
| * | c32c662 add node rewriter class that updates each node in the syntax tree
| * | 7543b1d get script content and parse with ast module
| * | 5b58338 use boolean inverse
| * | 65ae56a generate booleans from integers
| * | 9379436 convert some booleans to AND / OR expressions
| * | b4b072e encode booleans by generating numerical comparisons
| * | bdffbed add comments
| * | b2fda53 use random string indexing to encode some integer constants
| * | f287182 use string length to represent some integers
| * | 07cd2e9 more todos
| * | fbbada5 segment strings into a random number of sections (and join via + or .join())
| * | 5c51184 randomly wrap some expressions in lambda functions
| * | 2a95677 only round if original value was an int
| * | b13fbbb automatically round non-int values
| * | a4ceccb avoid divisions by 0
| * | 74770e9 convert number to equivalent expression
| * | 8458f7b add some TODOs
| * | e517fe7 add list of equivalent boolean expressions
| * | 8413d89 add list of numerical transforms and iterable types
| * | dd69d64 add more test statements
| * | a9ed633 add sample program (prime number generator)
| * | 07b11ab add imports
| * | e3895f9 initial commit
|  /  
* | 0f01ae9 auto-update information in README
* |   bc14df2 Merge pull request #4 from generic-github-user/pythings
|\ \  
| | | *   ba50b31 (origin/pythings, pythings) Merge branch 'pythings-docgen' into pythings
| | | |\  
| | | | * 7ae5e7f (origin/pythings-docgen, pythings-docgen) add option for hiding sections without content
| | | * |   a2bde6f Merge branch 'pythings-docs' into pythings
| | | |\ \  
| | | |/ /  
| | |/| |   
| | * | | 0d8beb3 update "Branches" section formatting
| | * | | bc0be55 add rest of pythings-related branches
| | * | | 66f19a0 wrap long lines in source when generating README (some sections are painful to reflow in vim)
| | * | | 425a393 add summaries of most pythings sub-branches
| | | * | f3a2e31 (origin/pythings-restructuring, pythings-restructuring) move Animal and File examples
| | | * | 0da9689 move some examples to separate files
| | | * | cd4c463 move custom type classes to a separate module
| | |/ /  
| | * | c7c5d36 add mermaid diagram summarizing organization of project internals
| | * | ac7026c add some installation and usage information
| | * | f44982c add summary of features
| | * |   ba8c2c0 Merge branch 'pythings-comments' into pythings-docs
| | |\ \  
| | | * | 7f97e98 (origin/pythings-comments, pythings-comments) add some comments
| | * | | 3abd74a add more docstrings
| | * | | 84c7a90 add docstrings to Type class
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
