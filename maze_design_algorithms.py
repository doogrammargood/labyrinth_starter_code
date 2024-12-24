#This file contains some algorithms needed to for the maze program.
#TODO: implement the Fisher Shuffle and Kruskal's algorithm to return
import numpy as np
def fisher_shuffle(n):
    #Expects n to be a positive integer.
    #Returns a uniformly random permutation of the list [0..n-1]
    #TODO
    '''
    Use: 
        np.random.randint(a) . . . . selects a random number in the range [0..a-1]
    '''
    pass

def kruskals(G, edge_weights):
    #expects G to be a networkx graph. 
    #expects edge_weights to be dictionary whose keys are nodes and values are nonnegative weights of G
    #returns a networkx spanning tree of G.
    #TODO

    def get_component(node,components):
        #Expects node to be a node, and components to be a dictionary.
        #Returns a node in the connected component of node that represents the connected component.

        #This implementation repeatedly calls component until the answer stabilizes at a representative node in the component,
        #then updates the values of components for all keys queried along the way to point to this representative.
        #You may implement this differently.
        pass
    return G.edge_subgraph(spanning_tree_edges) #returns the subgraph spanned by the edges of G.

def random_spanning_tree(G):
    #expect G to be a networkx graph.
    #returns a spanning tree uniformly at random.
    shuffle = fisher_shuffle(len(G.edges))
    edge_weights = {edge: shuffle[i] for i,edge in enumerate(G.edges)}
    return kruskals(G,edge_weights)