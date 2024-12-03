#this file contains the algorithms used in solving the maze
from maze import *
import time
def depth_first_search_choice(K, string):
    #expects K to be a known maze and Theseus to be a hero, whose location is a node.
    #string is a list of nodes starting from the entrance to the current location.
    #returns the string after the hero makes his next step.
    node= string[-1]
    unexplored_choices = [choice for choice in range (K.M.get_degree_of_node(node) ) if choice not in K.explored_choices[node] ]
    if len(unexplored_choices)>0:
        string.append(K.M.get_neighbor_from_number(node, unexplored_choices[0]))
        return string
    else: #unwind the string, taking a step back.
        string.pop()
        return string

    
def depth_first_search(Theseus,drawing):
    #Theseus to be a hero. draws the progress as a side effect.
    #expects drawing to be an instance of the graph_drawer class.
    M = Theseus.K.M
    string = [Theseus.location] #Tie string to entrance.
    while Theseus.location != M.exit:
        string = depth_first_search_choice(K,string)
        Theseus.explore_node(string[-1])
        vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus)
        for vertex in string:
            if vertex != Theseus.location:
                vertex_color_dict[vertex]=2
        drawing.recolor_graph(vertex_color_dict, edge_color_dict)
        plt.pause(0.1)
    print("exit found.")
    Theseus.print_stats()
    time.sleep(10)

def a_star_search(Theseus,drawing):
    #implements the A* algorithm to search the graph for the exit.
    M=Theseus.K.M
    def heuristic(node):
        return K.shortest_distances[(M.entrance,node)] + M.edge_length(node,M.exit)
    while Theseus.location!=M.exit:
        vertices_and_neighbor_number, edge_info = K.unexplored_edges()
        v, i = min(vertices_and_neighbor_number, key=lambda e: heuristic(M.get_neighbor_from_number(*e)))
        Theseus.travel_to_node(v)
        Theseus.explore_edge(i)
        vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus,K.explored)
        drawing.recolor_graph(vertex_color_dict, edge_color_dict)
        plt.pause(0.25)


M= maze(filename="maze_graphs/maze3.graphml")
K=known_maze(M)
Theseus=hero(K)
vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus)
drawing = graph_drawer(M.G, M.pos, vertex_color_dict, edge_color_dict)
plt.pause(0.1)
a_star_search(Theseus,drawing)