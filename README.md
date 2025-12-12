# fastapi-template

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-CC--BY--NC--ND--4.0-orange.svg)](LICENSE)

Production-ready FastAPI template with built-in observability, async-first architecture, and comprehensive testing support.

## 🚀 Quick Start

### Prerequisites

- **Python** ≥ 3.9 (tested up to 3.13)
- **pip/venv** (standard Python tooling)

### Setup

```bash
git clone https://github.com/IHCantabria/fastapi-template.git
cd fastapi-template

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment (optional)
cp .env .env.local

# Run development server
python -m uvicorn src.main:app --reload

# Run tests
pytest
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📁 Project Structure

```text
src/
├── main.py              # FastAPI application entry point
├── config/env.py        # Environment variables
├── routers/test.py      # Example API endpoints
├── models/              # Pydantic data models
├── services/            # Business logic layer
└── core/                # Core utilities (telemetry, middleware, etc.)
```

## 🔧 Environment Variables

Configure your application with `.env` file:

```bash
# App settings
APP_ENV=local                           # local | development | production
API_PREFIX=/v1/public                   # Route prefix
TMP_DIR=./tmp                           # Temporary directory

# Observability (optional)
EXPORT_TRACES=false                     # Enable OpenTelemetry export
OTEL_SERVICE_NAME=fastapi-template      # Service identifier
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## :package: Dependencies

### Production (API Runtime)

- **FastAPI** ≥0.121.2 - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **OpenTelemetry** (optional) - Distributed tracing
- **email-validator** - Email validation

### Development & Testing

- **pytest** - Testing framework
- **ruff** - Linter and formatter

## 📚 API Endpoints

Test endpoints available at `/v1/public/test/`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/healthcheck` | GET | Health status |
| `/error` | GET | Error handling demo |
| `/logs` | GET | Logging demo |
| `/http-client` | GET | HTTP request tracing |
| `/nested-operations` | GET | Nested trace demo |

## 🧪 Testing

```bash
# Run all tests
pytest .

# Generate coverage
coverage run      # generate coverage analisis (creates `.coverage` file)
coverage report   # generate coverage report pormpt (uses `.coverage` file)
coverage html     # generate html report (uses `.coverage` file)

# View HTML coverage report on htmlcov/index.html
```

## 🛠️ Advanced Setup (Optional)

### Using `uv` Package Manager

If you prefer `uv` instead of `pip`:

```bash
# Install uv
pip install uv

# Install dependencies
uv sync --frozen

# Update dependencies
uv lock --upgrade
```

### Docker Deployment

Build and run the API in a container:

```bash
# Build image
docker build -t fastapi-template:latest .

# Run container
docker run -p 8000:8000 \
  -e APP_ENV=development \
  fastapi-template:latest
```

### VS Code Dev Container

Complete development environment pre-configured with Python, uv, Ruff, and all extensions:

1. Install VS Code extension: **Dev Containers**
2. Press `Ctrl+Shift+P` and run **Dev Containers: Reopen in Container**

### Code Quality Tools

Using **Ruff** for linting and formatting:

```bash
# Format code
ruff format .

# Check and auto-fix issues
ruff check . --fix
```

## 📋 License

This project is licensed under **CC-BY-NC-ND-4.0**. See [LICENSE](LICENSE) for details.

## :copyright: Credits

Developed by [Germán Aragón](https://github.com/aragong) @ [IHCantabria](https://ihcantabria.com/en)
