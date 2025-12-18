---
applyTo: 'README.md'
---

# README Documentation Standards

## Automatic Updates

When making changes to the project, **always update the README** if:
- New endpoints are added to the API
- Environment variables are added or modified
- Dependencies are added or changed
- New features or modules are implemented
- Setup or deployment steps change

## Required Sections

### 1. Header & Badges
- Project name with clear description
- Badges: Python version, FastAPI version, License, Build status
- Brief one-line description of what the project does

### 2. Overview
- What is this project?
- Main purpose and use cases
- Key features (3-5 bullet points)
- Architecture diagram (optional but recommended)

### 3. Quick Start
```bash
# Complete setup from clone to running server
git clone [repo]
cd [project]
python -m venv .venv
source .venv/bin/activate
uv sync --frozen
python -m uvicorn template_api.main:app --app-dir src --reload
```

### 4. Project Structure
- Directory tree with descriptions
- Explain the monorepo structure (api vs lib)
- Purpose of each main directory

### 5. Environment Variables
**Complete table format:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_ENVIRONMENT` | Yes | `local` | Environment mode: local/development/production |
| `API_PREFIX` | No | `/v1/public` | API route prefix |
| ... | ... | ... | ... |

Include example `.env` file content.

### 6. API Endpoints
**Organized by router/tag:**

#### Test Endpoints (`/v1/public/test`)
| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/healthcheck` | GET | Service health status | - | `{status: "ok"}` |
| ... | ... | ... | ... | ... |

### 7. Development

#### Installation Options
- Standard pip installation
- UV package manager (preferred)
- Dev container setup

#### Running Locally
```bash
# Development server
python -m uvicorn template_api.main:app --app-dir src --reload

# With custom host/port
python -m uvicorn template_api.main:app --app-dir src --host 0.0.0.0 --port 8080
```

#### Code Quality
```bash
# Formatting
ruff format .

# Linting
ruff check . --fix

# Type checking (if applicable)
mypy src/
```

### 8. Testing

#### Running Tests
```bash
# All tests
pytest .

# Specific test file
pytest src/template_api/tests/test_api.py -v

# With coverage
coverage run && coverage report
coverage html  # Generate HTML report
```

#### Test Structure
- Where tests are located
- How to add new tests
- Testing patterns used (TestClient, fixtures, etc.)

### 9. Observability

#### OpenTelemetry Setup
- How tracing works in this project
- Required OTLP endpoint configuration
- Enabling/disabling traces
- Log correlation with traces

#### Monitoring
- Available metrics
- Log aggregation setup
- Trace visualization tools (Jaeger, Zipkin, etc.)

### 10. Deployment

#### Docker
```bash
# Build
docker build -t template-api:latest .

# Run
docker run -p 8000:8000 -e APP_ENVIRONMENT=production template-api:latest
```

#### Production Considerations
- Environment-specific configurations
- Recommended settings for production
- Security considerations

### 11. Dependencies

#### Core Dependencies
List and explain main dependencies:
- **FastAPI** - Web framework
- **OpenTelemetry** - Observability
- **Uvicorn** - ASGI server
- etc.

#### Development Dependencies
- pytest, ruff, coverage, etc.

### 12. Workspace Structure

Explain the UV workspace setup:
```toml
[tool.uv.workspace]
members = ["src/template_api", "src/template_lib"]
```
- How packages interact
- When to add code to API vs LIB
- Dependency management between packages

### 13. Contributing (Optional)
- Code style guide
- Pull request process
- Testing requirements

### 14. License & Credits
- License type and restrictions
- Author information
- Organization/institution

## Formatting Standards

- Use emoji icons for visual sections (🚀 ⚙️ 📚 🧪 🐳 etc.)
- Code blocks must specify language (```bash, ```python, etc.)
- Keep command examples copy-pasteable
- Use tables for structured data
- Include links to relevant files using relative paths
- Add "Back to top" links for long sections

## Length Target

- **Minimum**: 200 lines
- **Target**: 300-400 lines
- **Maximum**: No limit if content is valuable

Focus on completeness and clarity over brevity.
