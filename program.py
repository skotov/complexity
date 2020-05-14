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
def getAVVs(edges):
    nodes = getUniqueNodesFromEdges(edges)
    neighbors = getNeighborMapping(edges, nodes)
    avvMapping = {}
    for n in nodes:
        avvMapping[n] = calculateAvv(n, edges, neighbors)
    return avvMapping

def program():
    test1 = [(1,1)] # each test is a graph as described by a set of edges
    result1 = {1:2} # maps nodeId --> AVV
    if (result1 != getAVVs(test1)):
        print "Failed Test 1"

    test2PartA = [(1,2)] 
    result2A = {1: 1.5, 2: 1.5}
    if (result2A != getAVVs(test2PartA)):
        print "Failed Test 2 Part A"

    test2PartB = [(1, 2), (2, 1)] # test bidirectional 
    result2B = {1: 3, 2: 3}
    if (result2B != getAVVs(test2PartB)):
        print "Failed Test 2 Part B"

    test2PartC = [(1, 1), (1, 2), (2, 1)] # test that self-loops count for two
    result2C = {1: 5, 2: 4}
    if (result2C != getAVVs(test2PartC)):
        print "Failed Test 2 Part C"
    return

    test3 = [(1, 2), (2, 3), (3, 1)]
    result3 = {1: 4, 2: 4, 3: 4}
    if (result3 != getAVVs(test3)):
        print "Failed Test 3"

    test4PartA = [(0, 1), (1, 2), (1, 3), (1, 5), (2, 3), (3, 4), (5, 4)]
    test4PartB = [(1, 2), (5, 4), (0, 1), (1, 5), (1, 3), (3, 4), (2, 3)] # same as above, but shuffled
    result4 = {0: 5, 1: 8.5, 2: 6.75, 3: 7.75, 4: 6.125, 5: 6.5}
    if (result4 != getAVVs(test4PartA)):
        print "Failed Test 4 Part A"
    if (result4 != getAVVs(test4PartB)):
        print "Failed Test 4 Part B"
    
    

if __name__ == "__main__": 
    filename = "test.csv"
    program()

    