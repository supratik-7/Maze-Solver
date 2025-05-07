# Maze Solver

A visually interactive maze solver built with **Tkinter** in Python. This project allows users to create custom grids, place obstacles, and visualize the shortest path between selected start and end points using a breadth-first search (BFS) algorithm.

## Features

* **Dynamic Grid Creation:** Create grids of varying sizes dynamically.
* **Manual and Random Maze Generation:** Toggle between manual block placement and randomized obstacle generation.
* **Start and End Block Selection:** Easily set starting and ending points for the maze.
* **Pathfinding Animation:** Visualize the shortest path from start to end with smooth animations.
* **Path Weight Calculation:** Assign path weights based on Manhattan distance.
* **Responsive Design:** Grid buttons dynamically adjust size based on the canvas.
* **Reset and Clear Options:** Quickly reset the grid to its default state.

## Prerequisites

Ensure you have **Tkinter** installed (usually included with Python):

```bash
sudo apt install python3-tk  # For Linux (if not pre-installed)
```

## Project Structure

```
Maze_Solver/
├── main.py
└── README.md
```

## How to Run the Project

1. Clone the repository:

```bash
git clone <repo_url>
cd Maze_Solver
```

2. Run the main script:

```bash
python main.py
```

## Usage

* **Grid Creation:** Enter the number of rows and columns to create a grid.
* **Obstacle Percentage:** Set a percentage for random obstacle generation.
* **Manual Maze:** Manually select grid blocks as obstacles.
* **Random Maze:** Automatically generate random obstacles based on the set percentage.
* **Start and End Points:** Click to set start (green) and end (red) blocks.
* **Pathfinding:** Click "Find Path" to visualize the shortest path.
* **Reset:** Clear the entire grid.

## Screenshots

Include screenshots here (if needed) for a better understanding of the UI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to open issues or submit pull requests if you have ideas for improvement.
