# cellular-automata-experiments

Various experiments with cellular automata; so far, the following features have been implemented:
 - Reasonably fast simulation of simple neighborhood-based cellular automata, such as Conway's Game of Life
 - Collection of statistics about a particular simulation, allowing for coloring cells by age, tracking population over time, or visualizing which areas saw the most activity
 - Easy analysis and visualization of cellular automata space, allowing for examination of relationships between different starting conditions/outcomes (e.g., graphing the maximum population of 100 randomly initialized CGOL worlds over 500 generations given a random fraction of living cells at t=0)
 - Searching for initial conditions that produce a particular pattern after some number of generations or to optimize some function (e.g., finding the 4x4 pattern that will produce the highest maximum population over 1000 generations based on a randomly generated sample)
 - Interactive GUI for editing simulations in situ (adding/removing cells, starting and stopping, etc.)
