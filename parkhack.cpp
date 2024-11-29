#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <queue>

// ANSI escape codes for colors
#define RED "\033[31m"
#define GREEN "\033[32m"
#define BLUE "\033[34m"
#define YELLOW "\033[33m"
#define RESET "\033[0m"

using Matrix = std::vector<std::vector<int>>;

std::vector<std::vector<int>> readMatrixFromFile(const std::string& filename, std::pair<int, int> &targetPos, std::string &testDescription) {
    std::vector<std::vector<int>> matrix;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return matrix;
    }

    std::string target;

    std::getline(file, target);

    std::istringstream iss(target);
    int value;
    iss >> value;
    targetPos.first = value;
    iss >> value;
    targetPos.second = value;

    std::getline(file, testDescription);


    std::string line;
    while (std::getline(file, line)) {
        std::vector<int> row;
        std::istringstream iss(line);
        int value;
        while (iss >> value) {
            row.push_back(value);
        }
        matrix.push_back(row);
    }

    file.close();
    return matrix;
}

static std::pair<int, int> findClosestEmptyPoint(
    const Matrix& matrix,
    const std::pair<int, int>& target,
    int& distanceToTarget
) {
    int rows = matrix.size();
    int cols = matrix[0].size();

    // Initialize visited matrix
    std::vector<std::vector<bool>> visited(rows, std::vector<bool>(cols, false));

    // Queue to store positions and their distances
    // Each element contains: {{row, col}, distance}
    std::queue<std::pair<std::pair<int, int>, int>> q;

    // Direction arrays for moving up, right, down, left
    const int dr[] = { -1, 0, 1, 0 };
    const int dc[] = { 0, 1, 0, -1 };

    // Start BFS from target position
    q.push({ target, 0 });
    visited[target.first][target.second] = true;

    while (!q.empty()) {
        // Get current position and distance
        auto current = q.front();
        int curr_row = current.first.first;
        int curr_col = current.first.second;
        int curr_distance = current.second;
        q.pop();

        // If we found an empty spot, this is the closest one (due to BFS)
        if (matrix[curr_row][curr_col] == 0) {
            distanceToTarget = curr_distance;
            return { curr_row, curr_col };
        }

        // Try all four directions
        for (int i = 0; i < 4; i++) {
            int new_row = curr_row + dr[i];
            int new_col = curr_col + dc[i];

            // Check if new position is valid and not visited
            if (new_row >= 0 && new_row < rows &&
                new_col >= 0 && new_col < cols &&
                !visited[new_row][new_col]) {

                // Add new position to queue with incremented distance
                q.push({ {new_row, new_col}, curr_distance + 1 });
                visited[new_row][new_col] = true;
            }
        }
    }

    // If no empty spot found
    distanceToTarget = -1;
    return { -1, -1 };
}

void printColoredMatrix(const Matrix& matrix, int foundSpotRow, int foundSpotCol, int targetSpotRow, int targetSpotCol) {
    int n = matrix.size(); // Get matrix dimension

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == foundSpotRow && j == foundSpotCol) {
                std::cout << BLUE << matrix[i][j] << " " << RESET;
            }
            else if (i == targetSpotRow && j == targetSpotCol) {
                std::cout << YELLOW << matrix[i][j] << " " << RESET;
            }
            else if (matrix[i][j] == 1) {
                std::cout << RED << matrix[i][j] << " " << RESET;
            }
            else {
                std::cout << GREEN << matrix[i][j] << " " << RESET;
            }
        }
        std::cout << std::endl;
    }
}

void saveMatrix(const Matrix& matrix, int distance,int foundSpotRow, int foundSpotCol,
    int targetSpotRow, int targetSpotCol, const std::string& filename, std::string& testDescription) {
    std::ofstream outFile(filename);
    outFile << distance << std::endl;
    outFile << testDescription << std::endl;
    if (!outFile.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return;
    }

    int n = matrix.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == foundSpotRow && j == foundSpotCol) {
                outFile << 3 << " ";
            }
            else if (i == targetSpotRow && j == targetSpotCol) {
                outFile << 2 << " ";
            }
            else if (matrix[i][j] == 1) {
                outFile << matrix[i][j] << " ";
            }
            else {
                outFile << matrix[i][j] << " ";
            }
        }
        outFile << "\n";
    }
    outFile.close();
}

std::pair<int, int> runTest(Matrix& matrix, std::pair<int, int> &targetPos, int &distance) {
    std::pair<int, int> res = findClosestEmptyPoint(matrix, targetPos, distance);

    printColoredMatrix(matrix, res.first, res.second, targetPos.first,targetPos.second);

    std::cout << YELLOW << "Target parking spot was: " << "(" << targetPos.first << "," << targetPos.second << ")" << RESET << std::endl;
    std::cout << BLUE << "Best parking spot is: " << "(" << res.first << "," << res.second << "),With distance: " << RESET << distance << std::endl << std::endl;

    return res;
}

void moveMatrixFile() {
#ifdef _WIN32
    system("mkdir web 2> nul");  // Windows
    system("move /Y matrix.txt web\\matrix.txt > nul 2>&1");
#else
    system("mkdir -p web");      // Unix/Linux/MacOS
    system("mv matrix.txt web/matrix.txt 2>/dev/null");
#endif
}

void openChrome() {
#ifdef _WIN32
    // Windows
    system("start chrome http://localhost:8000 >nul 2>&1");
#elif __APPLE__
    // macOS
    system("open -a \"Google Chrome\" http://localhost:8000 >/dev/null 2>&1");
#else
    // Linux and other Unix-like systems
    system("google-chrome http://localhost:8000 >/dev/null 2>&1");
#endif
}

void programLoop() {
    while (true) {
        int distance;
        std::string testDescription;

        std::cout << "Please type one of the commands (run-tests,run,visualize,exit): ";
        std::string input;
        std::cin >> input;
        if (input == "exit") {
            return;
        }
        else if (input == "run-tests") {
            int testCount = 24;
            Matrix matrix;
            std::pair<int, int> targetPos;
            std::pair<int, int> result;

            for (int i = 1; i < testCount; i++) {
 
                std::string fileName = "test" + std::to_string(i) + ".txt";
                matrix = readMatrixFromFile(fileName, targetPos, testDescription);
   

               result = runTest(matrix, targetPos,distance);
            }
            saveMatrix(matrix,distance , result.first, result.second, targetPos.first, targetPos.second, "matrix.txt", testDescription);
            moveMatrixFile();
        }
        else if (input == "run") {
            std::cout << "Please enter the name of input file: ";
            std::string fileName;
            std::cin >> fileName;
            std::cout << std::endl;
            
            std::pair<int, int> targetPos;
            Matrix matrix = readMatrixFromFile(fileName, targetPos,testDescription);

            std::pair<int, int> result = runTest(matrix, targetPos,distance);
            saveMatrix(matrix,distance,result.first,result.second,targetPos.first,targetPos.second,"matrix.txt", testDescription);
            moveMatrixFile();
        }
        else if (input == "visualize") {
            openChrome();
        }
    }
}

int main()
{
    programLoop();

}