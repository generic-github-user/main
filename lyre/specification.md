# lyre

This is a draft specification of the lyre programming language, meant to aid in
its design and development (particularly the reference implementation, which is
currently being written in Rust). Further changes should be anticipated,
including significant and backwards-incompatible alterations to the language's
syntax, semantics, and standard library functions.

A lyre program is a (possibly empty) series of *forms*. These can be either
simple forms or compound forms. Simple forms are basic expressions, falling
into one of the following categories:

- string literal
- integer literal
- floating-point number literal
- symbol

Compound forms are lists of simple forms and other compound forms (and possibly
both), though they may be empty. As in the Lisp programming language, this
definition makes them functionally equivalent to trees by nesting expressions
to an arbitrary depth.
