#this file contains the algorithms used in solving the maze
from maze import *
import scipy.optimize
def depth_first_search_choice(Theseus, string):
    #expects Theseus to be a hero, whose location is a node.
    #string is a list of nodes starting from the entrance and ending with Theseus.location.
    #If the hero is forced to backtrack, this function modifies string by removing its last element.
    #returns the string after the hero makes his next step. Does not actually cause Theseus to move.
    '''
    Use:
    Theseus.K.unexplored_nodes() . . . .A list of edges (v,w), where v has been explored but w has not
    Theseus.location . . . . . . . . . .The current node where Theseus is.
    Theseus.K.explored.nodes . . . . . .The nodes that Theseus has explored.
    '''
    pass
    
def depth_first_search(Theseus):
    #Theseus is a hero.
    #Performs a depth-first search by calling depth_first_search_choice to decide where to go next.
    #Maintains a string to know which node to backtrack to.
    '''
    Use:
    M.exit . . . . . . . . . . .The node that is the exit of M.
    Theseus.location. . . . . . The node where Theseus is.
    Theseus.explore_node(node) .Moves Theseus to node, if it is a neighbor of his location. Has side effects on K and updates the drawing.
    depth_first_search_choice . Defined above
    '''
    M = Theseus.K.M #The maze that Theseus is in.

def a_star_search(Theseus):
    #implements the A* algorithm to search the graph for M.exit.
    '''
    Use: 
    M.entrance . . . . . . . . . . . . . . The node of M that is an entrance.
    M.exit . . . . . . . . . . . . . . . . The node of M that is an exit.
    K.shortest_distances . . . . . . . . . A default dictionary whose keys are pairs of nodes (v,w) and whose value is the length of the shortest path through K from v to w.
    M.edge_length(node1,node2) . . . . . . Returns the distance between node1 and node2. They don't need to be adjacent.
    Theseus.travel_to_node(node) . . . . . Takes Theseus to the node, node along the shortest path through K, assuming that node is a vertex of K.nodes.
    Theseus.explore_node(node) . . . . . . Moves Theseus to node, if it is a neighbor of his location. Has side effects on K and updates the drawing.
    recover_path_from_shortest_distances. .See maze_design_algorithms
    '''
    M=Theseus.K.M
    K=Theseus.K
    def heuristic_cost(v,node):
        #Returns the value to minimize in the greedy choice: g(n)+h(n)
        #where g(n) is the length of the shortest known path from the entrance to n
        #and h(n) is the length of distance from n to the exit, as the crow flies.
        return None #modify this to return a number.
    #Theseus.print_stats()

def linear_programming_shortest_path(M,node1,node2):
    #Assume M is a maze. We assume that we know the whole maze for this method.
    #We write the shortest path as a linear program.

    #The edges are directed edges of M.D
    '''
    Use: M.D . . . . . the graph whose nodes are rooms (of the form "n{i}") or dead ends, of the form "d,n1,n2", where n1 and n2 are rooms. Edges are pathways between nodes.
     . . M.D.edges. . .An iteratable of the edges in the graph M.D
     . . M.D.nodes. . .An iterable of the nodes of the graph M.D
    basic list operations: append, and copy.

    Define a list-of-lists A and lists c and b to express the shortest path problem as a linear program.
    '''
    
    #See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    result = scipy.optimize.linprog(np.array(c),A_eq=np.array(A), b_eq = np.array(b), bounds = (0,1), method = 'highs')
    return(result['fun'])
