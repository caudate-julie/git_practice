import unittest
from graph import Graph

class TestGraphMethods(unittest.TestCase):
    def test_creating(self):
        g = Graph(5)
        self.assertTrue(g.in_bounds(0))
        self.assertFalse(g.in_bounds(-1))
        self.assertFalse(g.in_bounds(5))

    def test_add_and_delete(self):
        g = Graph(10)
        self.assertEqual(g.size, 10)
        self.assertEqual(g.n_edges(), 0)

        # adding an edge - should be one more
        g.add_edge(0, 1)
        self.assertEqual(g.n_edges(), 1)

        # no adding should happen in these situations:
        g.add_edge(1, 0)
        g.add_edge(0, 1)
        g.add_edge(3, 3)
        self.assertEqual(g.n_edges(), 1)

        # add some more
        g.add_edge(4, 1)
        g.add_edge(3, 1)
        g.add_edge(2, 1)
        self.assertEqual(g.n_edges(), 4)

        # now deleting
        g.delete_edge(1, 3)
        g.delete_edge(1, 0)
        self.assertEqual(g.n_edges(), 2)

        # no deleting should happen in there situations:
        g.delete_edge(0, 1)
        g.delete_edge(0, 0)
        g.delete_edge(1, 3)
        self.assertEqual(g.n_edges(), 2)

        #assertion errors when index is out of range
        with self.assertRaises(AssertionError):
            g.add_edge(10, 3)

        with self.assertRaises(AssertionError):
            g.delete_edge(1, -3)
    
    def test_components(self):
        g = Graph(10)
        self.assertEqual(g.number_of_components(), 0)
        self.assertEqual(g.count_zero_vertices(), 10)

        # adding edges
        g.add_edge(0, 1)
        self.assertEqual(g.number_of_components(), 1)

        g.add_edge(3, 4)
        self.assertEqual(g.number_of_components(), 2)

        g.add_edge(2, 1)
        self.assertEqual(g.number_of_components(), 2)

        g.add_edge(2, 3)
        self.assertEqual(g.number_of_components(), 1)

        g.add_edge(4, 0)
        self.assertEqual(g.number_of_components(), 1)
        self.assertEqual(g.count_zero_vertices(), 5)

        # deleting edges
        g.delete_edge(2, 3)
        self.assertEqual(g.number_of_components(), 1)

        g.delete_edge(1, 0)
        self.assertEqual(g.number_of_components(), 2)

        g.delete_edge(1, 2)
        g.delete_edge(3, 4)
        self.assertEqual(g.number_of_components(), 1)
        self.assertEqual(g.count_zero_vertices(), 8)

        g.delete_edge(4, 0)
        self.assertEqual(g.number_of_components(), 0)

    def test_weights(self):
        

if __name__ == "__main__":
    unittest.main()