#this file contains the algorithms used in solving the maze
from maze import *
import time
import scipy.optimize
def depth_first_search_choice(Theseus, string):
    #expects Theseus to be a hero, whose location is a node.
    #string is a list of nodes starting from the entrance to the current location.
    #returns the string after the hero makes his next step.
    unexp = [w for v,w in  Theseus.K.unexplored_nodes() if v==Theseus.location in Theseus.K.explored.nodes]

    if len(unexp)>0:
        string.append(unexp[0])
        return string
    else: #unwind the string, taking a step back.
        string.pop()
        return string

    
def depth_first_search(Theseus):
    #Theseus is a hero. draws the progress as a side effect.
    #expects drawing to be an instance of the graph_drawer class.
    M = Theseus.K.M
    string = [Theseus.location] #Tie string to entrance.
    while Theseus.location != M.exit:
        string = depth_first_search_choice(Theseus,string)
        if not Theseus.drawing is None:
            Theseus.drawing.marked_nodes = string
        Theseus.explore_node(string[-1])
    #print("exit found.")
    #Theseus.print_stats()

def a_star_search(Theseus):
    #implements the A* algorithm to search the graph for the exit.
    M=Theseus.K.M
    K=Theseus.K
    def heuristic(v,node):
        if K.shortest_distances[(M.entrance,node)]==float('inf'):
            return K.shortest_distances[(M.entrance,v)] + M.edge_length(v,node)+ M.edge_length(node,M.exit)
        return K.shortest_distances[(M.entrance,node)] + M.edge_length(node,M.exit)
    while Theseus.location!=M.exit:
        unexp = K.unexplored_nodes()
        v, neighbor = min( unexp, key=lambda e: heuristic(e[0],e[1]))
        Theseus.travel_to_node(v)
        Theseus.explore_node(neighbor)
    #Theseus.print_stats()

def linear_programming_shortest_path(M,node1,node2):
    #Assume M is a maze. We assume that we know the whole maze for this method.
    #We write the shortest path as a linear program.

    #The edges are directed edge of M.D
    variable_list = [] #a list of all the variables.
    for e in M.D.edges:
        variable_list.append(e)
        variable_list.append((e[1],e[0]))
    A= []
    for v in M.D.nodes: #enforce the flow constraint for all nodes, except the entrance/exit.
        constraint = []
        if v != node1 and v!= node2: #Other than the entrance and exit...
            for edge in variable_list: #The amount of path going in is equal to the amount of path going out of each node.
                if edge[0] == v:
                    constraint.append(1) #amount of path going in
                elif edge[1] == v:
                    constraint.append(-1) #amount of path going out.
                else:
                    constraint.append(0)
            A.append(constraint.copy())
    

    #enforce the constraint that the flow into the entrance is 0.
    constraint = []
    for edge in variable_list:
        if edge[1] == node1:
            constraint.append(1)
        else:
            constraint.append(0)
    A.append(constraint.copy())
    #enforce the constraint that the flow out of the entrance is 1.
    constraint = []
    for edge in variable_list:
        if edge[0] == node1:
            constraint.append(1)
        else:
            constraint.append(0)
    A.append(constraint.copy())

    c = [M.edge_length(edge[0],edge[1]) for edge in variable_list]#Edges are weighted by their lengths.
    b = [0]*(len(M.D.nodes)-1) + [1]

    #See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    result = scipy.optimize.linprog(np.array(c),A_eq=np.array(A), b_eq = np.array(b), bounds = (0,1), method = 'highs')
    return(result['fun'])
    #The values of the 

if __name__=="__main__":
    M= maze(filename="maze_graphs/maze3.graphml",reopen_edges = float('inf'))
    linear_programming_shortest_path(M,M.entrance,M.exit)
    # K=known_maze(M)
    # Theseus=hero(K)
    # vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus)
    # drawing = graph_drawer(M.G, M.pos, vertex_color_dict, edge_color_dict)
    # plt.pause(0.1)
    #a_star_search(Theseus,drawing)
    #depth_first_search(Theseus,drawing)
    #linear_programming_shortest_path(M)