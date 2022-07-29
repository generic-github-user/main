# transpiler

An experimental implementation of Finch that transpiles source code to other
programming languages (namely, Python and Rust). The initial implementation is
being written in Python (using the [Lark](https://github.com/lark-parser/lark)
parsing toolkit), but the eventual goal is to support enough of Finch's
features to
[bootstrap](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)) a
self-hosting parser and compiler.
