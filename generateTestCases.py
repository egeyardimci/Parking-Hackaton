import random

def generate_test_case(n, occupied_percentage, target_row, target_col, description, filename):
    """
    Generate a parking lot test case ensuring target is part of a 2x2 occupied cluster
    """
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    if(occupied_percentage != 0):
        
        # First, create a 2x2 cluster of 1s that includes the target
        # Adjust target position to ensure we can place a 2x2 cluster
        cluster_row = min(target_row, n-2)  # Ensure we have room for 2x2 cluster
        cluster_col = min(target_col, n-2)
        
        # Place 2x2 cluster
        for i in range(2):
            for j in range(2):
                matrix[cluster_row + i][cluster_col + j] = 1
        
        # Calculate remaining occupied spots needed (subtract 4 for the cluster we just placed)
        total_spots = n * n
        occupied_spots = int(total_spots * occupied_percentage / 100) - 4
        occupied_spots = max(0, occupied_spots)  # Ensure we don't go negative
        
        # Fill remaining spots
        while occupied_spots > 0:
            row = random.randint(0, n-2)
            col = random.randint(0, n-2)
            
            # Create additional clusters avoiding existing 1s
            for i in range(2):
                for j in range(2):
                    if (occupied_spots > 0 and 
                        row+i < n and col+j < n and 
                        matrix[row+i][col+j] == 0):
                        matrix[row+i][col+j] = 1
                        occupied_spots -= 1

    # Write matrix and target info to file
    with open(filename, 'w') as f:
        # Then write target location and description
        f.write(f"{target_row} {target_col}\n")
        f.write(f"{description}\n")
        # First write the matrix
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

def generate_multiple_test_cases(base_filename, cases):
    for i, (size, percentage, target_row, target_col, description) in enumerate(cases, 1):
        filename = f"{base_filename}{i}.txt"
        generate_test_case(size, percentage, target_row, target_col, description, filename)
        print(f"Generated test case {i}: {size}x{size} matrix with {percentage}% occupied spots")
        print(f"Target location: ({target_row},{target_col}) - {description}")
        print("-" * 50)

test_cases = [
    # Format: (size, occupied_percentage, target_row, target_col, description)
    
    # Basic cases - ensuring targets are part of 2x2 clusters
    (5, 20, 3, 3, "2x2 cluster near middle"),
    (5, 40, 3, 3, "2x2 cluster in middle"),
    
    # Different sizes
    (6, 30, 2, 2, "Small cluster"),
    (7, 30, 4, 4, "Mid-size cluster"),
    (10, 30, 6, 6, "Large lot cluster"),
    
    # Different occupancy rates
    (6, 20, 2, 2, "Sparse lot cluster"),
    (6, 40, 3, 3, "Medium density cluster"),
    (6, 60, 2, 2, "High density cluster"),
    (6, 80, 3, 3, "Very high density cluster"),
    
    # Edge cases
    (4, 25, 0, 0, "Corner cluster"),
    (4, 90, 2, 2, "Full lot cluster"),
    (8, 40, 4, 4, "Center cluster"),
    
    # Specific scenarios
    (8, 35, 4, 0, "Left edge cluster"),
    (8, 45, 6, 6, "Far corner cluster"),
    (5, 60, 2, 2, "Dense small lot cluster"),
    
    # Real-world inspired
    (7, 40, 4, 4, "Mall parking cluster"),
    (7, 70, 2, 2, "Peak hours cluster"),
    (10, 80, 6, 6, "Event parking cluster"),

    # Big Cases
    (15, 40, 6, 8, "Mall parking cluster"),
    (20, 70, 1, 8, "Peak hours cluster"),

    (6, 100, 3, 3, "Completely full lot"),
    (6, 0, 3, 3, "Completely empty lot"),
]

# Generate all test cases
generate_multiple_test_cases("test", test_cases)