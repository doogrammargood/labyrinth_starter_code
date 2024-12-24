#This file contains the classes maze and known_maze for the final project for CMPS2200 intro to algorithms.
from draw_and_parse_graph import *
from maze_design_algorithms import *
from shortest_path_functions import *
import math
import csv
import random

class DistanceDefaultDict(defaultdict):
    #This class is used to keep track of the distances between all pairs of vertices.
    #The keys are pairs of nodes. The values are the distances of the shortest paths between the nodes.
    def __missing__(self, key):#We fill in missing keys by default: if the two nodes are equal, the distance is 0. Otherwise, we initialize the distance to infinite.
        self[key] = 0 if key[0] == key[1] else float('inf')
        return self[key]
    def __eq__(self, other): #Overwrite equality to use the default value. Warning: This means that checking for equality mutates instances of this object.
        if not isinstance(other, DistanceDefaultDict):
            return False
        for key in set(self.keys())| set(other.keys()): #Two DistanceDefaultDict 's are equal if every key of one has the appropriate value in the other.
            if self[key]==other[key]==float('inf'):
                continue
            elif abs(self[key] - other[key])> 0.0001:
                print("key value", key, self[key],other[key])
                return False
        return True

class maze(object):
    '''
    The maze class contains: 
        G . . . . . . a Networkx graph that has nodes for all of the rooms.
        pos . . . . . a dictionary from nodes of G to points in the plane that makes G planar.
        S . . . . . . a subgraph of G that represents the pathways that are open.
        D . . . . . . a Networkx graph that has all of the nodes of D, plus nodes for the deadends.
        posD . . . . .a dictionary from nodes of D to points in the plane. Extends pos with additional keys for the nodes of D
        edgeD. . . . .a dictionary from nodes of D to the corresponding edges of G-S.
        max_edge_length The length of the longest edge.
        entrance . . .The name of the node that represents the entrance.
        exit . . . . .The name of the node that represents the exit.
    '''
    def __init__(self, filename=None, reopen_edges=0):
        #filename is the graphml file that represents the graph.
        #reopen_edges is an integer that tells how many edges to open beyond the edges of a random spanning tree.
        if not filename is None:
            self.G, self.pos = parse_graph(filename)
        #self.S = nx.random_spanning_tree(self.G)
        self.S = random_spanning_tree(self.G)
        self.S = nx.Graph(self.S)
        reopen_edges = min(reopen_edges, len(self.G.edges)-len(self.S.edges))
        edges = random.sample([e for e in self.G.edges if not e in self.S.edges],reopen_edges)
        self.S.add_edges_from(edges)
        self.entrance = "n1"
        self.exit = "n"+ str(self.G.number_of_nodes())
        self.D=nx.Graph()
        self.update_D()
        self.max_edge_length = max([self.distance(v,w) for v,w in self.G.edges])

    def update_D(self):
        #updates the graph D by using G and S to place all of the deadends.
        #also updates posD and edgeD
        self.D = self.G.copy() #copy G
        self.D.remove_edges_from([e for e in self.G.edges if not e in self.S.edges])#remove the closed edges
        self.posD = self.pos.copy()
        self.edgeD=defaultdict()
        counter = 1 #counter to generate the names of the deadends
        for e in self.G.edges:
            if e not in self.S.edges: #loop through the closed edges
                midpoint= self.edge_midpoint(e)
                new_node_name = "d,"+str(e[0]) +"," + str(e[1])
                self.add_node_to_D(new_node_name, midpoint, [e[0]])
                self.posD[new_node_name]=midpoint
                self.edgeD[new_node_name] = tuple(sorted((e[0],e[1])))
                counter += 1
                new_node_name = "d"+str(e[0]) +"," + str(e[1])
                self.add_node_to_D(new_node_name, midpoint, [e[1]])
                self.posD[new_node_name]=midpoint
                self.edgeD[new_node_name] = tuple(sorted((e[0],e[1])))
                counter += 1


    
    def add_node_to_D(self, new_node, position, neighbors):
        #new_node is a string that is the name of this node.
        #position is a tuple of floats.
        #neighbors is a list of strings that represents the nodes that new_node is adjacent to. Assume these are open edges
        #returns None.
        self.D.add_node(new_node)
        self.pos[new_node]=position
        self.D.add_edges_from([(new_node, neighbor) for neighbor in neighbors])

    def get_degree_of_node(self,node):
        #Expects node to be a string, the name of a node.
        #Returns the degree of the node.
        #We number the neighbors of the node by 0,1,...,degree-1 by starting from the right and moving counterclockwise.
        return self.D.degree(node)
    
    def distance(self,node1,node2):
        #Assumes node1 and node2 are strings that represent nodes.
        #Returns the Euclidean distance between the nodes. The distance is a float.
        node1_x, node1_y = self.pos[node1]
        node2_x, node2_y = self.pos[node2]
        return ((node2_x - node1_x)**2 + (node2_y - node1_y)**2)**0.5
    def edge_midpoint(self,e):
        #Assumes e is an edge (a 2-tuple of nodes).
        #returns the midpoint of the edge between the nodes, a float.
        node1,node2=e
        node1_x, node1_y = self.pos[node1]
        node2_x, node2_y = self.pos[node2]
        return ((node1_x+node2_x)/2, (node1_y+node2_y)/2)
    
    def edge_angle(self, node1,node2):
        #Assumes node1 and node 2 are strings that represent nodes.
        #Returns the angle between nodes. Between 0 and 2pi, zero being when node2 is to the right of node1
        node1_x, node1_y = self.pos[node1]
        node2_x, node2_y = self.pos[node2]
        y = node2_y - node1_y
        x= node2_x - node1_x
        angle = math.atan2(y,x) #Returns an angle between -pi and pi. See https://docs.python.org/3/library/math.html#math.atan2
        if angle <0:
            angle = 2*math.pi+angle
        return angle
    
    def get_neighbor_from_number(self, node,neighbor_number):
        #Assume node is a string representing a node.
        #Assume neighbor number is a number between 0 and the degree of node -1.
        #Returns the neighbor_number-th neighbor of node, counting counterclockwise from the right.
        neighbors = list(self.D.neighbors(node))
        neighbors.sort(key= lambda neighbor: self.edge_angle(node, neighbor))
        return neighbors[neighbor_number]
    
    def get_number_from_neighbor(self, node1,node2):
        #returns a number n such that node2 is the nth neighbor of node1.
        for n in range(self.get_degree_of_node(node1)):
            if node2 == self.get_neighbor_from_number(node1,n):
                return n

    def to_csv(self, filename):
        #saves the graph G and S as a CSV.
        #the nodes take up 3 columns of the first several rows. (node_name, x_coord,y_coord)
        #Then a spacer "----"
        #Then there are the edges of S that take up the next several rows (node1,node2)
        #Then another spacer "+++++"
        #Then the edges of G that are not in S, the closed edges.
        try:
            # Open the file in write mode
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for node_name in self.pos: #write the nodes.
                    x,y =self.pos[node_name]
                    writer.writerow([node_name, x,y])
                writer.writerow("----")
                for node1,node2 in self.S.edges: #write the opened edges.
                    writer.writerow([node1,node2])
                writer.writerow("+++++")
                for node1,node2 in self.G.edges: #write the closed edges
                    if self.check_edge(node1,node2)=="closed":
                        writer.writerow([node1,node2])
            print(f"Data successfully written to {filename}")
        except Exception as e:
            print(f"Error writing to file: {e}")

#Students may need the function frontier_edges.
class known_maze(maze):
    '''
    The known maze class contains
    M . . . . . . . . . . The maze that we're exploring.
    explored . . . . . .  The graph that has been explored. A subgraph of M's graph D.
    exit_location . . . . An ordered pair of floats that represents location of the exit. If unknown, set to None.
    pos . . . . . . . . . A dictionary of the positions of the rooms that have been found.
    heros . . . . . . . . A list of heros exploring the maze.
    explored_choices . .  A default dictionary from nodes of G to lists of integers. Represents the choices that have been explored.
    shortest_known_path . A default dictionary from pairs of vertices to distances.
    '''
    def __init__(self,M):
        #Assume M is a maze.
        self.M = M
        self.explored = nx.Graph()
        self.explored.add_node(M.entrance) #add the entrance
        self.pos = {self.M.entrance: self.M.pos[self.M.entrance]}#we know where the entrance is
        self.explored_choices = defaultdict(list) #default dict: when a key is not in the dictionary, it initializes it as an empty list.
        self.shortest_known_path = DistanceDefaultDict() #by default, all distances are infinity, except between a node and itself, which is initialized to 0.
    def add_edge(self, node1,node2):
        #assume node1 and node2 are strings that represent adjacent nodes in the maze M.
        #We add the edge to our known maze.
        #This should be idempotent, so that if we try to add the same edge twice nothing new happens.
        self.pos[node1]=self.M.pos[node1]
        self.pos[node2]=self.M.pos[node2]
        self.explored.add_edge(node1,node2)

        #update shortest_known_path
        self.shortest_known_path = update_shortest_known_path_faster(self,self.shortest_known_path,(node1,node2), self.M.distance(node1,node2))

    def remove_edge(self, node1,node2):
        self.shortest_known_path = update_shortest_known_path_remove_edge(self,self.shortest_known_path, (node1,node2), self.M.distance(node1,node2))
        self.explored.remove_edge(node1,node2)
    def learn_all_edges(self):
        for edge in self.M.D.edges:
            self.add_edge(edge[0],edge[1])

    def unexplored_edges(self):
        #returns a list of pairs (node1,i) and a dictionary,edge_info.
        #the pairs are pairs of vertex/neighbor_number that have not been explored.
        #edge_info has these pairs as its keys and the (node2,l) as its values, where l is the length of the edge and node2 is the neighbor.
        pairs_to_return=[]
        for v in self.explored.nodes:
            for i in range(self.M.get_degree_of_node(v)):
                if not i in self.explored_choices[v]:
                    pairs_to_return.append((v,i))
        edge_info=defaultdict(list)
        for v,i in pairs_to_return:
            node2=self.M.get_neighbor_from_number(v,i)
            length = self.M.distance(v,node2)
            edge_info[(v,i)] = (node2,length)
        return pairs_to_return,edge_info
    
    def frontier_edges(self):
        #returns a list of edges (node1,node2) such that node1 has been explored but node2 has not.
        pairs, info = self.unexplored_edges()
        return [ (v, info[(v,i)][0]) for v,i in pairs if not info[(v,i)][0] in self.explored.nodes]

#Students may need the functions explore_edge, explore_node (calls_explore_edge), and travel_to_node.
class hero(object):
    '''
    The hero class contains
    K . . . . . . . . . . .A known maze, that represents the part of the maze that the hero has explored.
    location . . . . . . . Either a node, 
    . . . . . . . . . . . . . or a tuple (node1,node2,progress) where (node1,node2) is an edge of the graph and progress is a float in [0,1] that represents how far along the edge the hero is.
    . . . . . . . . . . . . . When progress=0, they've only just started along the path from node1 to node2. When progress is 1, they're at node2.
    speed . . . . . . . . .The speed at which the hero travels
    drawing . . . . . . . .A graph_drawer instance for drawing the graph.
    ----- Metric attributes----- (the following attributes are different ways to measure how much effort has been spent)
    travel_distance . . . .The total distance the hero has traveled.
    exploration_distance . The total distance the hero has explored (not counting backtracking).
    deadends_encountered . The total number of deadends that the hero has encountered.
    '''
    def __init__(self,K,draw = True, location=None,speed=1.0,travel_distance=0.0,exploration_distance=0.0,dead_ends_encountered = 0):
        #Assume K is a known maze.
        #draw is a boolean that decides whether to draw the graph or not.
        #location is a string that represents a node in the maze, where the hero spawns.
        #speed is a float that represents how fast the hero moves.
        #the other arguments are the hero's metric attributes.
        self.K = K

        if location is None:
            self.location = K.M.entrance #By default, put the hero at the entrance.
        else:
            self.location = location
        self.speed = speed
        self.travel_distance=travel_distance
        self.exploration_distance=exploration_distance
        self.dead_ends_encountered = dead_ends_encountered
        if isinstance(draw, bool) and draw:
            self.drawing = graph_drawer(self)
        else:
            self.drawing = None

    def time_til_arrival(self):
        #returns the time until reaching the next node.
        if isinstance(self.location, tuple): #if they're on an edge...
            node1,node2,progress = self.location
            length = self.K.M.distance(node1,node2)
            return length * (1- progress)
        else:
            return 0
        
    #This function is complicated because I want to allow multiple heros, and 
    #I want to know exactly where each hero is every time a hero is at a node.
    #So that the process can be animated.
    
    def update_location(self,time_elapsed):
        #expects time_elapsed to be a nonnegative float.
        #The hero moves along its edge if it is on an edge.
        #Otherwise, if they're on a node, they stay still.
        if isinstance(self.location, tuple): #if they're on an edge...
            node1, node2, progress = self.location #unpack the location.
            edge_distance = self.K.M.distance(node1,node2) #the distance of the edge.
            current_distance = edge_distance*progress #how far along the edge the hero currently is.
            new_distance =  min(current_distance + self.speed*time_elapsed, edge_distance) #take the min because the hero cannot travel farther than the edge distance.
            self.location = (node1,node2,new_distance/edge_distance)
            self.update_metric_attributes(current_distance, new_distance)
            self.enter_node()
        else:
            print("Hero is waiting at ", self.location) #this should never happen.
    def update_metric_attributes(self,current_distance,new_distance):
        #This function should only be called within the function 'update location'
        #current_distance is the distance before updating the location.
        #new_distance is the distance after updating the location.
        #returns None.
        node1,node2, progress = self.location
        self.travel_distance += new_distance - current_distance
        if not self.K.explored.has_edge(node1,node2):#if we haven't explored this edge before...
            self.exploration_distance += new_distance-current_distance
        if progress ==1.0 and self.K.M.get_degree_of_node(node2)==1: #if we hit a deadend,
            self.dead_ends_encountered += 1 #increment the deadend counter.
  
    def enter_node(self):
        #if the hero is on an edge but is ready to enter a node, then we call this function to put them on the node
        #Updates explored choices.
        #redraws the graph
        #returns None.
        if isinstance(self.location,tuple):#if the hero is on an edge
            node1,node2,progress = self.location #unpack the location.
            if progress == 1: #if the hero has traversed the entire edge...
                self.location = node2 #put them at the second node.
                #update_explored_choices              
                n = self.K.M.get_number_from_neighbor(node1,node2)
                if n not in self.K.explored_choices[node1]:
                    self.K.explored_choices[node1].append(n)
                m = self.K.M.get_number_from_neighbor(node2,node1)
                if m not in self.K.explored_choices[node2]:
                    self.K.explored_choices[node2].append(m)
                self.K.add_edge(node1,node2) #we've now explored this edge.
                if not self.drawing is None:
                    self.drawing.update_graph(self.K.M.distance(node1,node2)/self.K.M.max_edge_length)


    def enter_edge(self, neighbor_number):
        #Moves a hero from a node to an incident edge.\
        assert isinstance(self.location, str) #The hero can only enter an edge if they're at a node
        node2 = self.K.M.get_neighbor_from_number(self.location, neighbor_number)
        node1 = self.location
        self.location = (node1,node2,0.0)

    def explore_edge(self,neighbor_number):
        #Moves a hero from one node to its neighbor, exploring the edge between.
        #This is only useful if there's only one hero.
        assert isinstance(self.location, str) #The hero can only explore an edge if they're at a node
        self.enter_edge(neighbor_number)
        time = self.time_til_arrival()
        self.update_location(time)
        assert isinstance(self.location, str) #we should be at the next node after this.

    def explore_node(self, neighbor):
        #moves a hero to neighbor.
        if self.location==neighbor:#we're already there.
            return
        assert self.K.M.D.has_edge(neighbor, self.location) #be sure that there's actually an edge here.
        neighbor_number = self.K.M.get_number_from_neighbor(self.location, neighbor)
        self.explore_edge(neighbor_number)

    def travel_to_node(self,node,drawing=None):
        #moves the hero to node via the shortest path.
        #recover_path_from_shortest_known_path(self, self.K.shortest_known_path, self.location, node)
        if self.location == node:
            return None
        path = recover_path_from_shortest_known_path(self.K,self.K.shortest_known_path, self.location, node)
        for p in path:
            self.explore_node(p)
            # if not self.drawing is None:
            #     self.drawing.update_graph()

    def coordinates(self):
        #returns the coordinates of the hero's location.
        if isinstance(self.location, str): #if the hero is at a node...
            return self.K.M.pos[self.location] #return the coordinates of that node.
        else: #otherwise, the hero is at a location represented by a tuple.
            node1,node2,progress = self.location
            node1_x, node1_y = self.K.M.pos[node1]
            node2_x, node2_y = self.K.M.pos[node2]

            return (node1_x * progress + (1-progress)*node2_x, node1_y * progress + (1-progress)*node2_y)
    
    def ponder_choices(self):
        print(f"Thesus is at {self.location} at {self.K.pos[self.location]}.")
        print(f"His choices are 0-{self.K.M.get_degree_of_node(self.location)-1}.")
        print(f"He has already explored options {self.K.explored_choices[self.location]}.")
        print(f"Where should he go next?")

    def make_choice(self):
        while True:
            try:
                n = int(input("Enter an integer: "))
            except ValueError:
                continue
            
            if n in range(self.K.M.get_degree_of_node(self.location)):
                self.explore_edge(n)
                return

    def print_stats(self):
        #prints the metric attributes.
        print(f"travel distance: {self.travel_distance}")
        print(f"exploration distance: {self.exploration_distance}")
        print(f"number of deadends: {self.dead_ends_encountered}")


if __name__=="__main__":
    pass