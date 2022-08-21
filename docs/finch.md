# The Book

## Introduction

Welcome to the Finch manual. This is a (hopefully comprehensive) guide to
reading and writing code in Finch, covering variables, functions, expressions,
data types, control structures, testing, documentation, and many other topics.
The goal is to provide enough exposition, relevant examples, and detailed
elaboration on available methods or tools for the programmer to be able to
reliably choose the best option for their use case. It is very difficult (read:
impossible) to do so in a way that fits every reader well - so I encourage
anyone who wants to build deeper knowledge of the language to do their own
experimentation, take a look at the standard library source, read the other
documentation, and so on. I will also aim to arrange this in a (more or less)
linear format where each section builds on previous ones, such that you can
read or skim from start to finish without much friction and come away with a
fairly complete understanding of the language's basics. However, most chapters
can stand on their own, especially if you have previous programming experience.
I hope it serves you well. Best of luck.

## Basic Data Types

### Numbers

The most basic unit of a program in Finch (like in many other languages) will
variously be referred to as an *atom*, *value*, or *primitive*. The typical
example is an integer, which is usually represented as one "word" in a given
instruction set architecture and which corresponds to a "literal"
representation in a programming language's syntax.

Like Rust or C, Finch supports several basic integer types: `int8`, `int16`,
`int32`, `int64`, and `int128`. These each have a range corresponding to a
power of 2 (e.g., `int8` can represent 256 values, but this range is split over
the negative and positive integers, centered at 0). By default, the [reference
implementations of the] Finch compiler will check for integer overflows and
emit a warning since this usually causes unpredictable behavior. The shorter
aliases `i8`, `i16`, etc. are also available. For floating-point numbers there
are the analogous `float32` (`f32`) and `float64` (`f64`) types.
