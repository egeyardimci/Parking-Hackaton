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

# Parking Lot Data Format

This section explains the structure and meaning of the provided parking lot data format.

## Structure Overview

The data format consists of the following components:

1. **Starting Point (Line 1)**:  
   Specifies the starting point for a search or operation in the parking lot.  
   The format is:

- `row` is the zero-based row index.
- `column` is the zero-based column index.

2.  **Test Name (Line 2)**:  
    Provides a descriptive name for the current test scenario. This name can be used to identify the specific configuration being tested.
3.  **Parking Lot Matrix (Remaining Lines)**:  
    A matrix where each cell represents a parking space:

    - `1`: Occupied parking space.
    - `0`: Empty parking space.

## Example Input Data

Here is an example dataset with its explanation:

    3 3
    2x2 cluster near middle
    0 0 0 0 0
    0 0 0 0 0
    1 0 0 0 0
    0 0 0 1 1
    0 0 0 1 1

### Explanation:

1.  **Starting Point**:  
    `3 3`  
    This indicates the starting point is at row 3, column 3 (zero-based indexing).
2.  **Test Name**:  
    `2x2 cluster near middle`  
    This test name describes the parking lot's scenario, where there is a 2x2 cluster of occupied spaces near the center.
3.  **Parking Lot Matrix**:

        0 0 0 0 0
        0 0 0 0 0
        1 0 0 0 0
        0 0 0 1 1
        0 0 0 1 1

- Rows 0 and 1 contain only empty spaces.
- Row 2 has an occupied space at column 0.
- Rows 3 and 4 form a 2x2 cluster of occupied spaces starting at column 3.

### Notes

- The matrix can have any dimensions, and all rows must have the same number of columns.
- The starting point should always fall within the bounds of the matrix.

# Dependencies

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
    `g++ parkhack.cpp -o parking`

3.  Start the visualization server:
    `cd web`
    `uvicorn main:app --reload`

4.  Open a web browser and navigate to:
    `http://localhost:8000`

# File Structure

- `parkhack.cpp`: Main C++ program with BFS implementation
- `main.py`: FastAPI server for visualization
- `web`: Contains web visualization server
- `generate_tests.py`: Test case generator

# Algorithm

The program uses Breadth-First Search (BFS) to find the closest empty parking spot, guaranteeing the optimal solution with minimum distance.
