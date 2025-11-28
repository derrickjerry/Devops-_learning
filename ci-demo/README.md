# Install dependencies
pip install -r requirements.txt

# Run locally
python app/main.py

# Test API
curl http://localhost:5000/todos
curl -X POST http://localhost:5000/todos -H "Content-Type: application/json" -d '{"task":"CI Demo"}'

# Run tests
pytest -v --cov=app

##### Run lint
flake8 app tests

## Python close
