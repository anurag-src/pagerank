import numpy as np
filename = 'web-Google_10k.txt'
with open(filename,'r') as input_file:
    # The first 4 lines are metadata about the graph that you do not need
    # After the metadata, the next lines are edges given in the format: `node1\tnode2\n` where node1 points to node2
    lines = [item.replace('\n','').split('\t') for item in input_file]
    edges = [[int(item[0]),int(item[1])] for item in lines[4:]]
    nodes_with_duplicates = [node for pair in edges for node in pair]
    nodes = sorted(set(nodes_with_duplicates))
    # There are 10K unique nodes, but the nodes are not numbered from 0 to 10K!!!
    # E.g. there is a node with the ID 916155
    # So you might find these dictionaries useful in the rest of the assignment
    node_index = {node: index for index, node in enumerate(nodes)}
    index_node = {index: node for node, index in node_index.items()}
#print(index_node)
out = {}
dead = set()
def outlinks():
    for i in nodes:
        out[i] = 0
    for i in range(len(edges)):
        out[int(edges[i][0])] += 1
    for i in out.keys():
        if out[i] == 0:
            dead.add(i)
outlinks()

def power():
    n = 10000
    m = np.zeros((n,n),dtype = float)
    for i in range(len(edges)):
        if out[edges[i][0]] != 0:
            m[node_index[edges[i][1]], node_index[edges[i][0]]] = 1/out[edges[i][0]]

    for node in dead:
        m[:, node_index[node]] = 1 / n
    e = np.ones(n, dtype = int)
    r = np.ones(n, dtype=float)/n
    beta = 0.85
    epsilon = 0.0001
    a = beta*m + ((1-beta)/n)*e*e.T
    err = 99999
    while err > epsilon:
        rnext = a@r.T
        err = np.linalg.norm(r-rnext, ord = 1)
        r = rnext
    max = 0
    maxout = 0
    for i in range(len(rnext)):
        if rnext[i] > max:
            max = rnext[i]
            maxout = i
    maxout = index_node[maxout]
    print(maxout)
    count = 0
    for i in range(len(edges)):
        if edges[i][1] == maxout:
            count += 1
    print(count)

power()
