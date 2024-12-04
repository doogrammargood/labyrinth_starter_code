#This file contains some algorithms needed to for the maze program.
#TODO: implement the Fisher Shuffle and Kruskal's algorithm to return
import numpy as np
def fisher_shuffle(n):
    #returns a uniformly random permutation of the list [0..n]
    to_return = []
    unstruct_numbers = list(range(n))
    for k in range(n)[::-1]:
        random_index = np.random.randint(k+1)
        random_value = unstruct_numbers[random_index]
        to_return.append(random_value)
        unstruct_numbers.remove(random_value)
    return to_return

def kruskals(G, edge_weights):
    #expects G to be a networkx graph. 
    #expects edge_weights to be nonnegative weights of G
    #returns a networkx spanning tree of G.
    edges = sorted(G.edges,key=lambda edge: edge_weights[edge] ) #sort edges by weight.
    spanning_tree_edges = []
    components = {} #a dictionary to store representatives for each connected component.
    for node in G.nodes:
        components[node]=node
    def get_component(node,components):
        #repeatedly calls component until the answer stabilizes.
        #returns a node in the connected component of node that represents the connected component.
        #updates the values of components for all keys queried along the way to point to this representative.
        comp=None
        next_comp= node
        nodes_along_way = [node]
        while comp != next_comp:
            comp = next_comp
            next_comp = components[next_comp]
            nodes_along_way.append(comp)
            
        for intermediate_node in nodes_along_way:
            components[intermediate_node]=comp
        return comp
    for edge in edges:
        node1,node2 = edge
        if get_component(node1,components)!=get_component(node2,components):
            spanning_tree_edges.append(tuple(sorted(edge)))
            components[get_component(node2,components)]=node1
    return G.edge_subgraph(spanning_tree_edges)

def random_spanning_tree(G):
    #expect G to be a networkx graph.
    #returns a spanning tree uniformly at random.
    shuffle = fisher_shuffle(len(G.edges))
    edge_weights = {edge: shuffle[i] for i,edge in enumerate(G.edges)}
    return kruskals(G,edge_weights)


def update_shortest_distances(K,shortest_distances,new_edge,new_edge_distance):
    #assume that
    #K . . . . . . . . . . . a known maze
    #shortest_distances . . .a default dictionary with default value float('inf') 
    # . . . . . . . . . . . . . . that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #new_edge_distance. . . .the new_distance of the node.
    #returns shortest distances after updating it.
    node1,node2 = new_edge
    shortest_distances[(node1,node2)] = min(shortest_distances[(node1,node2)], new_edge_distance)
    for x in K.explored.nodes:
        shortest_distances[(x,x)] = 0
    for x in K.explored.nodes:
            for y in K.explored.nodes:
                x_edge_y_dist = shortest_distances[(x,node1)] + new_edge_distance + shortest_distances[(node2,y)] #shortest distance from x to the edge then to y.
                y_edge_x_dist = shortest_distances[(x,node2)] + new_edge_distance + shortest_distances[(node1,y)] #shortest distance from x to the edge backwards, then to y.
                shortest_distances[(x,y)] = min(shortest_distances[(x,y)],shortest_distances[(y,x)], x_edge_y_dist, y_edge_x_dist)
                shortest_distances[(y,x)] = shortest_distances[(x,y)]
    return shortest_distances
def recover_path_from_shortest_distances(K,shortest_distances,node1,node2):
    #Parameters
    #K . . . . . . . . . . . . a known maze.
    #shortest_distances. . . . a default dictionary with default value float('inf')
    # . . . . . . . . . .that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #node1 and node2 are nodes of K, strings.
    #returns a list of vertices [node1, ..., node2] that is the shortest path in K.
    current_distance = shortest_distances[(node1,node2)]
    if current_distance==float('inf'): #If the distance is infinite...
         assert False #this should not happen.
         return None #Then there is no path from node1 to node2
    else:
        to_return = []
        current_node = node1
        while current_node != node2:
            for next_node in K.explored.neighbors(current_node):
                 if abs(shortest_distances[(next_node,node2)] - current_distance + K.M.edge_length(current_node,next_node))<0.0001: #We look for the next_node that is the appropriate step to take from current_node.
                    to_return.append(current_node)
                    current_node = next_node
                    current_distance = shortest_distances[(next_node,node2)]
                    break
        to_return.append(node2)
        return to_return
    
