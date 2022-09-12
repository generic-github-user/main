# finch

*Fast, good, and cheap*

Finch is a general-purpose, multiparadigm programming language that draws
inspiration from Rust, Lisp, and Python, among several other languages. It aims
to be a highly capable choice for both high-level and low-level projects
spanning many different applications; and to support a wide range of coding
styles and environments without sacrificing quality, efficiency, or developer
experience.

It is not yet ready for practical use; I aim to release the first stable
version of Finch by January 2023 (subject to change). My goal is to have a
reasonably complete reference implementation in Rust within the next few
months, though further (substantial) changes are still a possibility ater that
point.

My hope is for Finch to be usable (and enjoyable) in all of the below settings,
among others:

- Systems programming
- Scripting and automation
- Mathematics (both numerical and symbolic)
- Application programming
- Machine learning and artificial intelligence
- Statistics
- Text processing and data science
- Web development
- Markup and templating

That said, there are certainly many areas where it *doesn't* aim to act as a
replacement for any existing standards; for example, the current Finch design
plan includes a fairly substantial runtime, so a compact and fully compiled
language like Rust might be a better choice for embedded applications.

**Note**: the master/main branch is pretty boring at the moment since the language is in a very early development phase, where core features are being designed, implemented, tested, and documented; I encourage anyone whose interest was piqued by the above description to take a look at some of the other [branches](https://github.com/generic-github-user/finch/branches).

*Credit to [@RaineDelay](https://github.com/RaineDelay) for the language name suggestion*


## Branches

- `master`: The main branch, where stable versions of Finch will be tagged and released from (though most likely not until several months from now)
- `parser`: The reference implementation of the Finch parser, which is meant to conform (more or less) to the grammar outlined on the `specification` branch
- `specification`: Grammars, diagrams, natural language descriptions, and other materials outlining my vision for Finch that will (ideally) guide development of the parser and runtime
- `stdlib`: The Finch standard library, modeled loosely after those of Python and Rust (as well as some *de facto* standards like NumPy that are consistent and stable enough to be considered part of the language for most purposes)
>>>>>>> specification
