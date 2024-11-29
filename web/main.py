from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create the templates directory and add the HTML file
if not os.path.exists("templates"):
    os.makedirs("templates")

# Create HTML template with Jinja2 syntax
html_template = """
<!DOCTYPE html>
<html>
<head>
<style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #f5f5f5;
            font-family: Arial, sans-serif;
        }

        .container {
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            display: flex;           /* Added */
            flex-direction: column;  /* Added */
            align-items: center;     /* Added */
        }

        .title {
            text-align: center;
            color: #333;
            font-size: 1.5rem;
            font-weight: bold;
        }

        .parking-grid {
            display: inline-grid;
            grid-template-columns: repeat({{ matrix|length }}, 40px);
            gap: 4px;
            background: #ddd;
            padding: 4px;
            border-radius: 4px;
            margin: 0 auto;          /* Added */
        }

        .parking-spot {
            width: 40px;
            height: 40px;
            border-radius: 4px;
            transition: transform 0.2s ease;
        }

        .parking-spot:hover {
            transform: scale(0.95);
        }
        p{
            margin: 2px;
        }

        .occupied {
            background: #ff4444;
        }

        .empty {
            background: #4CAF50;
        }
        
        .target {
            background: #2196F3;
        }
        
        .found {
            background: #FFC107;
        }

        .legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 2rem;
            color: #333;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .legend-square {
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">Parking Lot Status</div>
        <p>Scenario: {{description}} </p>
        <p> Distance: {{distance}}</p>
        <div class="parking-grid">
            {% for row in matrix %}
                {% for cell in row %}
                    {% if cell == 0 %}
                        <div class="parking-spot empty"></div>
                    {% elif cell == 1 %}
                        <div class="parking-spot occupied"></div>
                    {% elif cell == 2 %}
                        <div class="parking-spot target"></div>
                    {% elif cell == 3 %}
                        <div class="parking-spot found"></div>
                    {% endif %}
                {% endfor %}
            {% endfor %}
        </div>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-square" style="background: #4CAF50;"></div>
                <span>Empty Spot</span>
            </div>
            <div class="legend-item">
                <div class="legend-square" style="background: #ff4444;"></div>
                <span>Occupied Spot</span>
            </div>
            <div class="legend-item">
                <div class="legend-square" style="background: #2196F3;"></div>
                <span>Initial Spot</span>
            </div>
            <div class="legend-item">
                <div class="legend-square" style="background: #FFC107;"></div>
                <span>Found Spot</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Save the template
with open("templates/parking.html", "w") as f:
    f.write(html_template)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # Read matrix from file
    isFirstLine = True
    isSecondLine = True
    distance = -1
    description = ""
    matrix = []
    with open("matrix.txt", "r") as file:
        for line in file:
            if(isFirstLine):
                distance = line
                isFirstLine = False
            elif (isSecondLine):
                description = line
                isSecondLine = False
            else:
                # Convert each line to list of integers
                row = [int(x) for x in line.strip().split()]
                matrix.append(row)
    
    return templates.TemplateResponse("parking.html", {"request": request, "matrix": matrix , "distance" : distance, "description" : description})

# To run:
# 1. pip install fastapi uvicorn jinja2
# 2. Make sure matrix.txt exists with your matrix data
# 3. Run: uvicorn main:app --reload