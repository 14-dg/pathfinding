Perfect — you’ve already got A* and step-by-step visualization working, and the multi-grid structure is partially functional but still under development.

Here’s the  **updated and polished `README.md`** , fully reflecting your project’s current state and roadmap.

---

```markdown
# 🧭 Pathfinding Visualization Tool

A modular Python application for visualizing **pathfinding algorithms** (such as **Dijkstra** and **A\***).  
It features an interactive **grid-based GUI** built with **Pygame**, allowing users to build maps, place obstacles, and visualize the algorithm’s progress **step by step**.

---

## 🚀 Features

- **Interactive Grid System** — draw obstacles, set start and target cells interactively.
- **Supports Multiple Algorithms** — both **Dijkstra** and **A\*** are fully implemented.
- **Step-by-Step Visualization** — watch the algorithm explore the grid in real time.
- **Multi-Grid Display** — visualize multiple grids (currently up to four) in one window.
- **Extensible Architecture** — easily add new grid types or algorithms.
- **Random Maze Generation** — quickly create obstacle maps for testing.

---

## 🧩 Project Structure

```

📦 pathfinder-visualizer/

├── main.py               # Entry point — initializes grids and starts the GUI

├── constants.py          # Global constants (colors, cell types, algorithm identifiers)

├── cell.py               # Cell class representing each grid square

├── grid.py               # Grid class handling cell storage and logic

├── pathfinder.py         # Implements Dijkstra and A* pathfinding algorithms

├── drawing_grid.py       # Handles rendering of a single grid using Pygame

├── drawing_board.py      # Manages the window, events, and multiple grids

└── README.md             # Project documentation

```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pathfinding.git
cd pathfinder-visualizer
```

### 2. Install dependencies

Make sure you have **Python 3.10+** installed:

```bash
pip install pygame
```

---

## 🕹️ Usage

Run the program:

```bash
python main.py
```

### Controls

* **Left-click** — toggle obstacle cells.
* **Right-click** — set start position
* **P-click** — set target position
* **Keyboard shortcuts** — trigger algorithms, clear the grid, or step through the pathfinding process (key bindings are defined in `drawing_board.py`).

---

## 🧠 Core Components Overview

### **1. `Cell`**

Represents one square in a grid:

* Stores position `(row, col)`
* Contains a `cell_type` (`EMPTY`, `OBSTACLE`, `TARGET`, `STARTING_POINT`, etc.)
* Has color and visual state defined in `constants.py`

### **2. `Grid`**

Logical model for a grid:

* Stores a 2D array of `Cell` objects
* Provides access to neighbors for pathfinding
* Supports clearing, resetting, and random maze generation
* Identified by a unique `grid_name` (e.g. `MAIN_GRID`, `SECONDARY_GRID`, etc.)

### **3. `Pathfinder`**

Implements the pathfinding logic:

* Contains **Dijkstra** and **A*** algorithms
* Uses priority queues (`heapq`) for efficient search
* Supports **step-by-step** exploration for visual debugging
* Interacts directly with `Grid` cells to highlight visited paths

### **4. `DrawingGrid`**

Handles rendering a specific grid:

* Draws all cells and borders
* Translates mouse input to cell coordinates
* Manages its own offset, size, and layout within the main window

### **5. `DrawingBoard`**

Controls the **Pygame window** and main loop:

* Displays multiple `DrawingGrid` objects simultaneously
* Handles user events and keyboard input
* Coordinates algorithm execution and grid updates
* Allows for margins and dynamic layouts between grids

---

## 🗺️ Grid Types and Layout

The visualization supports multiple grids displayed side by side.

Each grid can represent a different aspect of the simulation.

| Grid Type                          | Description                                                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **MAIN_GRID**                | The main environment where the pathfinder operates. Displays start, goal, and explored nodes.                                    |
| **SECONDARY_GRID**           | Reserved for visualizing additional data — e.g. the rover’s internal map (for SLAM), heuristic overlays, or sensor visibility. |
| **THIRD_GRID / FOURTH_GRID** | Currently unused, but intended for future extensions like multi-agent simulations or comparing algorithm outputs.                |

Example setup from `main.py`:

```python
g1 = Grid(80, 80, grid_name=MAIN_GRID)
g2 = Grid(80, 80, grid_name=SECONDARY_GRID)
g3 = Grid(80, 80, grid_name=THIRD_GRID)
g4 = Grid(80, 80, grid_name=FOURTH_GRID)

dg1 = DrawingGrid(g1, x_offset=10, y_offset=10)
dg2 = DrawingGrid(g2, x_offset=810, y_offset=10)
...

db = DrawingBoard(MAIN_GRID=dg1, SECONDARY_GRID=dg2, THIRD_GRID=dg3, FOURTH_GRID=dg4)
db.mainloop()
```

This structure allows **multiple grids** to be drawn in one Pygame window, keeping their logic separate but their display synchronized.

---

## 🧱 Development Notes

* Built entirely in **Python** using  **Pygame** .
* Designed with **object-oriented principles** for modularity.
* Each component (logic, drawing, algorithms) is fully decoupled.
* Supports easy expansion for new grid types or algorithm variants.

---

## 🔮 Planned Extensions

* [ ] Implement  **SLAM visualization** , showing what the rover “thinks” the map looks like.
* [ ] Add **sensor simulation** overlays (LiDAR-style range visualization).
* [ ] Allow dynamic grid creation via menu selection.
* [ ] Improve UI with dropdowns and algorithm selectors.

---

## 🧪 Current Development Focus

The current development branch focuses on  **multi-grid visualization** , enabling scenarios such as:

* Simulating a rover exploring an environment (`MAIN_GRID`)
* Displaying the rover’s internal reconstruction of that environment (`SECONDARY_GRID`)
* Potential future use for  **path comparison** ,  **sensor uncertainty** , or  **multi-agent exploration** .

---

## 🪪 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Daniel Gräf**

Project for educational and research purposes.
