import itertools

def update_shortest_known_path(K,shortest_known_path,new_edge,new_edge_distance):
    #assume that
    #K . . . . . . . . . . . a known maze
    #shortest_known_path . . a default dictionary with default value infinity
    # . . . . . . . . . . . .that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #new_edge_distance. . . .the new_distance of the node.
    #returns shortest_known_path after updating it.
    node1,node2 = new_edge
    shortest_known_path[(node1,node2)] = min(shortest_known_path[(node1,node2)], new_edge_distance)
    for x in K.explored.nodes:
        shortest_known_path[(x,x)] = 0
    for x in K.explored.nodes:
            for y in K.explored.nodes:
                x_edge_y_dist = shortest_known_path[(x,node1)] + new_edge_distance + shortest_known_path[(node2,y)] #shortest distance from x to the edge then to y.
                y_edge_x_dist = shortest_known_path[(x,node2)] + new_edge_distance + shortest_known_path[(node1,y)] #shortest distance from x to the edge backwards, then to y.
                shortest_known_path[(x,y)] = min(shortest_known_path[(x,y)],shortest_known_path[(y,x)], x_edge_y_dist, y_edge_x_dist)
                shortest_known_path[(y,x)] = shortest_known_path[(x,y)]
    return shortest_known_path
def recover_path_from_shortest_known_path(K,shortest_known_path,node1,node2):
    #Parameters
    #K . . . . . . . . . . . . a known maze.
    #shortest_known_path. . . . a default dictionary with default value float('inf')
    # . . . . . . . . . .that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #node1 and node2 are nodes of K, strings.
    #returns a list of vertices [node1, ..., node2] that is the shortest path in K from node1 to node2
    current_distance = shortest_known_path[(node1,node2)]
    if current_distance==float('inf'): #If the distance is infinite...
         #assert False #this should not happen.
         return None #Then there is no path from node1 to node2
    else:
        to_return = []
        current_node = node1
        while current_node != node2:
            for next_node in K.explored.neighbors(current_node):
                 if abs(shortest_known_path[(next_node,node2)] - current_distance + K.M.distance(current_node,next_node))<0.0001: #We look for the next_node that is the appropriate step to take from current_node.
                    to_return.append(current_node)
                    current_node = next_node
                    current_distance = shortest_known_path[(next_node,node2)]
                    break
        to_return.append(node2)
        return to_return

def shortest_path_involves_edge(K,shortest_known_path,edge,node1,node2):
    v,w = edge
    if shortest_known_path[node1,node2] == shortest_known_path[node1,v] + K.M.distance(v,w) + shortest_known_path[w,node2]:
        return True
    if shortest_known_path[node1,node2] == shortest_known_path[node1,w] + K.M.distance(v,w) + shortest_known_path[v,node2]:
        return True
    return False
def find_affected_paths(K,shortest_known_path, edge, new_edge_distance):
    #assume edge = (v,w)
    #Returns found, a list of vertices whose shortest path to w includes edge, 
    # and frontier, the nodes adjacent to the found nodes.
    #This method should work before and after shortest_known path is updated with the edge.
    v,w = edge
    current = v
    previous = []
    found = []
    frontier = []
    while True:
        path_length_with_edge = new_edge_distance + shortest_known_path[current, v]
        if (shortest_known_path[current,w] - path_length_with_edge)>-0.001: #if the shortest path from current to w involves the new edge...
            next_choices = [node for node in K.explored.neighbors(current) if (not node in found) and not (node in frontier) and (node != w)]

            if current == v and len(next_choices)==0:
                assert len(set(found)& set(frontier))==0
                if current not in found:
                    found.append(current)
                return found, frontier
            else:
                if not current in found:
                    found.append(current)
                if len( next_choices )>0:
                    previous.append(current)
                    current = next_choices[0]
                else:
                    current = previous.pop()

        else:
            if current not in frontier:
                frontier.append(current)
            current = previous.pop()

def update_shortest_known_path_faster(K,shortest_known_path, new_edge, new_edge_distance):
    #Same behavior as update_shortest_known_path, but should run faster.
    #Assume that
    #K . . . . . . . . . . . . a known maze
    #shortest_known_path . . . a default dictionary with default value infinity
    # . . . . . . . . . . . . .that has pairs (node1,node2) as keys and shortest distances through the graph as values.
    #new_edge . . . . . . . . .An edge to add to the graph.
    #new_edge_distance. . . . .the new_distance of the node.
    #returns shortest distances after updating it.
    v,w = new_edge
    Dv, _ = find_affected_paths(K,shortest_known_path, (v,w), new_edge_distance)
    Dw, _ = find_affected_paths(K,shortest_known_path, (w,v), new_edge_distance)
    assert v in Dv and w in Dw
    for x,y in itertools.product(Dv,Dw):
        shortest_known_path[x,y]= min(shortest_known_path[x,y], shortest_known_path[x,v] + new_edge_distance + shortest_known_path[w,y])
        shortest_known_path[y,x]=shortest_known_path[x,y]
    return shortest_known_path



def update_shortest_known_path_remove_edge(K,shortest_known_path,old_edge,old_edge_distance):
    v,w = old_edge
    Dv, Fv = find_affected_paths(K,shortest_known_path, (v,w), old_edge_distance)
    Dw, Fw = find_affected_paths(K,shortest_known_path, (w,v), old_edge_distance)
    frontier_to_update = [node for node in Fv if node in Dw] #These nodes might have incorrect distances to Dv
    stable_frontier = [node for node in Fv if not node in frontier_to_update] #These nodes already have the correct distances to the nodes of Dv.
    
    sub_frontier = [] #sub_frontier is the nodes in Dv next to frontier to update.
    for node in frontier_to_update:
        for neighbor in K.explored.neighbors(node):
            if neighbor in Dv:
                sub_frontier.append(neighbor)

    sub_frontier.extend(stable_frontier)
    #Update the shortest paths to frontier to update.
    for x in Dv:
        for f in frontier_to_update:
            shortest_known_path[x,f] = min([shortest_known_path[x,z] + shortest_known_path[z,f] for z in sub_frontier])
            shortest_known_path[f,x] = shortest_known_path[x,f]

    for x in Dv:
        for y in Dw:
            shortest_known_path[x,y] = min([shortest_known_path[x,f]+shortest_known_path[f,y] for f in Fv])
            shortest_known_path[y,x]=shortest_known_path[x,y]
    return shortest_known_path