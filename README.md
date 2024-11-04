# LLMAgent Server

This project is a FastAPI application for managing file operations using an agent.

## Installation

To install the dependencies, run:

```bash
poetry install
```

## Usage
To use this app, run server

```bash
poetry run python app.py
```

After the server is running, you can send POST requests to interact with the agent. For example, to list all .txt files in the current directory, use the following curl command:
```bash
curl -X POST "http://0.0.0.0:8000/agent" -H "Content-Type: application/json" -d '{"msg": "List all txt files in this directory"}'
```

## Tests
To run tests
```bash
poetry run pytest python -m pytest
```
