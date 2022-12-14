# lyre

lyre is a weird, wonderful little language that takes heavy inspiration from
lisp, most notably in its minimalism and homoiconicity. It also draws on Rust,
Julia, Python, Nu, and Bash, among a handful of other languages. My main goal
was to create a language that is as elegant, expressive, and generic as lisp
but less verbose and easier to write code that is stylistically compatible with
multiple programming paradigms.

## Installation

At the moment, lyre is in an early development phase and the recommended way to
use the reference interpretation is by cloning this repository and building the
binary application with Cargo, Rust's pacakage manager.

Currently, the following requirements are listed in `Cargo.toml`:

```
num-traits = "0.2.15"
```

Cargo should be able to install these automatically prior to build. `cargo
build` and/or `cargo run` can then be used to build and execute the lyre
interpreter.

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

Generally, the first item in a form dictates what happens to the rest of its
contents; often, it will be the name of a function that is called with the
other item and sub-expressions as arguments. This applies to operators like
`+`, functions like `print` (and macros), and keywords like `def`. Here's an
example "Hello world" program:

```
echo Hello, world!
```

`echo` is a special function in lyre that does not evaluate its arguments, but
instead captures (quotes) them as syntactic forms, which are then converted to
strings. This is concise and helpful for experimentation, but a more robust
choice would look something like the following:

```
print "Hello, world!"
```

### Operators

Common arithmetic operators are available using the prefix notation described
above:

```
[print [+ 5 7]]
[print [- 23 4]]
[print [* 3 16]]
[print [/ 9 3]]
[print [** 4 4]]
[print [% 18 5]]
```

Since each of these forms occurs on the top level of our program, we can omit
the square brackets around each line:

```
print [+ 5 7]
print [- 23 4]
print [* 3 16]
print [/ 9 3]
print [** 4 4]
print [% 18 5]
```

These operators are not particularly unique; they provide convenient aliases to
several built-in functions:

```
print [add 5 7]
print [sub 23 4]
print [mul 3 16]
print [div 9 3]
print [pow 4 4]
print [mod 18 5]
```

### Strings

String literals can be constructed in the standard way, and can extend across
lines:

```
reverse "I will do't:"

dedent "And, for the purpose,
				I'll anoint my sword."

split "I bought an unction of a mountebank,"

slice "So mortal, that but dip a knife in it,"

join " " "Where it draws blood" "no cataplasm so rare,"

print "Collected from all simples that have virtue"

title-case "Under the moon, can save the thing from death"

format "{}: {}" "That is but scratch'd withal" "I'll touch my point"

"With this contagion, that, if I gall him slightly,"

strip "       It may be death.      "
```

### Variables

lyre includes the `set` keyword to assign a variable in the current scope:

```
[set num 42]
```

We can use `get` to retrieve the value of a symbol, though this is usually not
necessary (unless explicitly indicated otherwise, function calls evaluate their
arguments and use the resulting values).

```
[println [get num]]
[println num]
```

Calls to `set` also act as expressions, returning the value they were passed:

```
[println [set num 42]]
```

Variable types can be explicitly annotated:

```
[set [int a] 77]
[set [string b] "a short string"]
[set [float c] 3.14]
```

`unset` removes a variable from a namespace:

```
[unset num]
```

We're all adults here; though lyre will typically warn you if you attempt to do
something extremely misguided:

```
[unset unset]
```

Warnings can be suppressed with the `ikwiad` ("I know what I am doing") macro:

```
[ikwiad unset unset]
```

### Error Handling

lyre borrows from Rust's error-handling philosophy; there are two broad
categories of error, those which the program can recover from and those from
which it cannot. The latter is an exceptional state, often understood to be a
programmer error, and generally prompts an immediate exit from the thread of
execution. lyre provides various primitives, functions, and interfaces to
represent both and facilities for extending these.

### Classes

#### Example: Point

Let's define a simple point class:

```
class Point
		float x
		float y
```

... and a simple constructor function:

```
class Point
		float x
		float y

		def new [x' y' -> Point]
				Point [x x'] [y y']
```


If we want to print a human-readable summary of the data in a `Point` instance,
we should implement `to-string`:

```
class Point
		float x
		float y

		def new [x' y' -> Point]
				Point [x x'] [y y']

		def to-string self
				format "({}, {})" x y
```

This is the method that will be invoked whenever we need to coerce a `Point` to
a `string` -- so we can now use `Point`s as arguments to `print`, `println`,
`format`, and other string-adjacent functions:

```
[println "The Point: {}" ]
```
