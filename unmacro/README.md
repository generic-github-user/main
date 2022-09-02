# unmacro

A simple Python script that converts (interactively developed) Vim macros to
standalone text processing scripts. Results may vary.

If we have a list of titles like the one below and want to automatically format
them as a Markdown list, a Vim macro is an efficient and interactive way to do
so.

```
A Song of Ice and Fire
The Wheel of Time
Discworld
Nijntje (Miffy)
Alex Cross
```

*https://en.wikipedia.org/wiki/List_of_best-selling_books#Between_50_million_and_100_million_copies_2*

Recording the macro `I- wi*A*j` on the first line gives us this result:

```
- *A Song of Ice and Fire*
...
```

If we select the rest of the lines (e.g., using `V3j`) and apply the macro
(let's say it's in register `e`) to the other lines using `:'<,'>norm @e`, we
get something like this:

```
- *A Song of Ice and Fire*
- *The Wheel of Time*
- *Discworld*
- *Nijntje (Miffy)*
- *Alex Cross*
```
