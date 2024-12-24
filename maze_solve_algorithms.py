#this file contains the algorithms used in solving the maze
from maze import *
import scipy.optimize
from heapq import heapify, heappush, heappop

def depth_first_search_choice(Theseus, string):
    #expects Theseus to be a hero, whose location is a node.
    #string is a list of nodes starting from the entrance to the current location.
    #returns the string after the hero makes his next step.
    '''
    Use:
    Theseus.K.frontier_edges() . . . .A list of edges (v,w), where v has been explored but w has not
    Theseus.location . . . . . . . . . .The current node where Theseus is.
    Theseus.K.explored.nodes . . . . . .The nodes that Theseus has explored.
    '''
   pass

    
def depth_first_search(Theseus):
    #Theseus is a hero.
    #expects drawing to be an instance of the graph_drawer class.
    '''
    Use:
    Theseus.location. . . . . . The node where Theseus is.
    Theseus.explore_node(node) .Moves Theseus to node, if it is a neighbor of his location. Has side effects on K and updates the drawing.
    depth_first_search_choice . Defined above
    '''
    pass

def a_star_search(Theseus):
    #implements the A* algorithm to search the graph for the exit.
    '''
    Use: 
    M.entrance . . . . . . . . . . . . . . The node of M that is an entrance.
    M.exit . . . . . . . . . . . . . . . . The node of M that is an exit.
    Theseus.travel_to_node(node) . . . . . Takes Theseus to the node v along the shortest path through K.explored.
    Theseus.explore_node(node) . . . . . . Moves Theseus to node, if it is a neighbor of his location. Has side effects on K and updates the drawing.
    K.frontier_edges() . . . . . . . . . . Returns a list of pairs (v,w) where v has been explored but w has not.
    '''
    M=Theseus.K.M
    K=Theseus.K
    def cost_estimate(v,w):
        #Returns an estimate of the cost of exploring node w through its already-explored neighbor, v.
        '''
        Use:
            K.shortest_known_path . . . . . . . . .A default dictionary whose keys are pairs of nodes (v,w) and whose value is the length of the shortest path through K.explored from v to w.
            M.distance(node1, node2) . . . . . . . Calculates the Euclidean distance between 2 nodes.
        '''
        pass
    pass
def linear_programming_shortest_path(M,node1,node2):
    #Assume that M is a maze. We assume access to the whole maze for this method.
    #Assume that node1 and node2 are nodes of M.D.
    '''
    Use: 
        basic list operations. . . .append, copy.
        M.D.nodes. . . . . . . . . .An iterable of the nodes.
        M.D.edges . . . . . . . . . An iterable of the edges of D. 
    '''
    #We write the shortest path as a linear program.
    #The variables are directed edge of M.D
    
    #See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    result = scipy.optimize.linprog(np.array(c),A_eq=np.array(A), b_eq = np.array(b), bounds = (0,1), method = 'highs')
    return(result['fun'])