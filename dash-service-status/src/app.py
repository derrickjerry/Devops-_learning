import dash
from dash import dcc, html
import pandas as pd
from src.utils.file_reader import read_service_status

# Initialize the Dash app
app = dash.Dash(__name__)

# Read service status data
service_data = read_service_status('src/data/service_status.txt')

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Service Status Dashboard'),

    dcc.Graph(
        id='service-status-graph',
        figure={
            'data': [
                {'x': service_data['Service'], 'y': service_data['Status'], 'type': 'bar', 'name': 'Status'},
            ],
            'layout': {
                'title': 'Service Status Overview'
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)