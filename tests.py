from maze import *

def test_spanning_tree():
    #checks that the alleged spanning tre created in __init__ has 1 fewer edge than vertices.
    M= maze(filename="maze_graphs/maze3.graphml")
    assert len(M.G.nodes) == len(M.S.edges)+1
    print("assertion passed")