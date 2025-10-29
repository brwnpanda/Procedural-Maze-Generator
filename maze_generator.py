"""
Procedural Maze Generator using Kruskal's Algorithm.

This module generates perfect mazes (fully connected, cycle-free) by treating
cells as nodes and walls as edges in a graph, then applying Kruskal's algorithm
to create a minimum spanning tree.
"""

import random
from disjoint_set import DisjointSet


class MazeGenerator:
    """
    Generate perfect mazes using Kruskal's algorithm.
    
    The generator creates a grid where each cell is a node and walls between
    cells are edges. It uses Kruskal's algorithm with a Disjoint-Set data
    structure to efficiently build a maze that is fully connected and cycle-free.
    """
    
    def __init__(self, width, height, seed=None):
        """
        Initialize the maze generator.
        
        Args:
            width: Width of the maze (number of cells)
            height: Height of the maze (number of cells)
            seed: Random seed for reproducible mazes (optional)
        """
        self.width = width
        self.height = height
        self.num_cells = width * height
        
        if seed is not None:
            random.seed(seed)
        
        # Initialize the maze grid with all walls present
        # horizontal_walls[i][j] represents wall below cell (i, j)
        # vertical_walls[i][j] represents wall to the right of cell (i, j)
        self.horizontal_walls = [[True] * width for _ in range(height)]
        self.vertical_walls = [[True] * width for _ in range(height)]
    
    def _cell_to_index(self, row, col):
        """
        Convert 2D cell coordinates to 1D index for disjoint set.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            1D index for the cell
        """
        return row * self.width + col
    
    def _get_all_walls(self):
        """
        Get all possible walls (edges) in the maze.
        
        Returns:
            List of walls, where each wall is represented as
            ((row1, col1), (row2, col2), wall_type)
        """
        walls = []
        
        # Horizontal walls (walls below cells)
        for row in range(self.height - 1):
            for col in range(self.width):
                walls.append(((row, col), (row + 1, col), 'horizontal'))
        
        # Vertical walls (walls to the right of cells)
        for row in range(self.height):
            for col in range(self.width - 1):
                walls.append(((row, col), (row, col + 1), 'vertical'))
        
        return walls
    
    def generate(self):
        """
        Generate a perfect maze using Kruskal's algorithm.
        
        This method applies Kruskal's algorithm to create a minimum spanning
        tree of the grid, ensuring the maze is fully connected and cycle-free.
        """
        # Initialize disjoint set for all cells
        ds = DisjointSet(self.num_cells)
        
        # Get all walls and shuffle them randomly
        walls = self._get_all_walls()
        random.shuffle(walls)
        
        # Apply Kruskal's algorithm
        for cell1, cell2, wall_type in walls:
            row1, col1 = cell1
            row2, col2 = cell2
            
            index1 = self._cell_to_index(row1, col1)
            index2 = self._cell_to_index(row2, col2)
            
            # If cells are not connected, remove the wall between them
            if not ds.connected(index1, index2):
                ds.union(index1, index2)
                
                # Remove the wall
                if wall_type == 'horizontal':
                    self.horizontal_walls[row1][col1] = False
                else:  # vertical
                    self.vertical_walls[row1][col1] = False
    
    def to_string(self):
        """
        Convert the maze to a string representation.
        
        Returns:
            String representation of the maze using ASCII characters
        """
        result = []
        
        # Top border
        result.append('+' + '---+' * self.width)
        
        for row in range(self.height):
            # Cell row with vertical walls
            cell_line = '|'
            for col in range(self.width):
                cell_line += '   '
                if col < self.width - 1:
                    if self.vertical_walls[row][col]:
                        cell_line += '|'
                    else:
                        cell_line += ' '
                else:
                    cell_line += '|'
            result.append(cell_line)
            
            # Horizontal walls row
            wall_line = '+'
            for col in range(self.width):
                if row < self.height - 1:
                    if self.horizontal_walls[row][col]:
                        wall_line += '---+'
                    else:
                        wall_line += '   +'
                else:
                    wall_line += '---+'
            result.append(wall_line)
        
        return '\n'.join(result)
    
    def save_to_file(self, filename):
        """
        Save the maze to a text file.
        
        Args:
            filename: Path to the output file
        """
        with open(filename, 'w') as f:
            f.write(self.to_string())
    
    def print_maze(self):
        """
        Print the maze to the console.
        """
        print(self.to_string())


def main():
    """
    Example usage of the maze generator.
    """
    # Generate a 10x10 maze
    print("Generating a 10x10 maze using Kruskal's Algorithm...")
    maze = MazeGenerator(10, 10, seed=42)
    maze.generate()
    maze.print_maze()
    
    print("\n" + "="*50 + "\n")
    
    # Generate a 5x5 maze
    print("Generating a 5x5 maze...")
    small_maze = MazeGenerator(5, 5)
    small_maze.generate()
    small_maze.print_maze()
    
    print("\n" + "="*50 + "\n")
    
    # Generate a 15x15 maze and save to file
    print("Generating a 15x15 maze and saving to file...")
    large_maze = MazeGenerator(15, 15)
    large_maze.generate()
    large_maze.save_to_file('maze_15x15.txt')
    print("Maze saved to 'maze_15x15.txt'")


if __name__ == '__main__':
    main()
