from math import sqrt
from math import log

EPSILON = 0.00001
BIG_NUMBER = 1e9

class Graph:
    """Undirected graph of given capacity.

    There is no way to add or remove vertices, so zero-degree vertices
    are supposed to be just hidden.
    """

    VERTEX_COEFF = 500
    EDGE_COEFF = 1

    def __init__(self, size):
        """Create a new graph of given vertex capacity and with no edges."""
        self.size = size
        self.V = [Vertex() for i in range(size)]
        self.E = [[False] * self.size for _ in range(size)]
        #self.edge_weights = [[0] * self.size for _ in range(size)]
        self.weight = 0
        self.edge_weights = [[0] * self.size for _ in range(self.size)]
        self.is_tree = False



    def add_edge(self, i, j):
        """Add an edge (if it exists, do nothing)."""
        assert self.in_bounds(i) and self.in_bounds(j)
        if i == j or self.E[i][j]: return

        self.E[i][j] = self.E[j][i] = True
        self.V[i].degree += 1
        self.V[j].degree += 1
        
        self.calculate_vertex(i)
        self.calculate_vertex(j)
        self._check_for_tree()

    def delete_edge(self, i, j):
        """Delete edge (if it doesn't exist, do nothing."""
        assert self.in_bounds(i) and self.in_bounds(j)
        if i == j or not self.E[i][j]: return

        self.E[i][j] = self.E[j][i] = False
        self.V[i].degree -= 1
        self.V[j].degree -= 1
        
        self.calculate_vertex(i)
        self.calculate_vertex(j)
        self._check_for_tree()

    def set_coords(self, i, x, y):
        self.V[i].x = float(x)
        self.V[i].y = float(y)
        self.calculate_vertex(i)

    def n_edges(self):
        return sum(V.degree for V in self.V) / 2

    def count_zero_vertices(self):
        """Return number of hidden vertices (with zero degree)."""
        return sum(1 for V in self.V if V.degree == 0) 

    def number_of_components(self):
        """Return number of not-empty connected components."""
        visited = [False] * self.size
        queue = []
        count = 0
        for i in range(self.size):
            if self.V[i].degree == 0 or visited[i]:
                continue
            count += 1
            queue.append(i)
            while (queue):
                current = queue.pop()
                if (visited[current]): continue
                visited[current] = True
                queue += [j for j in range(self.size) if self.E[current][j]]
        return count

    def in_bounds(self, vertex):
        """Return true for valid index of vertex."""
        return vertex >= 0 and vertex < self.size

    def _check_for_tree(self):
        """Return true if graph is a tree (zero vertices excluded)."""
        self.is_tree = (
               self.n_edges() == self.size - self.count_zero_vertices() - 1
               and self.number_of_components() == 1
               )

    def calculate_vertex(self, i):
        """When vertex changes, recalculates weights of all adjacent edges."""
        for j in range(self.size):
            if i == j or self.V[j].degree == 0:
                # nothing to do here
                continue

            # this entry to be recalculated
            self.weight -= self.edge_weights[i][j]

            if self.V[i].degree == 0:
                # if vertex goes out of scope, zero all edge weights.                
                self.edge_weights[i][j] = self.edge_weights[j][i] = 0
            
            else:
                w = (self.vertex_repel(i, j)
                            + (self.edge_attract(i, j) if self.E[i][j] else 0))
                self.edge_weights[i][j] = self.edge_weights[j][i] = w
                self.weight += w

    def reset_weight(self):
        for i in range(self.size):
            self.calculate_vertex(i)
        self.weight = sum(sum(row) for row in self.edge_weights)

    def vertex_repel(self, i, j):
        """Calculate energy of repelling - smaller for distant vertices."""
        if i == j or self.V[i].degree == 0 or self.V[j].degree == 0:
            return 0
        if Vertex.L1_dist(self.V[i], self.V[j]) < 2 * EPSILON:
            return BIG_NUMBER
        return Graph.VERTEX_COEFF / Vertex.dist(self.V[i], self.V[j])
    
    def edge_attract(self, i, j):
        """Calculate energy of attraction - smaller for close vertices."""
        if i == j or not self.E[i][j]:
            return 0
        dist = Vertex.dist(self.V[i], self.V[j])
        return log(dist) * Graph.EDGE_COEFF if dist > 0 else 0
    
    #def calculate_summary_weight(self):
    #    """Safety method: to check vertexwise weight corrections."""
    #    self.weight = sum(sum(row) for row in self.edge_weights) / 2

class Vertex:
    """Presents vertex"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.degree = 0

    @staticmethod
    def dist(V, W):
        """Given two vertices, calculate linear distance between them."""
        return sqrt((V.x - W.x) ** 2 + (V.y - W.y) ** 2)

    @staticmethod
    def L1_dist(V, W):
        return abs(V.x - W.x) + abs(V.y - W.y)
