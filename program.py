import sys
import csv

# Parameters: 
#     nodeId -- a number
#     graphEdges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)]
# Returns: 
#     A list of tuples i.e. [(1,2), (2, 3), (3,1)] representing the edges extending from nodeId (includes self-loops)
def getAdjacentEdges(nodeId, graphEdges):
    adjacentEdges = []
    for e in graphEdges:
        src = e[0]
        target = e[1]
        if (src == nodeId or target == nodeId):
            adjacentEdges.append(e)
    return adjacentEdges

# Parameters
#   n -- a nodeId - the node for which we want to find adjacencies
#   edges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)]
# Returns
#   nodes -- a list of nodeIds with duplicates included
def getAdjacentNodes(n, edges):
    nodes = []
    for e in edges:
        if e[0] != n:
            nodes.append(e[0])
        elif e[1] != n:
            nodes.append(e[1])
        elif e[0] == n and e[1] == n:
            # only count itself as a neighbor if it's a self loop
            # self-loops count for two neighbors because of two outgoing edges
            nodes.append(n) 
            nodes.append(n)
    return nodes

# Parameters: 
#     graphEdges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)]
#     nodes -- list of numbers where each number is a nodeId
# Returns: 
#     Mapping of nodeId --> list of numbers[]. This represents the list of Nodes adjacent to nodeId
# Note that if a node has a self-loop, then this counts as two neighbors
def getNeighborMapping(edges, nodes):
    neighbors = {}
    for n in nodes:
        adjacentEdges = getAdjacentEdges(n, edges)
        neighbors[n] = getAdjacentNodes(n, adjacentEdges)
    return neighbors

# Parameters
#   edges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)]
# Returns
#   nodes -- a deduped list of numbers where each number is a nodeId
def getUniqueNodesFromEdges(edges):
    nodes = set() # using a set for easy deduping
    for e in edges:
        nodes.add(e[0])
        nodes.add(e[1])
    return list(nodes) # returning as a list for easy interaction

# Parameters
#     n -- a  number, corresponding to nodeId 
#     graphEdges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)]
#     graphNeigbors -- dictionary of (number aka nodeId --> Node[])
def calculateAvv(n, graphEdges, graphNeighbors):
    avv = 0

    # ----
    # Step 1: Explore the full graph and derive a mapping of nodeId --> that node's distance from n
    # this graph will contain all nodes that are reachable from n
    # ----

    # This is just a list, but treating as a FIFO queu, the driving data structure behind 
    # the breadth first search algorithm below. Initialized to contain only the origin node
    nodeQueue = [n] 

    # A set of Nodes (Using set instead of list for easy lookup and deduping)
    visitedNodes = set()
    
    # depthLookup is type dictionary of (number --> number). 
    # Maps Node id onto that node's depth/distance from n, the origin node
    depthLookup = {} 
    depthLookup[n] = 0 # origin node's depth is 0 because it is 0 edges away from itself
    
    # run breadth first search to explore the full graph and get each node's distance to
    # the origin node, n. We'll then use the depth in the AVV calculation
    while (len(nodeQueue) > 0):
        # pop a node from the stack
        currentNode = nodeQueue.pop(0)
        # check whether we have visited this node yet
        if (currentNode not in visitedNodes):
            # explore surrounding nodes
            adjacentNodes = graphNeighbors[currentNode]            
            for node in adjacentNodes:
                nodeQueue.append(node)
                # note the depth of surrounding nodes.
                if node not in depthLookup: # this check prevents overwriting the min depth
                    depthLookup[node] = depthLookup[currentNode] + 1
                    
            # add to visited set so that we only count this node once
            visitedNodes.add(currentNode)

    # ----
    # Step 2: Using the depth lookup and graphNeighbors lookup, calculate the AVV, one node at a time, keeping a running sum
    # ----
    for node in depthLookup:
        adjacentNodes = graphNeighbors[node]
        nodeDepth = depthLookup[node]
        avv += float(len(adjacentNodes)) / float(2**nodeDepth)
    return avv

# Parameters
#   edges -- a list of tuples, i.e. [(1,2), (2, 3), (3,1)] representing the edges in a graph
# Returns
#   a mapping of nodeId --> it's AVV
def getAVVs(edges):
    nodes = getUniqueNodesFromEdges(edges)
    neighbors = getNeighborMapping(edges, nodes)
    avvMapping = {}
    for n in nodes:
        avvMapping[n] = calculateAvv(n, edges, neighbors)
    return avvMapping

def testAvvs():
    print "Testing Avv calculation..."
    testsFailed = 0

    test1 = [(1,1)] # each test is a graph as described by a set of edges
    result1 = {1:2} # maps nodeId --> AVV
    if (result1 != getAVVs(test1)):
        print "Failed Test 1"
        testsFailed +=1

    test2 = [(1,2)] 
    result2 = {1: 1.5, 2: 1.5}
    if (result2 != getAVVs(test2)):
        print "Failed Test 2"
        testsFailed +=1

    test3 = [(1, 2), (2, 1)] # test bidirectional 
    result3 = {1: 3, 2: 3}
    if (result3 != getAVVs(test3)):
        print "Failed Test 3"
        testsFailed +=1

    test4 = [(1, 1), (1, 2), (2, 1)] # test that self-loops count for two
    result4 = {1: 5, 2: 4}
    if (result4 != getAVVs(test4)):
        print "Failed Test 4"
        testsFailed +=1

    test5 = [(1, 1), (1, 2), (1, 1)] # test that two self-loops count for four
    result5 = {1: 5.5, 2: 3.5}
    if (result5 != getAVVs(test5)):
        print "Failed Test 5"
        testsFailed +=1

    test6 = [(1, 2), (2, 3), (3, 1)]
    result6 = {1: 4, 2: 4, 3: 4}
    if (result6 != getAVVs(test6)):
        print "Failed Test 6"
        testsFailed +=1

    test7PartA = [(0, 1), (1, 2), (1, 3), (1, 5), (2, 3), (3, 4), (5, 4)]
    test7PartB = [(1, 2), (5, 4), (0, 1), (1, 5), (1, 3), (3, 4), (2, 3)] # same as above, but shuffled
    result7 = {0: 5, 1: 8.5, 2: 6.75, 3: 7.75, 4: 6.125, 5: 6.5}
    if (result7 != getAVVs(test7PartA)):
        print "Failed Test 7 Part A"
        testsFailed +=1
    if (result7 != getAVVs(test7PartB)):
        print "Failed Test 7 Part B"
        testsFailed +=1
    
    test8 = [(1,2), (2,3), (3,4), (4, 2)]
    result8 = {1: 3.5, 2: 5.5, 3: 4.75, 4: 4.75}
    print getAVVs(test8)
    if (result8 != getAVVs(test8)):
        print "Failed Test 8"
        testsFailed += 1
    
    # after done testing, log test result
    if testsFailed == 0:
        print "...all tests passed!"
    elif testsFailed == 1:
        print "...failed 1 test total"
    else:
        print "...failed {} tests total".format(testsFailed)
    
# Parameters
#   filename - file name as string
# Returns
#   the edges in the csv file -- a list of tuples i.e. [(1,2), (2, 3), (3,1)]
def readCsv(filename):
    edgeSourceIndex = 0
    edgeTargetIndex = 1
    edges = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        reader.next() # skip the first line
        for row in reader:
            edge = (int(row[edgeSourceIndex]), int(row[edgeTargetIndex]))
            edges.append(edge)
    return edges

if __name__ == "__main__": 
    # if no arguments provided, simply run the test suite
    if (len(sys.argv) == 1):
        testAvvs()
    else:
        filename = sys.argv[1]
        # add in the csv file ending if user did not type it
        if filename[-4:] != '.csv':
            filename = filename + '.csv'
        edges = readCsv(filename)
        print getAVVs(edges)

    