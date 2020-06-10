# Complexity
Python program to calculate the complexity index of nanoparticles as represented by an undirected graph

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
This runs the program through a series of test cases that independently test the AVV and AVC calculations. Assuming there are no bugs, this command should produce the following output:
```
Testing AVV calculation...
...all tests passed!
Testing AVC calculation...
...all tests passed!
```

### Custom Input
The program takes user input as a `.csv` file delimited by `;`. 

The contents of the file should list out graph edges, where the first column is the edge Source, second column the edge Target (though all edges are treated as undirected and column names don't matter). See `input1.csv` and `input2.csv` (also in this repository) for examples. 

To run with a custom input, execute this command in the terminal:
```
python program.py input1.csv
```

This will calculate the AVC for the given input. The output for `input1.csv` is
```
AVC calculated is 6.0
```
The output for `input2.csv` is
```
AVC calculated is 5.0
```

## Program Description
The purpose of this program is to calculate graph complexity. It does this in two steps.

### Calculate AVV for each node in the graph
The AVV, or Augmented Vertex Valence, for each node is calculated in the function called `getAVVs()`, which takes a list of tuples that represent the edges of a graph. Here is a sample input:
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

For each node, the program calculates the AVV score using the algorithm described in Randic and Plavsic's "On the Concept of Molecular Complexity". The AVV for node N is a sum of each graph node's "contribution" to the calculation:
```
contribution = n / 2^m
```
where `n` is the count of outgoing edges (note self-loops count for two outgoing edges)
and `m` is the minimum distance from node A (note that nodes inaccessible from A do not count towards the contribution, even if included in the edge list)
The final AVV for node A is the sum of each node's contribution (including the contribution from A itself aka `m = 0`)

### Calculate AVC for the graph
Once we have a list of all AVV values for each node in the graph, the AVC is a simple sum of all unique AVVs. This is done in the function called `getAVC()`, which takes the same input as `getAVVs()` - a list of tuples that represent the edges of a graph. 
The function `getAVC()` first calls `getAVVs()`. It then takes the result of this call and dedupes the resulting values. It then calculates the AVC by summing together the unique values.