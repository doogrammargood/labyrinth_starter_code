from maze_solve_algorithms import *
from unittest import TestCase
import unittest
import time
from gradescope_utils.autograder_utils.decorators import weight, visibility, number
from scipy.stats import chisquare
graph_names = [f"maze_graphs/maze{i}.graphml" for i in [1,2,3]]
import itertools
class Tests(TestCase):

    @weight(10)
    @number(1)
    @visibility(True)
    def test_fisher_shuffle(self):
        #tests if the fisher shuffle is actually returning uniformly random permutations.
        #Apples the chi-squared test.
        shuffles = defaultdict(int)
        observed_frequencies = []
        expected_frequencies = []
        n = 8
        num_trials =10000
        for trial in range(num_trials):
            shuffles[tuple(fisher_shuffle(n))]+=1
        for permutation in itertools.permutations(range(n)):
            observed_frequencies.append(shuffles[tuple(permutation)])
            expected_frequencies.append(num_trials/math.factorial(n))
        result = scipy.stats.chisquare(observed_frequencies,expected_frequencies)
        assert result.pvalue >0.01 #even if your shuffle is implemented correctly, this can fail 1/100 times.
    @weight(10)
    @number(2)
    @visibility(True)
    def test_minimal_spanning_tree(self):
        #checks that the alleged spanning tre created in __init__ has 1 fewer edge than vertices.
        minimal_spanning_trees = [9465.301381459423,13011.154937848629,7399.7810979449]
        for i, file in enumerate(graph_names):
            M=maze(file,reopen_edges=float('inf'))
            edge_weights = {e: M.distance(e[0],e[1]) for e in M.G.edges}
            result = kruskals(M.G, edge_weights)
            value = sum([M.distance(e[0],e[1]) for e in result.edges])
            assert value == minimal_spanning_trees[i]
            assert len(M.G.nodes) == len(result.edges)+1

    @weight(10)
    @number(3)
    @visibility(True)
    def test_dfs(self):
        for file in graph_names:
            M= maze(filename=file)
            K=known_maze(M)
            Theseus=hero(K,draw=False)
            depth_first_search(Theseus)
            assert Theseus.travel_distance>0
            assert Theseus.travel_distance <= 2* Theseus.exploration_distance #Each edge is travered at most twice.
            assert Theseus.location == Theseus.K.M.exit
    @weight(10)
    @number(4)
    @visibility(True)
    def test_shortest_path(self):
        M= maze(filename="maze_graphs/maze3.graphml", reopen_edges=float('inf'))
        K=known_maze(M)
        K.learn_all_edges()
        print(K.shortest_known_path[(M.entrance,M.exit)])
        assert abs(K.shortest_known_path[(M.entrance,M.exit)] - linear_programming_shortest_path(M,M.entrance,M.exit))<0.01 #there could be some rounding error, but these quantities should be close.
        
    @weight(10)
    @number(5)
    @visibility(True)
    def test_a_star(self):
        
        for index, file in enumerate(graph_names):
            M= maze(filename=file,reopen_edges=float('inf')) #all edges are open
            K=known_maze(M)
            Theseus=hero(K,draw=False)
            a_star_search(Theseus)
            a_star_dist = K.shortest_known_path[(M.entrance, M.exit)]
            K.learn_all_edges()
            new_dist = K.shortest_known_path[(M.entrance, M.exit)]
            assert abs(a_star_dist - new_dist)<.01
            #assert Theseus.exploration_distance==exploration_distances[index]
            assert Theseus.location == Theseus.K.M.exit

    def test_update_shortest_paths(self):
        time_to_update_shortest_paths_slow=0
        time_to_update_shortest_paths_fast=0
        for file in graph_names:
            M= maze(filename=file, reopen_edges=float('inf')) #all edges are open
            K1=known_maze(M)
            K2=known_maze(M)
            for edge in M.D.edges:

                K1.explored.add_edge(edge[0],edge[1])
                start = time.time()
                K1.shortest_known_path = update_shortest_known_path(K1,K1.shortest_known_path, edge, M.distance(edge[0],edge[1]))
                end = time.time()
                time_to_update_shortest_paths_slow += end - start

                K2.explored.add_edge(edge[0],edge[1])
                start=time.time()
                K2.shortest_known_path = update_shortest_known_path_faster(K2,K2.shortest_known_path, edge, M.distance(edge[0],edge[1]))
                end=time.time()
                time_to_update_shortest_paths_fast += end - start
                assert K2.shortest_known_path[edge]==M.distance(edge[0],edge[1])
                assert K1.shortest_known_path==K2.shortest_known_path
        print("times: ", time_to_update_shortest_paths_slow, time_to_update_shortest_paths_fast)
        print("passed")

    def test_remove_edge(self):
        for file in graph_names:
            M= maze(filename=file,reopen_edges=float('inf')) #all edges are open
            K1=known_maze(M)
            K2=known_maze(M)
            for edge in list(M.D.edges())[:-1]:
                K1.add_edge(edge[0],edge[1])
            edge = list(M.D.edges())[-1]
            K2.learn_all_edges()
            K2.remove_edge(edge[0],edge[1])
            assert K1.explored.nodes == K2.explored.nodes
            assert K1.explored.edges == K2.explored.edges
            assert K1.shortest_known_path == K2.shortest_known_path
if __name__=="__main__":
    #t = Tests()
    #t.test_minimal_spanning_tree()
    #t.test_a_star()
    #t.test_update_shortest_paths()
    #t.test_remove_edge()
    unittest.main()