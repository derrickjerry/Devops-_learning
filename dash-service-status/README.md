# Dash Service Statusss Dashboard

This project is a Dash application that reads service status details from a text file and displays them on a dashboard.

## Project Structure

- `src/app.py`: Entry point of the Dash application.
- `src/components/dashboard.py`: Contains layout components for the dashboard.
- `src/data/service_status.txt`: Text file with service status details.
- `src/utils/file_reader.py`: Utility functions for reading the service status file.
- `tests/test_file_reader.py`: Unit tests for file reading functions.
- `requirements.txt`: Lists project dependencies.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd dash-service-status
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:8050` to view the dashboard.
