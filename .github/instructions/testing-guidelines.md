---
applyTo: '**/tests/**/*.py'
---

# Testing Guidelines

## Test Structure

Organize tests in **two levels** within each package:

```text
src/template_api/tests/
├── e2e/                    # End-to-end tests
│   ├── test_api_flow.py
│   └── test_integration.py
└── unit/                   # Unit tests
    ├── test_routers.py
    └── test_services.py

src/template_lib/tests/
├── e2e/                    # End-to-end tests
│   └── test_processing_flow.py
└── unit/                   # Unit tests
    ├── test_preprocessing.py
    └── test_postprocessing.py
```

## End-to-End Tests (e2e/)

### Philosophy: Real Integration, Zero Mocking

**Rule**: If you need to mock something, **discard the test** or move it to unit tests.

### Characteristics

- Test complete workflows from start to finish
- Use real dependencies (database, file system, external services)
- Verify actual behavior in realistic scenarios
- **Can take several minutes** - verify critical paths thoroughly
- Minimize the number of long-running tests (focus on essential workflows)
- **No mocks, no stubs, no patches**

### API E2E Example

```python
# src/template_api/tests/e2e/test_api_flow.py
from fastapi.testclient import TestClient
from template_api.main import app

def test_complete_user_workflow():
    """Test entire user journey - no mocking"""
    client = TestClient(app)
    
    # Real API calls, real responses
    response = client.post("/v1/public/data/upload", files={"file": file_content})
    assert response.status_code == 200
    
    data_id = response.json()["id"]
    
    # Continue with real data
    result = client.get(f"/v1/public/data/{data_id}")
    assert result.status_code == 200
    assert result.json()["status"] == "processed"
```

### Library E2E Example

```python
# src/template_lib/tests/e2e/test_processing_flow.py
import xarray as xr
from pathlib import Path
from template_lib.services.preprocessing import clean_data
from template_lib.services.processing import process_data
from template_lib.services.postprocessing import export_results

def test_full_data_pipeline():
    """Test complete data processing pipeline - real files, may take minutes"""
    # Use real test data files
    input_file = Path("tests/fixtures/sample_data.nc")
    output_file = Path("tests/output/result.nc")
    
    # Real file operations - can be computationally intensive
    dataset = xr.open_dataset(input_file)
    cleaned = clean_data(dataset)
    processed = process_data(cleaned)  # May take several minutes with large data
    export_results(processed, output_file)
    
    # Verify real output
    assert output_file.exists()
    result = xr.open_dataset(output_file)
    assert "temperature" in result.variables
```

### Long-Running E2E Tests

**Acceptable**: Tests that take minutes to verify critical functionality

**Strategy**: Keep the number of long tests minimal - focus on essential workflows only

```python
@pytest.mark.slow
@pytest.mark.e2e
def test_heavy_climate_computation():
    """
    Process large climate dataset - may take 5-10 minutes.
    Only test the most critical computation path.
    """
    dataset = load_large_dataset()  # Real large file
    result = complex_climate_analysis(dataset)  # Real computation
    assert result.meets_quality_criteria()
```

### When to Skip E2E Tests

If a test requires:

- External paid API with no test environment
- Services that are unavailable in CI/CD
- Resources that can't be provisioned in test environment

**Solution**: Document why E2E is not feasible and ensure unit tests cover the logic.

## Unit Tests (unit/)

### Philosophy: Fast, Simple, Avoid Mocking

**Priority**: Simplicity and speed. **Minimize mocking** - only mock when absolutely necessary.

### Characteristics

- Test single functions or classes in isolation
- **Avoid mocks when possible** - use real objects/data
- Mock only when external dependencies are unavoidable (APIs, databases)
- Fast execution (milliseconds to seconds)
- Simple setup and teardown
- Focus on logic, not integration

### Simple Unit Test Example (No Mocking)

```python
# src/template_api/tests/unit/test_services.py
from template_api.services.data_validator import validate_coordinates

def test_validate_coordinates_valid():
    """Simple unit test - pure function, no mocking needed"""
    assert validate_coordinates(45.0, -122.0) is True

def test_validate_coordinates_invalid_latitude():
    assert validate_coordinates(91.0, -122.0) is False

def test_validate_coordinates_invalid_longitude():
    assert validate_coordinates(45.0, 181.0) is False
```

### Unit Test with Real Data (Preferred)

```python
# src/template_lib/tests/unit/test_preprocessing.py
import xarray as xr
import numpy as np
from template_lib.services.preprocessing import normalize_temperature

def test_normalize_temperature():
    """Use real xarray objects - no mocking needed"""
    # Create real test data
    data = xr.DataArray(
        [10.0, 20.0, 30.0],
        coords={'time': [0, 1, 2]},
        dims=['time']
    )
    
    result = normalize_temperature(data)
    
    # Verify with real assertions
    assert result.mean().item() == pytest.approx(0.0)
    assert result.std().item() == pytest.approx(1.0)
```

### Unit Test with Minimal Mocking (Only When Necessary)

```python
# src/template_api/tests/unit/test_routers.py
from unittest.mock import patch
from fastapi.testclient import TestClient
from template_api.main import app

def test_fetch_external_data_endpoint():
    """Mock ONLY unavoidable external API call"""
    client = TestClient(app)
    
    # Mock only the external HTTP call - everything else is real
    with patch('template_api.services.data_service.fetch_from_external_api') as mock_fetch:
        mock_fetch.return_value = {"temperature": 25.0}
        
        response = client.get("/v1/public/data/123")
        
        assert response.status_code == 200
        assert response.json()["temperature"] == 25.0
```

### Prefer Dependency Injection Over Mocking

```python
# ✅ GOOD: Design for testability without mocks
class DataProcessor:
    def __init__(self, data_source):
        self.data_source = data_source
    
    def process(self):
        data = self.data_source.fetch()
        return self.transform(data)

# Test with real test implementation
class TestDataSource:
    def fetch(self):
        return [1, 2, 3]

def test_data_processor():
    """No mocking - use real test implementation"""
    processor = DataProcessor(TestDataSource())
    result = processor.process()
    assert len(result) > 0

# ❌ BAD: Mock when you could use dependency injection
def test_data_processor_with_mock():
    with patch('module.DataSource') as mock:
        mock.fetch.return_value = [1, 2, 3]
        processor = DataProcessor(mock)
        ...
```

### When Mocking is Acceptable

Mock **only** when you cannot avoid external dependencies:

- External HTTP APIs (weather services, geocoding, etc.)
- Database connections (if not using in-memory DB)
- File system operations that require specific environments
- Time-dependent behavior (use `freezegun` or similar)

### Keep Any Mocking Simple

```python
# ✅ GOOD: Simple, one-level mock when necessary
def test_fetch_weather_data():
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.json.return_value = {"temp": 20}
        result = fetch_weather("location")
        assert result["temp"] == 20

# ❌ BAD: Complex mock hierarchy - refactor code instead
def test_complex():
    with patch('module.ClassA') as mock_a:
        with patch('module.ClassB') as mock_b:
            mock_a.return_value.method1.return_value.method2.return_value = ...
            # Too complex - refactor code or write E2E test
```

## Running Tests

```bash
# All tests
pytest .

# Only E2E tests
pytest src/template_api/tests/e2e/ -v
pytest src/template_lib/tests/e2e/ -v

# Only unit tests (fast)
pytest src/template_api/tests/unit/ -v
pytest src/template_lib/tests/unit/ -v

# Skip slow E2E tests during development
pytest -m "not slow"

# Run only slow tests (CI/nightly builds)
pytest -m "slow"
```

## Test Markers

Use pytest markers to categorize tests:

```python
import pytest

@pytest.mark.e2e
def test_full_workflow():
    """End-to-end test - no mocking, may be fast"""
    ...

@pytest.mark.e2e
@pytest.mark.slow
def test_heavy_processing():
    """Long-running E2E test - several minutes"""
    ...

@pytest.mark.unit
def test_single_function():
    """Unit test - fast, minimal/no mocking"""
    ...
```

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "e2e: End-to-end tests (no mocking)",
    "unit: Unit tests (fast, minimal mocking)",
    "slow: Tests that take >1 minute"
]
```

## Test Fixtures

### Simple Fixtures for Unit Tests

```python
# conftest.py
import pytest
import xarray as xr
import numpy as np

@pytest.fixture
def sample_dataset():
    """Real xarray dataset for unit tests"""
    return xr.Dataset({
        'temperature': (['time', 'lat', 'lon'], 
                       np.random.rand(10, 5, 5))
    })

@pytest.fixture
def sample_config():
    """Real config dict - no mocking"""
    return {
        "api_key": "test_key",
        "timeout": 10,
        "retry_attempts": 3
    }
```

### Real Fixtures for E2E Tests

```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Real test data directory"""
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def temp_output_dir(tmp_path):
    """Real temporary directory for outputs"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
```

## Coverage Guidelines

- **Target**: 80% overall coverage
- **Unit tests**: Should cover most logic (85%+)
- **E2E tests**: Focus on critical paths, not coverage percentage
- **Don't test**: External libraries, framework code, trivial getters/setters

```bash
# Generate coverage report
coverage run
coverage report --skip-covered  # Show only <100% files
coverage html                   # Visual report
```

## Best Practices

### DO

- ✅ Write descriptive test names: `test_validate_coordinates_rejects_invalid_latitude`
- ✅ Use real data/objects in unit tests when possible
- ✅ One assertion concept per test
- ✅ Use AAA pattern: Arrange, Act, Assert
- ✅ Clean up resources in E2E tests
- ✅ Keep unit tests fast (<1 second each)
- ✅ Minimize number of slow E2E tests - focus on critical paths
- ✅ Mark slow tests with `@pytest.mark.slow`

### DON'T

- ❌ Mock in E2E tests (defeats the purpose)
- ❌ Mock when you can use real test data
- ❌ Create complex mock hierarchies (refactor code instead)
- ❌ Test implementation details (test behavior)
- ❌ Share state between tests
- ❌ Write many slow E2E tests - keep them minimal
- ❌ Commit commented-out tests (delete or fix)

## Example Test File Structure

```python
# src/template_api/tests/unit/test_data_service.py
import pytest
from template_api.services.data_service import DataService

class TestDataService:
    """Group related tests"""
    
    def test_process_data_success(self):
        """Happy path - no mocking, use real data"""
        service = DataService()
        test_data = [1, 2, 3, 4, 5]
        result = service.process(test_data)
        assert len(result) == 5
        assert all(x > 0 for x in result)
    
    def test_process_empty_data(self):
        """Edge case - no mocking needed"""
        service = DataService()
        result = service.process([])
        assert result == []
    
    def test_process_with_invalid_data(self):
        """Error case - no mocking"""
        service = DataService()
        with pytest.raises(ValueError, match="Invalid data"):
            service.process(None)
```

## Decision Tree: E2E vs Unit Test?

```json
Can this be tested without mocking?
│
├─ YES → Does it test a complete workflow?
│        │
│        ├─ YES → Write E2E test
│        │        (May take minutes - that's OK)
│        │
│        └─ NO → Write unit test
│                (Should be fast)
│
└─ NO → Is the mock absolutely necessary?
         (External API, database, etc.)
         │
         ├─ YES → Can you refactor to avoid it?
         │        │
         │        ├─ NO → Write simple unit test with minimal mock
         │        │
         │        └─ YES → Refactor and write test without mock
         │
         └─ NO → Write unit test without mocking
```

## Time Guidelines

### Unit Tests

- **Target**: <1 second per test
- **Maximum**: Few seconds for data-intensive operations
- Run frequently during development

### E2E Tests

- **No strict time limit** - verify critical functionality thoroughly
- **Can take minutes** for computationally intensive processes
- **Keep minimal** - only essential workflows (3-5 critical E2E tests per module)
- Mark with `@pytest.mark.slow` if >1 minute
- Run in CI/CD or before major releases

Remember: **Real tests over mocks, critical coverage over 100% coverage**.
