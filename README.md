# Complexity
Python program to calculate various types of graph complexity for application in nanoparticle complexity analysis

## Getting Started
Clone the repository on the command line into your folder of choice
```
git clone https://github.com/skotov/complexity.git
```

Run the program by executing this command in the terminal
```
python program.py
```

### Test Suite
This runs the program through a series of test cases, calculating AVV for each input. Assuming there are no bugs, this command should produce the following output:
```
Begin testing Avv calculation...
...all tests passed!
```

### Custom Input
The program takes user input as a `.csv` file delimited by `;`. 

The contents of the file should list out graph edges, where the first column is the edge Source, second column the edge Target (though all edges are treated as undirected and column names don't matter). See `input1.csv` (also in this repository) for an example. 

To run with a custom input, execute this command in the terminal:
```
python program.py input1.csv
```

This will parse the csv, run the AVV calculation, and output the result as a dictionary in the format `<nodeId>: <avv>`. The output for `input.csv ` is
```
{0: 2.0, 1: 4.0, 2: 4.0, 3: 4.0}
```

## Program Description

The core function of interest in `getAVVs()`, which takes a list of tuples that represent the edges of a graph:
```
[(1,2), (2,3), (3,4), (4,2)]
```
and returns a dictionary in the format `<nodeId>: <avv>`. Given the above input, the expected output is:
```
{1: 3.5, 2: 5.5, 3: 4.75, 4: 4.75}
```

By looking at the list of edges, the program deduces the nodes that exist on this graph. In this case, nodes are
```
[1, 2, 3, 4]
```

For each node, the program calculates the AVV score using the algorithm described in Randic and Plavsic's "On the Concept of Molecular Complexity". It does this using a modified breadth first search algorithm

