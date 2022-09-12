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

Compound forms can be declared either through the use of square brackets (`[`
and `]`) or indentation. A bracket-delimited form should either be empty or
contain a sequence of space-separated forms ("subforms"). Note that per the
earlier definition, these may be simple expressions such as variables/symbols,
strings, and numeric literals.

Spaces must be used for indentation; identation by 4 spaces is recommended,
though other widths can be used as long as consistency is maintained. Each line
following a contrived "dedent" token is interpreted as a subform. The "root"
form (generally the first line of an indentation-nested form, which precedes
indented lines) takes the place of the first subform. thus, the two forms shown
below are equivalent:

```
[a b c]
```

```
a
		b
		c
```
