# FastAPI Library Template

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-CC--BY--NC--ND--4.0-orange.svg)](LICENSE)

Production-ready FastAPI monorepo template with built-in observability, async-first architecture, and comprehensive testing support.

## 📋 Overview

This template provides a complete foundation for building FastAPI applications with:

- **Monorepo workspace structure** - Separate API and library packages managed by `uv`
- **OpenTelemetry integration** - Full observability with traces, logs, and metrics
- **Async-first design** - Built for high-performance async operations
- **Type safety** - Pydantic models and type hints throughout
- **Dev container ready** - Complete development environment with VS Code
- **Production tested** - Battle-tested patterns and best practices

### Architecture

```text
src/
├── template_api/          # FastAPI web service
│   ├── main.py           # Application entry point
│   ├── config/           # Environment configuration
│   ├── core/             # Telemetry, middleware, utilities
│   ├── routers/          # API endpoint definitions
│   │   └── test.py       # Example test router
│   ├── services/         # Business logic layer
│   ├── models/           # Pydantic data models
│   └── tests/            # API tests
│       ├── e2e/          # End-to-end tests (no mocking)
│       └── unit/         # Unit tests (fast, isolated)
│
└── template_lib/          # Reusable library package
    ├── models/           # Shared data models
    ├── services/         # Data processing logic
    └── tests/            # Library tests
        ├── e2e/          # End-to-end tests
        └── unit/         # Unit tests
```

## 🎯 Using This Template

### 1. Create Your Project

Click "Use this template" button or:

```bash
git clone https://github.com/IHCantabria/fastapi-template.git your-project-name
cd your-project-name
```

### 2. Rename Packages

**Critical**: Replace `template_api` and `template_lib` with your actual package names:

```bash
# Rename directories
mv src/template_api src/your_api_name
mv src/template_lib src/your_lib_name

# Update workspace configuration in pyproject.toml
# Change:
#   members = ["src/template_api", "src/template_lib"]
# To:
#   members = ["src/your_api_name", "src/your_lib_name"]

# Update package names in:
# - src/your_api_name/pyproject.toml (name = "your-api-name")
# - src/your_lib_name/pyproject.toml (name = "your-lib-name")
# - All import statements throughout the codebase
```

### 3. Update Metadata

Edit `src/your_api_name/pyproject.toml`:

```toml
[project]
name = "your-api-name"
version = "0.1.0"
description = "Your API description"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env .env.local

# Edit .env.local with your settings
# At minimum, update:
# - OTEL_SERVICE_NAME
# - API_PREFIX (if needed)
# - OTEL_EXPORTER_OTLP_ENDPOINT (if using observability)
```

## 🚀 Quick Start

### Prerequisites

- **Python** ≥ 3.9 (tested up to 3.13)
- **uv** package manager (recommended) or pip/venv

### Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (recommended: uv)
uv sync --frozen

# Or use pip
pip install -e ".[dev]"
```

### Running the API

```bash
# Development server with auto-reload
python -m uvicorn template_api.main:app --app-dir src --reload

# Custom host/port
python -m uvicorn template_api.main:app --app-dir src --host 0.0.0.0 --port 8080 --reload
```

**Important**: The `--app-dir src` flag is required because packages are located in `src/`, not at repo root.

Visit <http://localhost:8000/docs> for interactive API documentation.

### Running Tests

```bash
# All tests
pytest .

# With verbose output
pytest -v

# Specific test file
pytest src/template_api/tests/test_api.py -v

# With coverage
coverage run
coverage report
coverage html  # Open htmlcov/index.html
```

## � Environment Variables

All environment variables are managed in [src/template_api/config/env.py](src/template_api/config/env.py).

### Required Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENVIRONMENT` | `local` | Environment mode: `local`, `development`, or `production` |
| `API_PREFIX` | `""` | API route prefix (e.g., `/v1/public`) |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_ROOT_PATH` | `""` | Root path for proxy deployments |
| `TMP_DIR` | `./tmp` | Temporary files directory |
| `EXPORT_TRACES` | `true` | Enable OpenTelemetry trace export |
| `OTEL_SERVICE_NAME` | - | Service name for telemetry |
| `OTEL_SERVICE_VERSION` | - | Service version for telemetry |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | - | OTLP collector endpoint (e.g., `http://localhost:4317`) |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | - | Protocol: `grpc` or `http/protobuf` |
| `OTEL_PYTHON_EXCLUDED_URLS` | `""` | Comma-separated paths to exclude from tracing |

### Example `.env` File

```bash
# Application
APP_ENVIRONMENT=local
API_PREFIX=/v1/public
TMP_DIR=./tmp

# Observability (optional)
EXPORT_TRACES=true
OTEL_SERVICE_NAME=my-fastapi-service
OTEL_SERVICE_VERSION=0.1.0
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_PYTHON_EXCLUDED_URLS=/healthcheck,/metrics
```

## 📦 Dependencies

### Core Dependencies (API)

| Package | Purpose |
|---------|---------|
| **FastAPI** ≥0.121.2 | Modern web framework |
| **Uvicorn** | ASGI server |
| **Pydantic** | Data validation |
| **OpenTelemetry** | Distributed tracing and observability |
| **httpx** | Async HTTP client |
| **email-validator** | Email validation |

### Library Dependencies

| Package | Purpose |
|---------|---------|
| **xarray** | Multi-dimensional data processing |
| **matplotlib** | Data visualization |

### Development Tools

| Package | Purpose |
|---------|---------|
| **pytest** | Testing framework |
| **coverage** | Code coverage analysis |
| **ruff** | Linting and formatting |

### Workspace Management

This project uses **uv workspace** to manage multiple packages:

```toml
[tool.uv.workspace]
members = ["src/template_api", "src/template_lib"]
```

The API depends on the library via workspace dependency:

```toml
[tool.uv.sources]
lib = { workspace = true }
```

## 📚 API Endpoints

### Test Router (`/v1/public/test`)

Example endpoints demonstrating FastAPI patterns and OpenTelemetry integration:

| Endpoint | Method | Description | Purpose |
|----------|--------|-------------|----------|
| `/healthcheck` | GET | Service health check | Verify API is running |
| `/error` | GET | Error handling demo | Exception handling with traceback logging |
| `/external-call` | GET | External HTTP call | Automatic tracing of external services |
| `/processing` | GET | Multi-step workflow | Nested spans + library function call |

### Adding New Endpoints

1. Create router in [src/template_api/routers/](src/template_api/routers/)

2. Use `env.API_PREFIX` for consistency:

    ```python
    from template_api.config.env import env
    from fastapi import APIRouter

    router = APIRouter(tags=["MyFeature"], prefix=env.API_PREFIX + "/myfeature")

    @router.get("/")
    async def my_endpoint():
        return {"message": "Hello"}
    ```

3. Register in [src/template_api/main.py](src/template_api/main.py):

    ```python
    from template_api.routers.myfeature import router as myfeature_router
    app.include_router(myfeature_router)
    ```

## 🧪 Testing

### Running Tests

```bash
# All tests (both packages)
pytest .

# API E2E tests
pytest src/template_api/tests/e2e/ -v

# API unit tests
pytest src/template_api/tests/unit/ -v

# Library tests
pytest src/template_lib/tests/ -v

# Skip slow tests
pytest -m "not slow"

# With coverage
coverage run
coverage report
coverage html  # Open htmlcov/index.html
```

### Test Organization

Tests are organized in **two levels** per package:

```
src/template_api/tests/
├── e2e/              # End-to-end tests (no mocking)
│   └── test_basics.py
└── unit/             # Unit tests (fast, isolated)

src/template_lib/tests/
├── e2e/              # End-to-end tests
└── unit/             # Unit tests
```

**E2E Tests** - Real integration, no mocking:

```python
import pytest
from fastapi.testclient import TestClient
from template_api.main import app

@pytest.mark.e2e
def test_healthcheck(client: TestClient):
    response = client.get("/v1/public/test/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Unit Tests** - Fast, isolated:

```python
from template_lib.services.processing import process_data

def test_processing():
    result = process_data("test input")
    assert result == "TEST INPUT"
```

## 🔍 Observability

### OpenTelemetry Integration

This template includes full OpenTelemetry instrumentation for:

- **Traces**: Automatic span creation for HTTP requests, database calls, and custom operations
- **Logs**: Correlated with trace context for easy debugging
- **Metrics**: Service performance and resource usage

### Configuration

Telemetry is configured in [src/template_api/core/telemetry.py](src/template_api/core/telemetry.py):

```python
# Setup happens in lifespan context BEFORE any logging
setup_opentelemetry()
```

### Conditional Tracing

- **`EXPORT_TRACES=true`**: Exports to OTLP endpoint (production/staging)
- **`EXPORT_TRACES=false`**: Uses `LoggingMiddleware` for local debugging

### Using Traces in Code

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@router.get("/my-endpoint")
async def my_endpoint():
    with tracer.start_as_current_span("custom_operation"):
        # Your code here - automatically traced
        result = await process_data()
    return result
```

### Visualization

Compatible with:

- **Jaeger** - Distributed tracing UI
- **Zipkin** - Trace visualization
- **Grafana Tempo** - Trace storage and querying
- **Seq** - Structured logs with trace correlation

## 🐳 Deployment

### Docker

```bash
# Build image
docker build -t your-api-name:latest .

# Run container
docker run -p 8000:8000 \
  -e APP_ENVIRONMENT=production \
  -e API_PREFIX=/v1/public \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4318/v1 \
  your-api-name:latest
```

### Production Considerations

- Set `APP_ENVIRONMENT=production`
- Configure OTLP endpoint for observability
- Use secrets management for sensitive env vars
- Enable HTTPS/TLS termination at load balancer
- Set appropriate resource limits (CPU/memory)
- Configure health check endpoints for orchestration

## ⚙️ Development

### Package Manager: UV

**Recommended** for faster dependency resolution and workspace management:

```bash
# Install dependencies
uv sync --frozen

# Update lockfile
uv lock --upgrade

# Add dependency to API package
uv add --package template-api fastapi-users

# Add dependency to library package
uv add --package template-lib pandas

# Add development dependency (workspace level)
uv add --dev pytest-asyncio
```

**Important**: In monorepo workspaces, always specify `--package <package-name>` to define which package receives the dependency (`template-api` or `template-lib`).

### Code Quality

```bash
# Format code
ruff format .

# Lint and auto-fix
ruff check . --fix
```

Configuration in [pyproject.toml](pyproject.toml):

- Line length: 120
- Notable rule ignores: `D100` (module docstrings), `T201` (print allowed), `EM101` (inline exception messages)

### Dev Container

Pre-configured development environment in [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json):

- **Base**: Ubuntu 22.04
- **Tools**: Python, uv, Ruff, git, zsh
- **Extensions**: Python, Pylance, Jupyter, TOML, YAML, etc.
- **Shell**: Zsh with syntax highlighting and autosuggestions

**Usage**:

1. Install VS Code extension: **Dev Containers**
2. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**
3. Environment ready immediately

### Project Patterns

#### Logging Convention

Use emoji prefixes for visual clarity (consistent throughout codebase):

```python
logger.info("🚀 Starting application")
logger.warning("⚠️ Configuration missing")
logger.error("❌ Operation failed")
logger.info("✅ Successfully completed")
logger.debug("🔍 Debugging info")
logger.info("📊 Processing data")
```

#### Router Pattern

Always use `env.API_PREFIX` for environment-specific routing:

```python
router = APIRouter(tags=["Feature"], prefix=env.API_PREFIX + "/feature")
```

#### Cross-Package Imports

Import library functions directly in API:

```python
from template_lib.services.processing import process_data
```

Workspace dependency ensures availability without separate installation.

## 🤝 Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for public APIs
- Keep functions focused and small
- Use async/await for I/O operations

### Pull Request Process

1. Create feature branch from `main`
2. Make changes with clear commit messages
3. Run tests and ensure coverage
4. Format with `ruff format .`
5. Fix linting issues with `ruff check . --fix`
6. Submit PR with description of changes

## 📋 License

This project is licensed under **CC-BY-NC-ND-4.0**. See [LICENSE](LICENSE) for details.

**Summary**:

- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ❌ Must give credit
- ❌ Cannot use for commercial purposes
- ❌ Cannot distribute modified versions

## 👥 Credits

**Developed by**: [Germán Aragón](https://github.com/aragong)  
**Organization**: [IHCantabria](https://ihcantabria.com/en)

---

<div align="center">

**[⬆ Back to Top](#fastapi-library-template)**

Made with ❤️ using FastAPI and OpenTelemetry

</div>
