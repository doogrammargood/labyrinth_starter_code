#This file contains methods for parsing graphs in the graphml format and drawing them.
#It was mostly written by ChatGPT.
from collections import defaultdict

import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def parse_graphml_with_positions(file_path):
    """Parse a Pigale-specific GraphML file and extract graph + positions."""
    # Parse the GraphML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespace for GraphML
    namespace = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
    
    # Initialize NetworkX graph and position dictionary
    G = nx.Graph()
    pos = {}
    
    # Iterate over nodes
    for node in root.findall(".//graphml:node", namespace):
        node_id = node.get("id")
        G.add_node(node_id)
        
        # Extract positional data
        for data in node.findall(".//graphml:data", namespace):
            if data.get("key") == "Pigale/V/":
                coords = data.text.split(",")
                if len(coords) == 2:  # Ensure valid format
                    x, y = map(float, coords)
                    pos[node_id] = (x, y)

    # Iterate over edges
    for edge in root.findall(".//graphml:edge", namespace):
        source = edge.get("source")
        target = edge.get("target")
        G.add_edge(source, target)
    
    return G, pos

class graph_drawer(object):
    #attributes are edges and nodes, both nx objects. Edges need to be sorted (n1,n2), where n1<n2 are strings.
    #and vertex_color_choices, edge_color_choices, a list of colors to paint the edges/vertices. 

    def __init__(self,G,pos,vertex_color_dict,edge_color_dict):
        #Assume G is a graph, pos is a dictionary from G to R^2 that give the positions of the nodes.
        #edge_color_dict is a dictionary from edges to integers that will be turned into colors.
        #vertex color dict has vertices as colors and integers as as values.
        self.G= G
        self.edge_color_choices = ["pink", "green","red"]
        self.vertex_color_choices = ["skyblue","red","black"]
        # Draw graph using positions
        plt.figure(figsize=(12, 12))

        # Draw nodes
        colors = [self.vertex_color_choices[vertex_color_dict[node]] for node in G.nodes]
        self.nodes = nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=100)
        
        # Draw edges
        edge_colors = [self.edge_color_choices[edge_color_dict[tuple(sorted(edge))]] for edge in G.edges]
        self.edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
        
        # Write labels
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.ion()  # Interactive mode for dynamic updates
        plt.axis("off")  # Hide axis
        plt.show(block=False)
    @classmethod
    def get_graph_colors(cls,M, Theseus,explored=nx.Graph()):
        #returns two default dictionaries, vertex_color_dict and edge_color_dict that assign integers that represent colors.
        #K is a subgraph of G that we will color
        vertex_color_dict = defaultdict(int)
        edge_color_dict = defaultdict(int)
        for s in M.S.edges:
            e = tuple(sorted(s))
            edge_color_dict[e] = 1

        for v in explored.nodes:
            vertex_color_dict[v]=2

        if isinstance(Theseus.location,str):
            if Theseus.location[0] == 'n':
                vertex_color_dict[Theseus.location]=1
            else: #Theseus is at a dead end.
                edge_color_dict[tuple(sorted(M.edgeD[Theseus.location]))] = 2
        elif isinstance(Theseus.location, tuple):
            edge = tuple(sorted((Theseus.location[0],Theseus.location[1])))
            edge_color_dict[edge]=2
        return vertex_color_dict, edge_color_dict
    def recolor_graph(self,vertex_color_dict,edge_color_dict):
        #called after draw_graph to update it with new colors.
        edge_colors = [self.edge_color_choices[edge_color_dict[tuple(sorted(edge))]] for edge in self.G.edges]
        self.edges.set_color(edge_colors)
        colors = [self.vertex_color_choices[vertex_color_dict[node]] for node in self.G.nodes]
        self.nodes.set_color(colors)

# Example usage
#file_path = "maze3.graphml"  # Replace with your file path
#visualize_graph_with_curved_edges(file_path)