# CA2

This toolkit (titled CA2 for the time being) is a software framework to assist in investigating cellular automata, such as Conway's Game of Life. It is intended as the successor to a Python-based library I was developing previously for similar purposes; this version is written in C to permit more granular control of execution and more efficient computation (a highly relevant asset in, e.g., the case of brute force searches for automata patterns or rules with desired properties).

## Installation

### Requirements

- An updated version of Python (at least 3.9 is preferred)
- Matplotlib
- Access to `gcc` and `Make` (running using a terminal is preferred, though a standard compatibility layer should work fine if using Windows or a similar OS)

Note that all of the above tools must be included in your `PATH` environment variable (i.e., must be globally accessible).

Clone the repository and compile using `make`, then execute the normal way.

## Usage

This program includes an interactive mode (i.e., a command shell) for experimentation and entertainment; this will be entered automatically if the program is launched without passing any arguments (in the style of a REPL environment). It provides means for generating and simulating cellular automata, as well as reading and writing to local files. Data can be passed (piped) from one command to another using the `>` operator. Most of the commands automatically handle special cases or extensions of the basic objects generated by other commands, such as collections/sets of states or simulations.

This is a non-exhaustive list of commands that can be run in the tool's interactive mode:

- `randomstate -n [int >= 1] -w [int >= 0] -h [int >= 0] -t [topology]`: Randomly generate a set of cellular automata states
- `simulate [rule] -i [int >= 1] -r auto -p`
- `sort [property]`
- `rchoice [collection] -n [int >= 0]`: Randomly select the specified number of elements from a collection; for example, passing a simulation will return a subset of that simulation's states
- `clone -n [int >= 1]`: Create a collection of 
- `get [property]`: Extracts a property from the current selection, usually generating an array/matrix; as with the other commands, this will be distributed over iterable selections to produce a new axis
- `write [path]`: Store a human-readable text summary of the data (state(s), simulation(s), etc.) passed to the command at the specified filepath
- `save [path]`
- `print`: Display the current selection via `stdout`
- `render [path]`: Render the selected objects to an image file
- `plot`: Generate a plot from the current selection (using the Matplotlib wrapper)
- `abbr short long`: Create an abbreviation that will be expanded before a command is run, similar to preprocessor directives and macros in C
- `collapse`: Get the last state of one or more simulations
- `enumerate`: Iterate through possible states of a cellular automaton
- `min [property]`: Reduce a set of states based on the specified property
- `max [property]`
- `help`: Display this list
- `repeat`: Repeat the last command executed
- `clear [object]`: Free (deallocate) the memory used to store an object (useful in interactive mode if you no longer need access to an earlier selection you generated)
- `undo`: Revert previous command (only applicable to commands that mutate the current state/selection)
- `redo`: Redo an undone command

These options can be used with any command:

- `--help [command]`: Display information about the provided command
- `--dry`: Execute a "dry run", displaying information about the actions that would be executed without actually modifying the current selection or writing to any files
- `--log [int]`: Set the verbosity level (an integer greater than or equal to 0) for this command (useful to set as a default for all commands)

Here are descriptions of the `[types]` used in the above command descriptions:

- `int`: A simple integer; restrictions on the range of the number may be present for specific commands/options
- `rule`: A named cellular automata rule, like `cgol`
- `property`: One of population, volume, density
- `path`: A filepath (both relative and absolute are allowed)
- `command`: A command name (see the list above)
- `object`: An object that a selection can contain, e.g. a state, simulation, set of unrelated states, etc.

Commands can also be written into scripts using the `.ca` extension; newlines will be interpreted as pipe operators, as in the following example:

```
randomstate
simulate -i 300
get population
plot
```

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

Enumerate 10000 states on a 4 by 4 grid and simulate CGOL for 50 iterations, automatically expanding the bounds to fit the current state, then write information about each state into a text file:

```
enumerate -n 10000 -wh 4 > simulate cgol -i 50 > write ex3.txt
```

Find and display the densest state resulting from evolving 5000 random states on a torus manifold for 100 steps:

```
randomstate -n 5000 -wh 30 -t torus > simulate cgol -i 100 > max density > print
```

#### Plotting

Run a simulation and plot the population over each timestep:

```
randomstate > simulate cgol -i 100 > get population > plot
```

Run 200 simulations and plot their populations over each timestep:

```
randomstate -n 200 > simulate cgol -i 100 > get population > plot
```

Simulate different initial density conditions and simulation lengths and generate a heatmap of the resulting densities:

```
randomstate -n 100 -d 0.01:0.99 > simulate cgol -i 100 > plot density
```

Run 1000 simulations and generate a scatter plot of the final densities and average neighbor counts:

```
randomstate -n 1000 > simulate cgol -i 100 >
```

Run 1000 simulations and generate a histogram of the final populations, such that the full range is divided into 20 bins:

```
randomstate -n 1000 > simulate cgol -i 100 > get population > group -n 20 > plot
```

## About

### Project structure

The main modules are subdirectories of the repository (`array`, `commands`, etc.); these generally contain a C source file, a corresponding C content file, a header file, and object file; and may have additional scripts or templates. A custom build script, `build.py` transforms each `.c0` file into a `.c` file by inserting templates from `.ct` (C template) files (a sort of fine-tuned pre-preprocessor), which is then used normally by the C compiler and linker.

Plain template files can be used to separate large source files into more manageable modules (see the `commands` directory for an example); these are essentially copied and pasted into the source files like the C preprocessor does with directives and includes, via the following syntax:

```
{{template_name}}
```

where `template_name.ct` is a file in the same directory.

Templates may also have arguments:

```
$template_name(arg_1:value_1,arg_2:value_2,...)$
```

These will be expanded into the corresponding fields in the template file. For example, the template

```
TYPE NAME(array a) {
	TYPE output = INIT;
	for (int i=0; i<a.size; i++) {
		output = output OP a.data[i];
	}
	return output;
}
```

and reference

```
$ARRAY_REDUCE(name:array_sum,type:int,op:+,init:0)$
```

will produce an output similar to the following (with the appropriate date and time):

```
/* Imported from ./array/array_reduce.ct at 05/23/2022, 05:43:02 */ 
int array_sum(array a) {
	int output = 0;
	for (int i=0; i<a.size; i++) {
		output = output + a.data[i];
	}
	return output;
}
```

The majority of the project is written in C, for reasons both of control and efficiency. The most notable exceptions are the build scripts and graphing/plotting utilities, both of which benefit greatly from improved concision and do not need to be highly specialized. The C-based command processor interfaces with those scripts using temporary local files to store data (where applicable) and system calls. The most notable example is the plotting code, which writes to `pltdata.txt` and then calls `plot/plot.py`.
