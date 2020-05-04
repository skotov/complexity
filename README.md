# Complexity
Python program to calculate various types of graph complexity for application in nanoparticle complexity analysis

## Getting Started
Clone the repository on the command line
```
git clone https://github.com/skotov/complexity.git
```

Run the program
```
python program.py
```

This runs the program through a series of test cases, calculating AVV for each input.

The core function of interest in `getAVVs()`, which takes a list of tuples, i.e.
```
[(1,2), (2,3), (3,4), (4,2)]
```
Each tuple represents a graph edge; the full list of tuples represents the graph

## Remaining Work
- Allow CSV inputs via command line i.e. `python program.py myInput.csv`
- Split out tests into separate program
