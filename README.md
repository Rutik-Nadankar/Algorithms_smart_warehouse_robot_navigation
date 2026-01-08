# Algorithms_smart_warehouse_robot_navigation

A simulation of a smart warehouse using AI pathfinding algorithms (BFS and A*) to navigate a robot through shelves. This project demonstrates how AI can be applied in logistics and warehouse management.

---

## 1. Project Overview

The Smart Warehouse AI project simulates a warehouse environment where a robot moves from a start point to an end point while avoiding shelves. We implemented and compared **BFS (Breadth-First Search)** and **A* Search** algorithms to find the optimal path.  

- **Purpose:** Demonstrate AI pathfinding in real-world scenarios like warehouse management.  
- **Key Features:**  
  - Visual grid-based warehouse using **pygame**.  
  - Randomly or manually placed shelves.  
  - Comparison of BFS and A* algorithms (steps & nodes explored).  
  - Interactive GUI for testing different scenarios.

---

Follow these steps to quickly set up and run the Algorithms_smart_warehouse_robot_navigation:

1. **Clone the repository**
```bash
git clone https://github.com/Rutik-Nadankar/Smart-Warehouse-AI.git
cd Smart-Warehouse-AI
Install Python 3.10 (required for compatibility)
Download from Python.org
.

Create and activate a virtual environment (optional but recommended)

Windows:

python -m venv .venv
.venv\Scripts\activate


macOS/Linux:

python -m venv .venv
source .venv/bin/activate


Install required Python libraries

pip install pygame


Run the simulation

python main.py


Using the GUI

Click on the grid to set Start Point (green) and End Point (red).

Click Run BFS to see BFS pathfinding in action.

Click Run A* to see A* pathfinding in action.

Click Shuffle to randomly rearrange shelves.

Click Restart to reset grid, robot position, path, and results.

Result Panel

Shows steps taken and nodes explored for BFS and A*.

Displays algorithm comparison, showing which is better.

If a path is unreachable, a message will appear.

Important Notes

Ensure images folder contains robot.png, shelf.png, and floor.png.

Folders agents and environment must remain in the same directory as main.py.

To set constant shelves instead of random, modify the Warehouse class in warehouse.py.
