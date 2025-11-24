import dash
from dash import dcc, html
import pandas as pd
from ..utils.file_reader import read_service_status

# Initialize the Dash app
app = dash.Dash(__name__)

# Read service status data
service_data = read_service_status()

# Create layout components for the dashboard
app.layout = html.Div([
    html.H1("Service Status Dashboard"),
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
    ),
    html.Table(
        # Header
        [html.Tr([html.Th("Service"), html.Th("Status")])] +
        # Body
        [html.Tr([html.Td(service), html.Td(status)]) for service, status in zip(service_data['Service'], service_data['Status'])]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)