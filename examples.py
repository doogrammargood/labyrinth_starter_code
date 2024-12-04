#This file contains some examples
from maze_solve_algorithms import *
graph_names = [f"maze_graphs/maze{i}.graphml" for i in [1,2,3]]

def run_all_dfs():
    #runs dfs on all of the graph mazes and displays it.
    for file in graph_names:
        M=maze(filename=file)
        K=known_maze(M)
        Theseus=hero(K)
        depth_first_search(Theseus)
def run_all_a_star():
    #runs A* on all the graph mazes and displays it.
    for file in graph_names:
        M=maze(filename=file)
        K=known_maze(M)
        Theseus=hero(K)
        a_star_search(Theseus)
def text_explore():
    #provides a text-based interface to explore the maze.
    #Could be useful to get a feel for the functions available.
    M= maze(filename="maze_graphs/maze3.graphml")
    K=known_maze(M)
    Theseus= hero(K)

    vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus)
    drawing = graph_drawer(M.G, M.pos, vertex_color_dict, edge_color_dict)
    while(Theseus.location != M.exit):
        Theseus.ponder_choices()
        Theseus.make_choice()
        vertex_color_dict,edge_color_dict = graph_drawer.get_graph_colors(M,Theseus)
        drawing.recolor_graph(vertex_color_dict, edge_color_dict)
if __name__=="__main__":
    run_all_dfs()
    #run_all_a_star()