# transpiler

An experimental implementation of Finch that transpiles source code to other
programming languages (namely, Python and Rust). The initial implementation is
being written in Python (using the [Lark](https://github.com/lark-parser/lark)
parsing toolkit), but the eventual goal is to support enough of Finch's
features to
[bootstrap](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)) a
self-hosting parser and compiler.

## Overview

A brief summary of the transpilation process (some of these steps may overlap):

- Parse the raw source into a plain [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (essentially a hierarchy of lightweight wrappers around the `Tree` and `Token` classes from Lark)
- Transform the AST into a more convenient representation with structured information about expressions and statements in the source program
- Perform various reductions and optimizations on the source tree, potentially evaluating components of it to determine the most suitable transformations
- Generate equivalent (terms and conditions may apply) code in the target language; generally, each type of source node must specify how its contents should be (recursively) translated and joined with other nodes' translations
- Compile and/or execute the generated code
