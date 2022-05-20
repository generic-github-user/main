# CA2

This toolkit (titled CA2 for the time being) is a software framework to assist in investigating cellular automata, such as Conway's Game of Life. It is intended as the successor to a Python-based library I was developing previously for similar purposes; this version is written in C to permit more granular control of execution and more efficient computation (a highly relevant asset in, e.g., the case of brute force searches for automata patterns or rules with desired properties).

## Installation

Clone the repository and compile using `gcc ca.c -g`, then execute the normal way.

## Usage

This program includes an interactive mode (i.e., a command shell) for experimentation and entertainment; this will be entered automatically if the program is launched without passing any arguments (in the style of a REPL environment). It provides means for generating and simulating cellular automata, as well as reading and writing to local files. Data can be passed (piped) from one command to another using the `>` operator. Most of the commands automatically handle special cases or extensions of the basic objects generated by other commands, such as collections/sets of states or simulations.

This is a non-exhaustive list of commands that can be run in the tool's interactive mode:

- `randomstate -n [int] -w [int] -h [int]`: Randomly generate a set of cellular automata states
- `simulate [rule] -i [int] -r auto -p`
- `sort [property]`
- `write [path]`: Store a human-readable text summary of the data (state(s), simulation(s), etc.) passed to the command at the specified filepath
- `save [path]`
- `print`: Display the current selection via `stdout`
- `render [path]`: Render the selected objects to an image file
- `abbr short long`: Create an abbreviation that will be expanded before a command is run, similar to preprocessor directives and macros in C
- `collapse`: Get the last state of one or more simulations
- `enumerate`: Iterate through possible states of a cellular automaton
- `min [property]`: Reduce a set of states based on the specified property
- `max [property]`
- `help`: Display this list
- `undo`: Revert previous command
- `redo`

Here are descriptions of the `[types]` used in the above command descriptions:

- `int`: A simple integer; restrictions on the range of the number may be present for specific commands/options
- `rule`: A named cellular automata rule, like `cgol`
- `property`: One of population, volume, density
- `path`: A filepath (both relative and absolute are allowed)

### Examples

Here are a few practical examples that illustrate command usage (note that not all of these are fully implemented yet).

Generate 1000 random states, simulate for 200 iterations, and write the final states to a text file:

```
randomstate -n 1000 > simulate -i 200 > collapse > write ex1.txt
```

Simulate 100 iterations of Conway's Game of Life, rendering to stdout:

```
randomstate > simulate -i 100 -p
```
