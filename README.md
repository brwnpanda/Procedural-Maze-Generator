# Procedural Maze Generator

A Python implementation of a procedural maze generator using **Kruskal's Algorithm** to create perfect mazes (fully connected, cycle-free).

## Overview

This project generates perfect mazes by applying Kruskal's algorithm to a grid structure, treating cells as nodes and walls as edges. It utilizes a **Disjoint-Set (Union-Find)** data structure to efficiently track connected components and ensure the resulting maze is fully connected without any cycles.

## Features

- **Kruskal's Algorithm**: Generates minimum spanning trees to create perfect mazes
- **Disjoint-Set Data Structure**: Efficient union-find operations with path compression and union by rank
- **Customizable Maze Size**: Generate mazes of any width and height
- **Reproducible Mazes**: Optional seed parameter for generating the same maze
- **ASCII Visualization**: Clean text-based maze representation
- **File Export**: Save generated mazes to text files

## Algorithm Details

### Kruskal's Algorithm

The maze generator uses Kruskal's algorithm to create a minimum spanning tree:

1. Start with a grid where all walls are present (each cell is isolated)
2. Treat each cell as a node and each potential wall removal as an edge
3. Randomly shuffle all possible walls
4. For each wall, check if removing it would connect two previously disconnected cells
5. If yes, remove the wall and union the two cells in the disjoint set
6. Continue until all cells are connected

This approach guarantees:
- **Fully connected**: Every cell is reachable from every other cell
- **Cycle-free**: There is exactly one path between any two cells (no loops)
- **Perfect maze**: The maze has the minimum number of walls removed to achieve connectivity

### Disjoint-Set (Union-Find)

The implementation uses two key optimizations:

- **Path Compression**: Flattens the tree structure during find operations
- **Union by Rank**: Attaches smaller trees under larger trees to keep the structure balanced

These optimizations ensure nearly O(1) amortized time complexity for both union and find operations.

## Installation

No external dependencies required! This project uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/brwnpanda/Procedural-Maze-Generator.git
cd Procedural-Maze-Generator
```

## Usage

### Basic Usage

Run the example program:

```bash
python maze_generator.py
```

This will generate three sample mazes of different sizes and save one to a file.

### Custom Maze Generation

```python
from maze_generator import MazeGenerator

# Create a 10x10 maze
maze = MazeGenerator(width=10, height=10)
maze.generate()

# Print to console
maze.print_maze()

# Save to file
maze.save_to_file('my_maze.txt')
```

### Reproducible Mazes

Use a seed for reproducible results:

```python
maze = MazeGenerator(width=10, height=10, seed=42)
maze.generate()
maze.print_maze()
```

### Accessing the Maze Structure

The maze walls are stored in two 2D arrays:

```python
maze = MazeGenerator(width=5, height=5)
maze.generate()

# Access wall data
horizontal_walls = maze.horizontal_walls  # Walls below each cell
vertical_walls = maze.vertical_walls      # Walls to the right of each cell
```

## Example Output

A 5x5 maze:

```
+---+---+---+---+---+
|                   |
+   +---+   +   +---+
|   |       |       |
+---+---+   +---+   +
|           |   |   |
+   +   +   +   +   +
|   |   |       |   |
+---+   +---+   +---+
|       |           |
+---+---+---+---+---+
```

## Project Structure

```
Procedural-Maze-Generator/
├── README.md              # This file
├── disjoint_set.py        # Disjoint-Set (Union-Find) implementation
├── maze_generator.py      # Main maze generator using Kruskal's algorithm
└── .gitignore             # Git ignore file
```

## Implementation Details

### DisjointSet Class

- `__init__(size)`: Initialize with a given number of elements
- `find(x)`: Find the root of the set containing x (with path compression)
- `union(x, y)`: Unite the sets containing x and y (with union by rank)
- `connected(x, y)`: Check if x and y are in the same set

### MazeGenerator Class

- `__init__(width, height, seed=None)`: Initialize the generator
- `generate()`: Generate the maze using Kruskal's algorithm
- `to_string()`: Convert maze to ASCII string representation
- `print_maze()`: Print the maze to console
- `save_to_file(filename)`: Save the maze to a text file

## Time Complexity

- Maze generation: O(E log E) where E is the number of edges (walls)
  - For a width × height grid: E ≈ 2 × width × height
- Union-Find operations: O(α(n)) amortized, where α is the inverse Ackermann function (effectively constant)

## Space Complexity

- O(width × height) for storing the maze and disjoint set structures

## Contributing

This is a personal project, but feel free to fork and modify it for your own use!

## License

This project is open source and available for educational purposes.

## Author

Created as a personal project to demonstrate:
- Understanding of graph algorithms (Kruskal's algorithm)
- Implementation of efficient data structures (Disjoint-Set)
- Procedural generation techniques
- Clean code practices and documentation