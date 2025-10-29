"""
Unit tests for the Procedural Maze Generator.

Tests the DisjointSet data structure and MazeGenerator class to ensure
correct implementation of Kruskal's algorithm and proper maze generation.
"""

import unittest
import os
from disjoint_set import DisjointSet
from maze_generator import MazeGenerator


class TestDisjointSet(unittest.TestCase):
    """Test cases for the DisjointSet class."""
    
    def test_initialization(self):
        """Test that disjoint set initializes correctly."""
        ds = DisjointSet(5)
        self.assertEqual(len(ds.parent), 5)
        self.assertEqual(len(ds.rank), 5)
        
        # Each element should be its own parent initially
        for i in range(5):
            self.assertEqual(ds.find(i), i)
    
    def test_union_and_find(self):
        """Test union and find operations."""
        ds = DisjointSet(5)
        
        # Initially, all elements should be disconnected
        self.assertFalse(ds.connected(0, 1))
        self.assertFalse(ds.connected(1, 2))
        
        # Union elements 0 and 1
        result = ds.union(0, 1)
        self.assertTrue(result)  # Union should succeed
        self.assertTrue(ds.connected(0, 1))
        
        # Union elements 1 and 2
        ds.union(1, 2)
        self.assertTrue(ds.connected(0, 2))  # Transitivity
        self.assertTrue(ds.connected(1, 2))
        
        # Elements 3 and 4 should still be separate
        self.assertFalse(ds.connected(0, 3))
        self.assertFalse(ds.connected(2, 4))
    
    def test_union_same_set(self):
        """Test that unioning elements in the same set returns False."""
        ds = DisjointSet(3)
        
        ds.union(0, 1)
        # Try to union again - should return False
        result = ds.union(0, 1)
        self.assertFalse(result)
    
    def test_path_compression(self):
        """Test that path compression works correctly."""
        ds = DisjointSet(4)
        
        # Create a chain: 0 -> 1 -> 2 -> 3
        ds.union(0, 1)
        ds.union(1, 2)
        ds.union(2, 3)
        
        # After find operations, paths should be compressed
        root = ds.find(0)
        self.assertEqual(ds.find(3), root)
        self.assertTrue(ds.connected(0, 3))


class TestMazeGenerator(unittest.TestCase):
    """Test cases for the MazeGenerator class."""
    
    def test_initialization(self):
        """Test that maze generator initializes correctly."""
        maze = MazeGenerator(5, 5)
        self.assertEqual(maze.width, 5)
        self.assertEqual(maze.height, 5)
        self.assertEqual(maze.num_cells, 25)
        
        # All walls should be present initially
        for row in maze.horizontal_walls:
            for wall in row:
                self.assertTrue(wall)
        for row in maze.vertical_walls:
            for wall in row:
                self.assertTrue(wall)
    
    def test_cell_to_index(self):
        """Test cell coordinate to index conversion."""
        maze = MazeGenerator(3, 3)
        
        self.assertEqual(maze._cell_to_index(0, 0), 0)
        self.assertEqual(maze._cell_to_index(0, 1), 1)
        self.assertEqual(maze._cell_to_index(0, 2), 2)
        self.assertEqual(maze._cell_to_index(1, 0), 3)
        self.assertEqual(maze._cell_to_index(2, 2), 8)
    
    def test_get_all_walls(self):
        """Test that all walls are generated correctly."""
        maze = MazeGenerator(3, 3)
        walls = maze._get_all_walls()
        
        # For a 3x3 grid:
        # Horizontal walls: 3 * 2 = 6 (3 columns, 2 rows of horizontal walls)
        # Vertical walls: 2 * 3 = 6 (2 columns of vertical walls, 3 rows)
        # Total: 12 walls
        self.assertEqual(len(walls), 12)
    
    def test_maze_generation(self):
        """Test that maze generation completes without errors."""
        maze = MazeGenerator(5, 5, seed=42)
        maze.generate()
        
        # After generation, some walls should be removed
        horizontal_removed = sum(1 for row in maze.horizontal_walls 
                                for wall in row if not wall)
        vertical_removed = sum(1 for row in maze.vertical_walls 
                              for wall in row if not wall)
        
        # In a perfect maze, exactly (cells - 1) walls should be removed
        # For a 5x5 maze: 25 cells, so 24 walls should be removed
        total_removed = horizontal_removed + vertical_removed
        self.assertEqual(total_removed, 24)
    
    def test_reproducible_maze(self):
        """Test that mazes with the same seed are identical."""
        maze1 = MazeGenerator(5, 5, seed=42)
        maze1.generate()
        
        maze2 = MazeGenerator(5, 5, seed=42)
        maze2.generate()
        
        # Both mazes should be identical
        self.assertEqual(maze1.horizontal_walls, maze2.horizontal_walls)
        self.assertEqual(maze1.vertical_walls, maze2.vertical_walls)
    
    def test_different_seeds_different_mazes(self):
        """Test that mazes with different seeds are different."""
        maze1 = MazeGenerator(10, 10, seed=1)
        maze1.generate()
        
        maze2 = MazeGenerator(10, 10, seed=2)
        maze2.generate()
        
        # Mazes should be different (at least one wall differs)
        self.assertNotEqual(maze1.horizontal_walls, maze2.horizontal_walls)
    
    def test_to_string(self):
        """Test maze string representation."""
        maze = MazeGenerator(3, 3, seed=42)
        maze.generate()
        maze_str = maze.to_string()
        
        # String should not be empty
        self.assertTrue(len(maze_str) > 0)
        
        # Should contain walls and cells
        self.assertIn('+', maze_str)
        self.assertIn('|', maze_str)
        self.assertIn('-', maze_str)
    
    def test_save_to_file(self):
        """Test saving maze to file."""
        maze = MazeGenerator(3, 3, seed=42)
        maze.generate()
        
        test_filename = '/tmp/test_maze.txt'
        maze.save_to_file(test_filename)
        
        # File should exist
        self.assertTrue(os.path.exists(test_filename))
        
        # File should contain maze content
        with open(test_filename, 'r') as f:
            content = f.read()
            self.assertTrue(len(content) > 0)
            self.assertIn('+', content)
        
        # Clean up
        os.remove(test_filename)
    
    def test_maze_connectivity(self):
        """
        Test that generated maze is fully connected.
        This is a crucial property of perfect mazes.
        """
        from disjoint_set import DisjointSet
        
        maze = MazeGenerator(5, 5)
        maze.generate()
        
        # Rebuild the connectivity using the generated maze
        ds = DisjointSet(maze.num_cells)
        
        # Connect cells based on removed walls
        for row in range(maze.height):
            for col in range(maze.width):
                # Check horizontal wall below
                if row < maze.height - 1 and not maze.horizontal_walls[row][col]:
                    index1 = maze._cell_to_index(row, col)
                    index2 = maze._cell_to_index(row + 1, col)
                    ds.union(index1, index2)
                
                # Check vertical wall to the right
                if col < maze.width - 1 and not maze.vertical_walls[row][col]:
                    index1 = maze._cell_to_index(row, col)
                    index2 = maze._cell_to_index(row, col + 1)
                    ds.union(index1, index2)
        
        # All cells should be connected to cell 0
        for i in range(1, maze.num_cells):
            self.assertTrue(ds.connected(0, i), 
                          f"Cell {i} is not connected to cell 0")


if __name__ == '__main__':
    unittest.main()
