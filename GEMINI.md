# Gemini Custom Instructions

This file provides instructions for Gemini to follow when interacting with this project.

## Project Overview

This project is a FastAPI application for managing products. It uses a PostgreSQL database and is set up to run with Docker.

- **Framework:** FastAPI
- **Database:** PostgreSQL (via `sqlmodel`)
- **Linting:** `ruff`
- **Testing:** `pytest`

## Development Workflow

### Running the Application

The application is containerized with Docker. To run the application:

1.  Start the services: `docker-compose up -d`
2.  The API will be available at `http://localhost:8000`.

To run the application locally without Docker:

1.  Ensure you have a running PostgreSQL instance.
2.  Set the `DATABASE_URL` environment variable.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the application: `uvicorn main:app --reload`

### Running Tests

Tests are located in the `tests/` directory and use `pytest`. To run the tests, execute:

```bash
pytest
```

### Linting

This project uses `ruff` for linting. To check for linting errors, run:

```bash
ruff check .
```

To automatically fix linting errors, run:

```bash
ruff check . --fix
```

## Code Style and Conventions

- Follow PEP 8 guidelines.
- Use type hints for all function signatures.
- Keep functions small and focused on a single task.
- Write clear and concise docstrings for all public modules and functions.
