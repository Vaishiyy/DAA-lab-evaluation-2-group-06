8-Puzzle Game 

1. Divide and Conquer with A* Heuristic Solver

Project Description

This project implements the 8-Puzzle (3×3 sliding puzzle) game using a Divide and Conquer approach combined with the A Heuristic Search*. The puzzle is modeled as a graph, with puzzle states as nodes and legal tile moves as edges. The AI solver utilizes the A* algorithm with a Manhattan distance heuristic to solve the puzzle step-by-step.

Algorithms Used:

Graph Model: The puzzle is modeled as a graph where each state is a node, and each legal move between states is an edge.

Divide and Conquer: The puzzle is solved in two main phases:

Divide: Solve the first row using A* search.

Conquer: Solve the remaining puzzle, moving towards the goal state.

A Heuristic Search:* Uses the Manhattan distance heuristic to evaluate the cost of each move. The best possible move (with the lowest heuristic value) is chosen for the next step.

Heuristic:

Manhattan Distance: Calculates the sum of the absolute differences in the row and column of each tile's current position and its goal position.

Features:

Dual board interface: The user competes against the AI in solving the puzzle.

Image-based puzzle tiles: Uses images as puzzle tiles, allowing for a visually engaging gameplay experience.

Guaranteed solvable shuffle: Ensures that the shuffled board is always solvable.

Step count comparison: Tracks and displays the number of steps taken by both the user and the AI to solve the puzzle.

Animated AI solution: Visualizes the AI’s step-by-step solution.

Technologies Used:

Python Tkinter: For the GUI (Graphical User Interface).

PIL (Pillow): For image manipulation and display.

<img width="1910" height="1155" alt="image" src="https://github.com/user-attachments/assets/11c3f629-1410-402b-bbaa-c860a0121ba8" />

2. Dynamic Programming with BFS

Project Description

This project implements the 8-Puzzle (3×3 sliding puzzle) game using Dynamic Programming (DP) with a Breadth-First Search (BFS) approach to solve the puzzle. The puzzle is represented as a grid, and each possible puzzle configuration is treated as a state in a graph. The goal is to move from the starting state to the goal state by sliding tiles, while minimizing the number of moves.

Algorithms Used:

Dynamic Programming Table:
The puzzle states are pre-computed and stored in a DP table where the key is the puzzle state and the value is the previous state. This enables fast path reconstruction from any given state to the goal state.

Breadth-First Search (BFS):
BFS is used to explore all possible moves in a level-order fashion, ensuring that the shortest path (minimum number of moves) is found from the starting state to the goal state.

Features:

Dual Board Interface:
The user competes against the AI in solving the puzzle. The AI utilizes BFS with a precomputed DP table to find the optimal solution.

Precomputed DP Table:
The DP table stores the shortest path from the goal state to all other reachable puzzle states, allowing for rapid path reconstruction using BFS.

Image-based Puzzle Tiles:
The puzzle tiles are displayed as images, making the gameplay visually engaging and interactive.

Guaranteed Solvable Shuffle:
The puzzle board is shuffled in such a way that it is guaranteed to be solvable, ensuring a fair game for the user.

Step Count Comparison:
Tracks and displays the number of steps taken by both the user and the AI to solve the puzzle, allowing for a side-by-side comparison.

Animated AI Solution:
The AI’s solution is animated step-by-step, showing how it arrives at the goal state.

Technologies Used:

Python Tkinter: For creating the GUI (Graphical User Interface).

PIL (Pillow): For handling image manipulation and display.

<img width="1912" height="1151" alt="image" src="https://github.com/user-attachments/assets/950cd3c8-c50e-4434-a98e-0c488007876e" />
