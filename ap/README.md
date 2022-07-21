# ap

*ao-python*

An alternative to the shell-based version of the ao codebase, which is
beginning to show issues with maintainability and scalability. Rust, Lisp, and
zx were also considered (among other languages), but Python's interoperability
(particularly, the massive ecosystem of useful packages and libraries) and
convenience made it the best choice for this next iteration. Another advantage
is how seamlessly pickling/serialization integrate with Python's object model,
permitting fluid development of customized classes that are easy for humans to
interact with.

The core philosophy is the same: track everything, always; and make things
easier for the user (myself in particular), even at the expense of speed or
mathematical elegance. This tool implements many functionalities (file
tracking, bookmark management) that I had been planning to design standalone
tools for; I still might in the future, but being tied to an established API
inhibits rapid prototyping and generalization makes it more time-consuming to
tailor functionality to my needs (though I still try to follow practices like
DRY for the sake of maintainability and consistency as the codebase grows).

At this point, the Python branch is my preferred tool and I'm unsure to what
extent (if any) I will continue developing and/or maintaining the shell
version.
