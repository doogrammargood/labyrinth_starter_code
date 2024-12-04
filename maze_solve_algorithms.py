#this file contains the algorithms used in solving the maze
from maze import *
import time
import scipy.optimize
def depth_first_search_choice(Theseus, string):
    #expects Theseus to be a hero, whose location is a node.
    #string is a list of nodes starting from the entrance to the current location.
    #returns the string after the hero makes his next step.
    #TODO
    pass
def depth_first_search(Theseus):
    #Theseus is a hero. draws the progress as a side effect.
    #expects drawing to be an instance of the graph_drawer class.
    #TODO
    pass

def a_star_search(Theseus):
    #implements the A* algorithm to search the graph for the exit.
    #Consider using Theseus.K.unexplored_nodes() to get the edges that lead to a node on the frontier.
    #TODO
    pass

def linear_programming_shortest_path(M,node1,node2):
    #Assume M is a maze. We assume that we know the whole maze for this method.
    #We write the shortest path as a linear program.
    #TODO define A,b,c in terms of M.G
    #See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    result = scipy.optimize.linprog(np.array(c),A_eq=np.array(A), b_eq = np.array(b), bounds = (0,1), method = 'highs')
    return(result['fun'])
