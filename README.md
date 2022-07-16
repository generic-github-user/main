# grammars

A very fast, very general tool for constructing and using grammars, built in
Rust. This project aims to provide types and functions that are useful beyond
the context of formal language theory by generalizing to arbitrary structures.
It is applicable to generative art, data science, experimental combinatorics,
simulations, and more. Rust's integration of type theory makes intuitive
parametrized grammar types simple to construct and compose into a larger system
(which makes memory safety particularly relevant). It is not designed for
interactive experimentation; an interactive Python or Julia notebook would
generally be preferred for such tasks.

## Installation

TODO

## Usage

Here is a very general overview of the types provided by `grammars`:

- `Symbol`: A single unit (i.e., token) in a grammar or language
- `Pattern`: (note: the class of patterns is implemented as a trait)
	- `String`: An ordered collection of symbols
	- `Any`: Matches any symbol or pattern it contains, or generates one of those symbols if being sampled
	- `Repeat`: Repeats the item it wraps; if generating, that item will be sampled repeatedly
- `Rule`: A relation specifying how strings can be rewritten in a grammar
- `Grammar`: A set of rules and symbols (divided into *terminal* and *nonterminal* symbols)
- `Set`: A general container type
- `Alphabet`: A set of symbols
- `Language`: A grammar and alphabet it operates over
