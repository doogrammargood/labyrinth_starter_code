from maze_solve_algorithms import *
from unittest import TestCase
import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility, number
from scipy.stats import chisquare
graph_names = [f"maze_graphs/maze{i}.graphml" for i in [1,2,3]]
import itertools
class Tests(TestCase):

    @weight(5)
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
            observed_frequencies.append(shuffles[tuple(permutation)]/num_trials)
            expected_frequencies.append(1/math.factorial(n))
        result = scipy.stats.chisquare(observed_frequencies,expected_frequencies)
        assert result.pvalue >0.99
    @weight(5)
    @number(2)
    @visibility(True)
    def test_spanning_tree(self):
        #checks that the alleged spanning tre created in __init__ has 1 fewer edge than vertices.
        M= maze(filename="maze_graphs/maze3.graphml")
        assert len(M.G.nodes) == len(M.S.edges)+1

    @weight(5)
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
    
    @weight(5)
    @number(4)
    @visibility(True)
    def test_shortest_path(self):
        M= maze(filename="maze_graphs/maze3.graphml", reopen_edges=float('inf'))
        K=known_maze(M)
        K.learn_all_edges()
        assert abs(K.shortest_distances[(M.entrance,M.exit)] - linear_programming_shortest_path(M,M.entrance,M.exit))<0.01 #there could be some rounding error, but these quantities should be close.
        
    @weight(5)
    @number(5)
    @visibility(True)
    def test_a_star(self):
        exploration_distances = [6349.179523682272,2623.9738546780213,3781.761227509557]
        for index, file in enumerate(graph_names):
            M= maze(filename=file,reopen_edges=float('inf')) #all edges are open
            K=known_maze(M)
            Theseus=hero(K,draw=False)
            a_star_search(Theseus)
            assert Theseus.exploration_distance==exploration_distances[index]
if __name__=="__main__":
    t = Tests()
    #t.test_fisher_shuffle()
    #t.test_a_star()
    unittest.main()