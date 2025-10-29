"""
Disjoint-Set (Union-Find) data structure implementation.

This data structure efficiently tracks connected components and supports
union and find operations to determine if elements belong to the same set.
"""


class DisjointSet:
    """
    Disjoint-Set data structure with path compression and union by rank.
    
    This implementation provides efficient operations for tracking
    connected components in a graph or grid structure.
    """
    
    def __init__(self, size):
        """
        Initialize the disjoint set with 'size' elements.
        
        Args:
            size: Number of elements in the disjoint set
        """
        self.parent = list(range(size))
        self.rank = [0] * size
    
    def find(self, x):
        """
        Find the root of the set containing element x.
        Uses path compression for optimization.
        
        Args:
            x: Element to find the root for
            
        Returns:
            Root of the set containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        """
        Unite the sets containing elements x and y.
        Uses union by rank for optimization.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if the elements were in different sets (union performed),
            False if they were already in the same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True
    
    def connected(self, x, y):
        """
        Check if elements x and y are in the same set.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if x and y are connected, False otherwise
        """
        return self.find(x) == self.find(y)
