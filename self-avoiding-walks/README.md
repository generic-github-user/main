# Self-Avoiding Walks

Refer to the [Wikipedia article](https://en.wikipedia.org/wiki/Self-avoiding_walk) on self-avoiding walks for a good primer on the subject. [Bauerschmidt et al. (2012)](https://www.ihes.fr/~duminil/publi/saw_lecture_notes.pdf) give an extremely thorough description of known qualities of self-avoiding random walks and their connections to other areas of mathematics. Here are links to some other resources I found informative:

 - MathOverflow
   - https://mathoverflow.net/questions/158811/wander-distance-of-self-avoiding-walk-that-backs-out-of-culs-de-sac
   - https://mathoverflow.net/questions/52813/self-avoiding-walk-enumerations
   - https://mathoverflow.net/questions/41543/how-to-characterize-a-self-avoiding-
   - https://mathoverflow.net/questions/54144/self-avoiding-walk-pair-correlation
   - https://mathoverflow.net/questions/23583/self-avoidance-time-of-random-walk
   - https://mathoverflow.net/questions/181340/square-filling-self-avoiding-walk
   - https://mathoverflow.net/questions/1592/special-cases-for-efficient-enumeration-of-hamiltonian-paths-on-grid-graphs
   - https://math.stackexchange.com/questions/2900521/counting-hamiltonian-cycles-in-a-graph
 - https://stackoverflow.com/questions/7371227/algorithm-to-find-a-random-hamiltonian-path-in-a-grid
 
Some exhaustive results by numerical simulation are available here (also see the OEIS entries and their associated references, several of which contain extensive tables of data for specific grid sizes):

 - https://secure.math.ubc.ca/~slade/lacecounts/index.html
 - https://secure.math.ubc.ca/~slade/se_tables.pdf
 
Here are some other academic results on the topic:

 - https://secure.math.ubc.ca/~slade/se_tables.pdf
 - https://www.sciencedirect.com/science/article/abs/pii/0032386185900084?via%3Dihub
 - https://journals.aps.org/prb/abstract/10.1103/PhysRevB.31.2993
 - https://arxiv.org/abs/1408.6714
 - https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i4p7
 - https://arxiv.org/pdf/1110.3074.pdf
 - http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.2950
 - https://www.researchgate.net/publication/267115049_Enumeration_of_Hamiltonian_Cycles_in_Some_Grid_Graphs
 
Other interesting simulations/related information:

 - https://mathoverflow.net/questions/88659/traversing-the-infinite-square-grid
 - https://mathoverflow.net/questions/306794/counting-hamiltonian-cycles-in-n-times-n-square-grid
 - https://iopscience.iop.org/article/10.1088/0305-4470/38/42/001
 - https://mathoverflow.net/questions/67192/exactly-simulating-a-random-walk-from-infinity
 - http://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf
 - http://www.njohnston.ca/2009/05/on-maximal-self-avoiding-walks/
 - https://datagenetics.com/blog/december22018/index.html
 - https://mathworld.wolfram.com/GridGraph.html
 - https://math.stackexchange.com/questions/4018110/calculate-the-area-of-a-n-times-n-grid-using-a-2d-random-walk
 - https://rdlyons.pages.iu.edu/rw/rw.html
 - https://demonstrations.wolfram.com/SelfAvoidingRandomWalks/
 - https://www.researchgate.net/figure/a-shows-all-possible-backbite-moves-b-c-show-all-resulting-structures-after-the_fig2_221008721
 - http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.35.3648&rep=rep1&type=pdf
 - OEIS
     - https://oeis.org/A145157
     - https://oeis.org/A120443
     - https://oeis.org/A046995
     - https://oeis.org/A046994
 
Some search terms in case you wish to explore further:

 - (Self-avoiding) random walks (SAWs)
 - Lattice theory
 - Space-filling curve
 - Combinatorics
 - Hamiltonian path (also see Hamiltonian cycle, bent Hamiltonian path)
 - (Solid) grid graph
 - [Peano curve](https://en.wikipedia.org/wiki/Peano_curve)
 - (Minimum) [spanning tree](https://en.wikipedia.org/wiki/Spanning_tree)
 - Depth-first (tree) search
 - Chaos theory
 - [Regular graph](https://en.wikipedia.org/wiki/Regular_graph)
 - [Component](https://en.wikipedia.org/wiki/Component_(graph_theory))
 - [Adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix)
 - Planar graph
 - Backbite algorithm
     - This approach appears a handful of times (seriously, a Google search for that specific phrase returned 46 results), mostly in blog posts; it appears to be effective for some purposes (mainly artistic or exploratory) despite its obscurity
     - (Though, as far as I can tell, the method only produces a small subset of the possible Hamiltonian paths on a grid/lattice and a brute force search is required for rigorous conclusions regarding a given grid size (also see: NP-completeness); clearly, the issue there is that the search space is intractably large for grid sizes above 6 by 6 or so, even in 2 dimensions.)
 - Ant colony optimization/system
 - Maze generation algorithms
 - Pivot algorithm (self-avoiding walks)
 - Coarse graining

Other notes:

 - "Greek-key tours" also came up in a handful of online blog posts (linked above) but I was unable to find any relevant information in the literature; in case you want to look, it seems to be related to chess, in the same sense as a Knight's Tour. It also appears in the context of [protein folding](https://en.wikipedia.org/wiki/Beta_sheet#Greek_key_motif) (a surprisingly connected subject).
 - There are quite a few thorough but (unfortunately) isolated resources about this niche of geometry/graph theory on the web; there appears to be a standard nomenclature and some established methodology for these problems but very limited resources on specific (and modern - most of what I could find is at least a few years old) implementations.
