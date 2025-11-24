import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import datetime
import os
import sys

def get_status_files():
    """Get all status text files from environment directories"""
    # Use absolute path
    current_dir = r'c:\Users\Admin\Documents\Devops learnin\EMS_Dashboard'
    envs = ['PL1', 'PL2', 'PL3']
    files = []
    for env in envs:
        env_dir = os.path.join(current_dir, env)
        if os.path.exists(env_dir):
            for file_name in ['pods_status.txt', 'services_status.txt']:
                file_path = os.path.join(env_dir, file_name)
                if os.path.exists(file_path):
                    files.append(file_path)
    print(f"\nFound files: {files}")
    return files

def read_status_file(filename):
    """Read a status file and return its data"""
    data = []
    try:
        print(f"\nAttempting to read file: {filename}")
        if not os.path.exists(filename):
            print(f"File does not exist: {filename}")
            return data
            
        with open(filename, 'r') as file:
            print(f"Successfully opened {filename}")
            content = file.readlines()
            print(f"Read {len(content)} lines")
            
            # Get component type from filename (e.g., 'pods' from 'pods_status.txt')
            base_name = os.path.basename(filename)
            component_type = base_name.split('_')[0].capitalize()
            print(f"Component type: {component_type}")
            
            for line in content:
                name, status, state, env = line.strip().split(',')
                print(f"Processing: {name}, {status}, {state}, {env}")
                
                # Standardize status to 'up'/'down'
                if status.lower() in ['running', 'up']:
                    status = 'up'
                else:
                    status = 'down'
                
                entry = {
                    'Name': name,
                    'Status': status,
                    'State': state,
                    'Type': component_type,
                    'Environment': env
                }
                print(f"Adding entry: {entry}")
                data.append(entry)
                
            print(f"Successfully processed {len(data)} entries from {filename}")
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    return data

def read_all_data():
    """Read all status files and combine their data"""
    print("\n=== Reading All Status Files ===")
    all_data = []
    
    # Get list of status files
    status_files = get_status_files()
    print(f"Found status files: {status_files}")
    
    # Read each status file
    for filename in status_files:
        file_data = read_status_file(filename)
        all_data.extend(file_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    if len(df) == 0:
        df = pd.DataFrame(columns=['Name', 'Status', 'State', 'Type', 'Environment'])
    
    print("\nFinal Combined Data:")
    print(f"Total records: {len(df)}")
    print(df)
    
    return df

# Initialize the Dash app
app = dash.Dash(__name__, 
    external_stylesheets=[
        'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
    ])

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .container-fluid { max-width: 1200px; margin: auto; }
            .alert { 
                font-size: 0.8rem; 
                margin-bottom: 0.2rem !important;
                padding: 0.2rem 0.5rem !important;
            }
            .pods-container, .services-container { 
                max-height: 200px; 
                overflow-y: auto;
                padding: 0.3rem;
                background-color: rgba(0,0,0,0.05);
                border-radius: 4px;
            }
            .alert-success { background-color: #28a745; color: white; }
            .alert-danger { background-color: #dc3545; color: white; }
            h4 { font-size: 1.1rem; margin-bottom: 0.5rem !important; }
            h5 { font-size: 0.9rem; margin-bottom: 0.3rem !important; }
            .mt-3 { margin-top: 0.5rem !important; }
            .mb-2 { margin-bottom: 0.3rem !important; }
            .py-1 { padding-top: 0.15rem !important; padding-bottom: 0.15rem !important; }
            .rounded { border-radius: 0.2rem !important; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Create the layout
app.layout = html.Div(className='container-fluid', children=[
    dcc.Interval(
        id='interval-component',
        interval=5000,  # in milliseconds (5 seconds)
        n_intervals=0
    ),
    
    # Header with last update time
    html.Div(className='row mt-3', children=[
        html.Div(className='col-12', children=[
            html.H1('MM Dashboard', className='text-center'),
            html.H4('Environment Status Monitor', className='text-center text-muted mb-2'),
            html.P(id='last-update-time', className='text-center text-muted')
        ])
    ]),
    
    # Dynamic summary cards
    html.Div(id='summary-cards', className='row mt-3'),
])

@app.callback(
    [Output('summary-cards', 'children'),
     Output('last-update-time', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n_intervals):
    # Read all data
    df = read_all_data()
    
    # Create summary cards
    summary_cards = []
    environments = ['PL1', 'PL2', 'PL3']
    
    for env in environments:
        env_df = df[df['Environment'] == env]
        env_components = []
        
        # Separate pods and services
        pods_df = env_df[env_df['Type'] == 'Pods']
        services_df = env_df[env_df['Type'] == 'Services']
        
        # Create pods section
        pods_section = html.Div(className='col-6', children=[
            html.H5('Pods', className='text-center mb-2'),
            html.Div(className='pods-container', children=[
                html.Div(className=f'alert alert-{"success" if row["Status"] == "up" else "danger"} py-1 mb-1 d-flex justify-content-between align-items-center', children=[
                    html.Span(row['Name'], className='font-weight-bold'),
                    html.Small(row['State'])
                ]) for _, row in pods_df.iterrows()
            ])
        ])
        
        # Create services section
        services_section = html.Div(className='col-6', children=[
            html.H5('Services', className='text-center mb-2'),
            html.Div(className='services-container', children=[
                html.Div(className=f'alert alert-{"success" if row["Status"] == "up" else "danger"} py-1 mb-1 d-flex justify-content-between align-items-center', children=[
                    html.Span(row['Name'], className='font-weight-bold'),
                    html.Small(row['State'])
                ]) for _, row in services_df.iterrows()
            ])
        ])
        
        env_components.extend([pods_section, services_section])
        
        summary_cards.append(
            html.Div(className='col-md-4 mb-2', children=[
                html.H4(f'{env}', className='text-center mb-2 bg-info text-white py-1 rounded'),
                html.Div(className='row mx-0', children=env_components)
            ])
        )
    
    # Get current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return summary_cards, f'Last Updated: {current_time}'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050)