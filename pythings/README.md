# pythings

This is a small module resurrecting some old experiments of mine taking
advantage of Python's highly dynamic runtime, namely to bridge the gaps between
code written for functionality, testing, and documentation. Python's semantics
enable quite extensive metaprogramming capabilities without necessarily
resorting to syntactic macros; the language also has many tools that permit us
to extract useful information embedded in code without needing a separate
parsing tool.

The core feature this tool was designed around is the idea of a refinement
type, which combines an abstract type with a predicate function that dictates
the values an element of that type may have. More specifically, it is often
useful to describe valid arguments to a function, data members of a class/type,
possible function outputs (return values), etc. In practice, I often find
myself creating partial class templates or makeshift components that check
input types and generate documentation from type signatures and other
annotations.
