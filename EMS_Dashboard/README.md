# Pod Status Dashboard

A simple dashboard built with Python, Plotly, and Dash to visualize pod status information from a text file.

## Requirements
- Python 3.x
- dash
- plotly
- pandas

## Setup
1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install dash plotly pandas
   ```

## Running the Dashboard
1. Make sure `pods_status.txt` is in the same directory as `app.py`
2. Run the application:
   ```
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:8050`

## Features
- Pie chart showing the distribution of pod statuses
- Detailed table view of all pods and their current states