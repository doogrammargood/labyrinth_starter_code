#This file contains some algorithms needed to for the maze program.
#TODO: implement the Fisher Shuffle and Kruskal's algorithm to return

def update_shortest_distances(K,shortest_distances,new_edge,new_edge_distance):
    #assume that
    #K . . . . . . . . . . . a known maze
    #shortest_distances . . .a default dictionary with default value float('inf') 
    # . . . . . . . . . . . . . . that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #new_edge_distance. . . .the new_distance of the node.
    #returns none
    node1,node2 = new_edge
    for x in K.explored.nodes:
            for y in K.explored.nodes:
                if x == y:
                    shortest_distances[(x,y)] = 0
                else:
                    x_edge_y_dist = shortest_distances[(x,node1)] + new_edge_distance + shortest_distances[(node2,y)] #shortest distance from x to the edge then to y.
                    y_edge_x_dist = shortest_distances[(x,node2)] + new_edge_distance + shortest_distances[(node1,y)] #shortest distance from x to the edge backwards, then to y.
                    shortest_distances[(x,y)] = min(shortest_distances[(x,y)], x_edge_y_dist, y_edge_x_dist)
    return shortest_distances
def recover_path_from_shortest_distances(K,shortest_distances,node1,node2):
    #Parameters
    #K . . . . . . . . . . . . a known maze.
    #shortest_distances. . . . a default dictionary with default value float('inf')
    # . . . . . . . . . .that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #node1 and node2 are nodes of K, strings.
    #returns a list of vertices [node1, ..., node2] that is the shortest path in K.
    current_distance = shortest_distances(node1,node2)
    if current_distance==float('inf'): #If the distance is infinite...
         return None #Then there is no path from node1 to node2
    else:
        to_return = []
        current_node = node1
        while current_node != node2:
            for next_node in K.explored.neighbors(current_node):
                 if shortest_distances([next_node,node2])== current_distance - K.M.edge_length(current_node,next_node): #We look for the next_node that is the appropriate step to take from current_node.
                    to_return.append(current_node)
                    current_node = next_node
                    current_distance = shortest_distances([next_node,node2])
        to_return.append(node2)
        return to_return