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
        Theseus.print_stats()
def run_all_a_star():
    #runs A* on all the graph mazes and displays it.
    for file in graph_names:
        M=maze(filename=file, reopen_edges=float('inf'))
        K=known_maze(M)
        Theseus=hero(K)
        a_star_search(Theseus)
        Theseus.print_stats()

def run_lp_shortest_paths():
    for i, file in enumerate(graph_names):
        M=maze(filename=file, reopen_edges=float('inf'))
        dist_to_exit = linear_programming_shortest_path(M,M.entrance,M.exit)
        print(f'When all edges are open, the shortest path to the exit of maze {i} is', dist_to_exit)
def text_explore():
    #provides a text-based interface to explore the maze.
    #Could be useful to get a feel for the functions available.
    M= maze(filename="maze_graphs/maze3.graphml")
    K=known_maze(M)
    Theseus= hero(K)
    while(Theseus.location != M.exit):
        Theseus.ponder_choices()
        Theseus.make_choice()
if __name__=="__main__":
    #run_all_dfs()
    run_all_a_star()
    #text_explore()
    #run_lp_shortest_paths()