# main

An experimental [monorepo](https://en.wikipedia.org/wiki/Monorepo) for some of
my projects. Most of the existing projects that I've cloned into this
repository will continue to be developed independently in their corresponding
repositories, but I'm hoping to ameliorate some of the code duplication issues
and other maintenance headaches I've run into recently.

## Branches

- `geometry`: helper classes for geometry in Python that I've been copy-pasting around periodically for the last 18 months or so (and actually one of the main reasons for creating this monorepo)
- `leetcode`: some of my solutions to programming problems from [leetcode.com](https://leetcode.com/)
- `meta`: information about this repository itself (code statistics, file listings, issue metadata, etc.)
- `obfuscation`: code obfuscation tools repurposed from an old repository of mine
- `pythings`: useful tools and scripts for the boring parts of Python (mainly writing tests, documentation, etc.)

## Statistics


cloc|github.com/AlDanial/cloc v 1.82  T=0.02 s (2931.6 files/s, 362132.0 lines/s)
--- | ---

Language|files|blank|comment|code
:-------|-------:|-------:|-------:|-------:
Markdown|19|282|0|1351
Python|21|305|450|1279
Bourne Shell|2|77|102|449
C|1|73|92|353
Jupyter Notebook|1|0|1043|293
JSON|1|0|0|185
YAML|3|2|0|137
vim script|2|10|13|15
TOML|2|4|1|14
Rust|1|2|2|13
--------|--------|--------|--------|--------
SUM:|53|755|1703|4089


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
├── README.md
├── README.src.md
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

22 directories, 68 files

```

## History

```
*   4db490e (refs/stash) WIP on meta: 3217348 add labels to other projects in this monorepo
|\  
| * 51f8f65 index on meta: 3217348 add labels to other projects in this monorepo
|/  
| *   79a8246 (HEAD -> meta, origin/meta, origin/master, master) Merge branch 'packings'
| |\  
| | *   f1932de (origin/packings-rust, origin/packings, packings-rust, packings) Merge remote-tracking branch 'packings/main' into packings
| | |\  
| | | * 9c38413 move files to subdirectory to allow merge with monorepo
| | | * 58292da Refactor add_center
| | | * ba9e195 Add README
| | | * 07e0436 change some return types, etc
| | | * b6180ba Add function for placing center block
| | | * 63035a3 Add missing compute counters
| | | * 61e06f0 Add global list of allocated polyominoes
| | | * 33dda73 Add polyomino optimization function
| | | * 0012982 cleanup
| | | * 40dcb04 minor refactoring
| | | * f1177db Add templates for other functions
| | | * a1d2330 add node and graph structs
| | | * da4d468 Generate and display sample polyominoes
| | | * 74e6b8d update polyomino indexing scheme
| | | * 7190a04 miscellaneous
| | | * c9db171 Add main function
| | | * e1af71e Add function for randomly removing blocks
| | | * 0840c72 Add helper function for removing blocks
| | | * b2931b7 Add function for adding blocks to polyomino (while maintaining both the geometric data structure and index)
| | | * e037be9 Add function for finding available memory to store pointer to new index (vector) in
| | | * 0071f44 add polyomino equivalence function
| | | * ae8b76c Add randomized function for expanding polyominoes
| | | * bbb3d8d Add function for computing perimeter of polyomino
| | | * 9366309 Add function for counting adjacent blocks
| | | * 4737686 misc
| | | * fa74741 Add function for checking polyomino equivalence up to translation
| | | * 33d8129 Add function for generating and counting polyominoes (in place)
| | | * 36f893f Add function for getting pointers to all candidate cells in a polyomino representation
| | | * 3d33edf Add function for testing whether 2 (aligned) polyominoes overlap
| | | * 22d781b Add helper functions
| | | * f246748 Add functions for releasing dynamically allocated memory (used to store arrays and polyominoes)
| | | * b59d30b misc
| | | * d54b2ce Add polyomino printing function
| | | * 56ab5c9 Add function for safely getting pointer to a block from a polyomino
| | | * e3b44b9 Add polyomino struct and constructor
| | | * cb12b75 Add function for creating arrays
| | | * 06f770b add TODOs
| | | * 52de5b6 Add function for populating array with value
| | | * 0e82000 Add ANSI escape codes for printing colored text
| | | * 7e4c2a5 add vector and array structs
| | | * dd5fcc5 Add C-based version of system
| | | * c533d05 refactoring
| | | * 79a95b4 Add method for removing squares from polyominoes
| | | * 9eaa77e Add method for building larger polyominos by adding squares to edges
| | | * f71322b Add str method to Polyomino class
| | | * c2bf715 Add method for expanding polyomino representation to correct size
| | | * 5fac011 Add Polyomino class
| | | * c6c3b2d Add class for representing collections of polyominoes
| | | * a48bce8 add packings.py
| | | * f49d0c1 Initial commit
| * |   c203f54 Merge branch 'meta'
| |\ \  
| |/ /  
|/| /   
| |/    
* | 3217348 add labels to other projects in this monorepo
* | b5b027a add list of labels/topics to some projects
* | 6763501 add language information for some projects
* | f558afc add diagram of repository branching history
* | 2200f35 minor reorganization (added location indicators to some items)
* | e0f70c4 add descriptions of some status labels
* | 56384bf add info about some external repositories
* | bf2f053 add metadata for other projects
* | 224ffa9 add information about some projects' statuses
* | b66eca8 update formatting
* | a2166a6 add branch summaries
| * f798b6e update stats (again
| *   21fde43 Merge remote-tracking branch 'graphs/graphs'
| |\  
| | * 228ea98 (graphs) fix merge prep from last commit (on /giraffe)
| | * 343af69 move Randomizer class
| | * ee2e5d3 more cleanup and restructuring
| | * 59ace1a more cleanup
| | * c3cae9d Extract GridGraph and Node classes and move manual tests to a new script
| | * f104f12 move graph classes out of notebook
| | * 2aacd20 Push all current changes to new branch
| | * 41b74e9 Add method for sampling from distribution
| | * 49027ae add Randomizer class
| | * b5df399 Allow returning of grouped nodes/subnodes generated by add_node method using return_node='inner'
| | * 75a4c3a Add option to use edge weights in adjacency matrix
| | * dfdf267 Add parameters for specifying which node to return
| | * 1f310b0 add dictionary of default edge drawing parameters
| | * 28e4896 add more dependencies
| | * 6cfe5a0 Add parameters for weighted edges in RandomGraph
| | * 5c369c9 Add function for generating an adjacency matrix for a given graph
| | * c9d66a4 Add subclass for creating complete graphs
| | * be10448 Split Graph class methods across multiple cells
| | * 6bf7a1a Handle errors sometimes thrown when drawing graph edges
| | * 10a4055 Add method for merging two graphs' nodes
| | * 205ab95 add subclass for generating simple random graphs
| | * d7c7a0f Add metadata properties to node in constructor method
| | * 7ddc2a2 Pass metadata and other parameters to add_node and Node.init calls
| | * 226fdb9 misc
| | * e6ce8a6 Use updated Graph.find() method parameter syntax
| | * a7dcf53 Iteratively generate sequence and add nodes to the graph
| | * f0fee45 miscellaneous testing code
| | * d2bedb0 add node and edge visualization parameters (these are passed to pyvis)
| | * a72c8ba Add improved node coloring
| | * 4b850f7 Add example with sequences of arithmetic operations iterated on random inputs
| | * 290d1e0 delegate node initialization to add_nodes method
| | * 2b180ce Add example visualizing relationships between subsequences of a string
| | * b221f61 misc
| | * 87420c2 Allow searching for nodes matching one or more arbitrary conditions using find() function
| | * efdf97c Add node class method for adding another node that shares a group with the first
| | * 85a14e9 Get text nodes from a path along the corpus graph
| | * 75565d5 Add method for finding adjacent nodes to a given node (ones which are grouped with the target node)
| | * b5fce3f Testing
| | * 6830ca9 Pass kwargs to single-node method
| | * b1150b6 Add convenience methods/builtins
| | * c8ff4fb Add methods for randomly selecting nodes from a graph object
| | * ad34e36 Sample non-overlapping sets of sentences from text
| | * 88b2d4a Create giraffe.ipynb
| | * 47db551 Miscellaneous testing
| | * 759e849 Create a test graph and generate visualization
| | * e060960 Update class method names
| | * efa4b14 Calculate degree of node
| | * d871f40 add Node class
| | * 5e33396 Add method for adding multiple nodes from an iterable at once
| | * 3a8b19f Accept primitive arguments to Graph.add_node()
| | * 6efdac5 Allow node object as parameter to Graph.add_node() method
| | * 3602df1 Add method for adding a node to a graph given a list containing the node's value and other nodes it groups
| | * 44e39fb Add node search function
| | * f90cc0d Visualize graph edges
| | * 7fcae2c Update .gitignore
| | * 5c3de0d Add function for visualizing nodes with pyvis
| | * 409699a Add graph class
| | * f5f79a2 Sample sentences from the text corpus and calculate similarity values
| | * 482dd0e Load and process text corpus
| | * e43c4a4 Create giraffe.py
| | * 8fc0278 Create .gitignore
| *   355b795 Merge remote-tracking branch 'keyboard-dyamics/main'
| |\  
| | * 70c22af restructure to allow merging with main repo
| | * d40a3fa Scale key location coordinates by keyboard length parameter
| | * 56fe8fb Move code for computing cost of moving to new position to a dedicated function
| | * a267602 Add more testing strings
| | * 09bc3b5 Add other common characters/keys
| | * f67da44 Add parameter for setting random seed
| | * 2a12769 Add scatter plot (#1)
| | * 3090b99 Move random string generation code to a new function
| | * 951d5f8 Generate grouped bar plot displaying different metrics for each test string
| | * caf5143 Generate histogram visualizing distributions of typing difficulty scores
| | * 8ab38f5 Add function for randomly generating some strings and calculating corresponding scores
| | * a76db9d Add README
| | * d050a0a Add simplistic logging
| | * d0d327c Add method for calculating typing cost assuming each character is typed using the nearest available pointer/finger
| | * dd8de9e Add function for calculating "effort" needed to type a given string
| | * 973dc46 ad some test strings
| | * 37250bb Add querty keyboard layout as array of characters
| | * c28b6c3 Add keyboard.py and main imports
| | * 2228ef7 Initial commit
| * eb37c98 update stats
| * baf623b Merge branch 'leetcode'
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
