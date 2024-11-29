# Parking Lot Pathfinding Visualizer

A program that finds and visualizes the closest empty parking spot to a target location using BFS (Breadth-First Search) algorithm.

## Features

- Finds the closest empty parking spot using BFS
- Web-based visualization of the parking lot
- Color-coded spots:
  - Green: Empty spots
  - Red: Occupied spots
  - Blue: Initial target location
  - Yellow: Found closest spot

## Dependencies

### C++

- C++17 or later
- Standard library

### Python

`pip install fastapi`
`pip install uvicorn `
`pip install jinja2`

## Usage

1.  Generate test cases:
    `python generate_tests.py`

2.  Run the C++ program to find the closest spot:
    `g++ main.cpp -o parking ./parking`

3.  Start the visualization server:
    `cd web`
    `run.bat`

4.  Open a web browser and navigate to:
    `http://localhost:8000`

## File Structure

- `main.cpp`: Main C++ program with BFS implementation
- `main.py`: FastAPI server for visualization
- `web`: Contains web visualization server
- `generate_tests.py`: Test case generator

## Algorithm

The program uses Breadth-First Search (BFS) to find the closest empty parking spot, guaranteeing the optimal solution with minimum distance.
