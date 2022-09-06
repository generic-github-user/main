# lyre

lyre is a weird, wonderful little language that takes heavy inspiration from
lisp, most notably in its minimalism and homoiconicity. It also draws on Rust,
Julia, Python, Nu, and Bash, among a handful of other languages. My main goal
was to create a language that is as elegant, expressive, and generic as lisp
but less verbose and easier to write code that is stylistically compatible with
multiple programming paradigms.

## Usage

### Introduction

lyre's syntax closely resembles that of Common Lisp, with a couple notable
differences:

- Square brackets (`[]`) are used instead of parentheses
- Indented blocks are parsed as nested forms

lyre programs consist exclusively of nested list-like expressions (often
referred to as "forms" in this guide), forming a tree structure. Syntactically,
these are space-separated expressions (either literals like numbers and
strings, or other forms) grouped with square brackets and indentation.
