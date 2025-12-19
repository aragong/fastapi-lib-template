---
applyTo: '**/routers/**/*.py'
---

# API Design Guidelines

## Core Principles

- **Simplicity First**: Prefer simple, intuitive endpoints over complex abstractions
- **Consistency**: Follow the same patterns across all endpoints
- **RESTful when possible**: Use standard HTTP methods and status codes
- **Self-documenting**: Clear names and automatic OpenAPI/Swagger documentation

## URL Structure

### Naming Conventions

```python
# ✅ GOOD: Clear, noun-based, lowercase
GET  /v1/public/datasets
GET  /v1/public/datasets/{dataset_id}
POST /v1/public/datasets
PUT  /v1/public/datasets/{dataset_id}
DELETE /v1/public/datasets/{dataset_id}

# ❌ BAD: Verbs, unclear, camelCase
GET  /v1/public/getDatasets
POST /v1/public/createNewDataset
GET  /v1/public/datasetById/{id}
```

### Router Organization

```python
from template_api.config.env import env
from fastapi import APIRouter

# Group related endpoints by resource
router = APIRouter(
    tags=["Datasets"],  # Appears in Swagger UI
    prefix=env.API_PREFIX + "/datasets"
)

@router.get("/")
async def list_datasets():
    """List all datasets"""
    ...

@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str):
    """Get specific dataset"""
    ...
```

### Path Parameters vs Query Parameters

```python
# ✅ GOOD: ID in path, filters in query
@router.get("/datasets/{dataset_id}")
async def get_dataset(
    dataset_id: str,
    include_metadata: bool = False
):
    ...

# ✅ GOOD: Query params for filtering lists
@router.get("/datasets")
async def list_datasets(
    region: str | None = None,
    start_date: str | None = None,
    limit: int = 100
):
    ...

# ❌ BAD: Everything in path
@router.get("/datasets/{region}/{start_date}/{limit}")
```

## HTTP Methods

Use standard HTTP methods for their intended purpose:

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Retrieve data (safe, idempotent) | Get dataset, list items |
| **POST** | Create new resource | Upload file, create dataset |
| **PUT** | Replace entire resource | Update entire dataset |
| **PATCH** | Partial update | Update specific fields |
| **DELETE** | Remove resource | Delete dataset |

```python
# ✅ GOOD: Correct method usage
@router.get("/datasets/{id}")  # Read
@router.post("/datasets")      # Create
@router.put("/datasets/{id}")  # Full update
@router.patch("/datasets/{id}") # Partial update
@router.delete("/datasets/{id}") # Delete

# ❌ BAD: Wrong methods
@router.post("/datasets/get")   # Should be GET
@router.get("/datasets/delete/{id}")  # Should be DELETE
```

## Request/Response Models

### Use Pydantic Models

```python
from pydantic import BaseModel, Field

# ✅ GOOD: Clear input/output models
class DatasetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    region: str
    
class DatasetResponse(BaseModel):
    id: str
    name: str
    description: str | None
    region: str
    created_at: datetime
    status: str

@router.post("/datasets", response_model=DatasetResponse)
async def create_dataset(dataset: DatasetCreate):
    ...
    return DatasetResponse(...)

# ❌ BAD: Dict responses without validation
@router.post("/datasets")
async def create_dataset(name: str, region: str):
    return {"id": "123", "name": name}  # No validation
```

### Response Structure

Keep responses simple and consistent:

```python
# ✅ GOOD: Simple, direct response
@router.get("/datasets/{id}")
async def get_dataset(id: str) -> DatasetResponse:
    return DatasetResponse(...)

# ✅ GOOD: List response
@router.get("/datasets")
async def list_datasets() -> list[DatasetResponse]:
    return [DatasetResponse(...), ...]

# ❌ BAD: Unnecessary wrapper
@router.get("/datasets/{id}")
async def get_dataset(id: str):
    return {
        "status": "success",
        "data": dataset,
        "meta": {...}
    }
```

## Error Handling

### Always Include Detailed Error Information

**Critical**: Error responses must include specific details and context visible in Swagger.

```python
from fastapi import HTTPException, status
import traceback
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD: Detailed error with context
@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    dataset = find_dataset(dataset_id)
    
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with id '{dataset_id}' not found in the database"
        )
    
    return dataset

# ✅ GOOD: Include specific validation failures
@router.post("/datasets/process")
async def process_dataset(dataset_id: str, variables: list[str]):
    dataset = find_dataset(dataset_id)
    
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{dataset_id}' does not exist"
        )
    
    missing_vars = [v for v in variables if v not in dataset.variables]
    if missing_vars:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Variables {missing_vars} not found in dataset '{dataset_id}'. Available: {list(dataset.variables)}"
        )
    
    return process(dataset, variables)

# ❌ BAD: Generic error without context
@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    dataset = find_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Not found")  # No context!
    return dataset
```

### Catch and Log Exceptions with Traceback

```python
# ✅ GOOD: Catch exceptions, log traceback, return detailed error
@router.post("/datasets/analyze")
async def analyze_dataset(dataset_id: str, config: AnalysisConfig):
    try:
        dataset = load_dataset(dataset_id)
        result = perform_analysis(dataset, config)
        return result
        
    except FileNotFoundError as e:
        logger.error(f"Dataset file not found: {dataset_id}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset file for '{dataset_id}' not found: {str(e)}"
        )
    
    except ValueError as e:
        logger.error(f"Invalid configuration for dataset {dataset_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid analysis configuration: {str(e)}"
        )
    
    except Exception as e:
        # Log full traceback for unexpected errors
        logger.exception(f"Unexpected error analyzing dataset {dataset_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze dataset '{dataset_id}': {type(e).__name__}: {str(e)}"
        )
```

### Development vs Production Error Details

```python
from template_api.config.env import env

@router.post("/datasets/process")
async def process_dataset(dataset_id: str):
    try:
        result = complex_processing(dataset_id)
        return result
        
    except Exception as e:
        logger.exception(f"Processing failed for dataset {dataset_id}")
        
        # Include more details in development
        if env.APP_ENVIRONMENT == "local":
            detail = f"Processing error for '{dataset_id}': {type(e).__name__}: {str(e)}\nTraceback: {traceback.format_exc()}"
        else:
            detail = f"Processing failed for dataset '{dataset_id}': {str(e)}"
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
```

### Standard HTTP Status Codes

| Code | Usage | Detail Example |
|------|-------|----------------|
| **200** | Success | - |
| **201** | Created | `"Dataset 'temp_2024' created with id 'ds_123'"` |
| **204** | No Content | - |
| **400** | Bad Request | `"Invalid date format '2024-13-01': month must be 1-12"` |
| **401** | Unauthorized | `"Authentication token missing or expired"` |
| **403** | Forbidden | `"User 'john@example.com' lacks permission to delete dataset 'ds_123'"` |
| **404** | Not Found | `"Dataset with id 'ds_999' not found in database"` |
| **422** | Unprocessable Entity | `"Variable 'humidity' not found. Available: ['temp', 'pressure']"` |
| **500** | Internal Error | `"Failed to process dataset 'ds_123': IOError: disk full"` |

### Error Response Examples in Swagger

Errors appear automatically in Swagger with your detail messages:

```python
@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str) -> DatasetResponse:
    """
    Retrieve a specific dataset by ID.
    
    Returns the dataset information including name, region, and status.
    
    Raises:
        404: Dataset not found
        500: Server error during retrieval
    """
    try:
        dataset = find_dataset(dataset_id)
        if dataset is None:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_id}' not found"
            )
        return dataset
    except Exception as e:
        logger.exception(f"Error retrieving dataset {dataset_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve dataset '{dataset_id}': {str(e)}"
        )
```

This will show in Swagger UI with example responses:

- **200**: `{dataset object}`
- **404**: `{"detail": "Dataset 'ds_999' not found"}`
- **500**: `{"detail": "Failed to retrieve dataset 'ds_123': Connection timeout"}`

## Documentation (Swagger UI)

### Swagger is the Standard

**All API documentation uses Swagger UI** (OpenAPI), automatically generated by FastAPI.

Access at: `http://localhost:8000/docs`

### Endpoint Docstrings

Write clear docstrings - they appear directly in Swagger:

```python
@router.get("/datasets/{dataset_id}")
async def get_dataset(
    dataset_id: str,
    include_metadata: bool = False
) -> DatasetResponse:
    """
    Retrieve a specific dataset by ID.
    
    Returns the dataset information including name, region, and processing status.
    Optionally includes additional metadata if requested.
    
    **Parameters:**
    - **dataset_id**: Unique identifier for the dataset (e.g., 'ds_123abc')
    - **include_metadata**: Include technical metadata (default: false)
    
    **Returns:**
    - Dataset information with current status
    
    **Errors:**
    - **404**: Dataset with given ID not found
    - **500**: Internal server error during retrieval
    """
    ...
```

### Model Examples for Swagger

Add examples to Pydantic models for better Swagger documentation:

```python
from pydantic import BaseModel, Field

class DatasetCreate(BaseModel):
    name: str = Field(..., description="Dataset name", min_length=1, max_length=100)
    description: str | None = Field(None, description="Optional description")
    region: str = Field(..., description="Geographic region code")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Temperature Data Europe 2024",
                    "description": "Daily temperature measurements",
                    "region": "europe"
                }
            ]
        }
    }

class DatasetResponse(BaseModel):
    id: str = Field(..., description="Unique dataset identifier")
    name: str = Field(..., description="Dataset name")
    region: str = Field(..., description="Geographic region")
    status: str = Field(..., description="Processing status: pending, ready, error")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "ds_123abc",
                    "name": "Temperature Data Europe 2024",
                    "region": "europe",
                    "status": "ready",
                    "created_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
    }
```

### Response Model Documentation

Specify response models for automatic Swagger schemas:

```python
# ✅ GOOD: Documented response model
@router.get("/datasets/{id}", response_model=DatasetResponse)
async def get_dataset(id: str) -> DatasetResponse:
    ...

# ✅ GOOD: List response
@router.get("/datasets", response_model=list[DatasetResponse])
async def list_datasets() -> list[DatasetResponse]:
    ...

# ❌ BAD: No response model (Swagger shows generic response)
@router.get("/datasets/{id}")
async def get_dataset(id: str):
    return {"id": id, "name": "..."}  # No schema in Swagger
```

### Tags for Organization

Group endpoints with tags (visible in Swagger sidebar):

```python
# Datasets section in Swagger
datasets_router = APIRouter(
    tags=["Datasets"],
    prefix=env.API_PREFIX + "/datasets"
)

# Processing section in Swagger
processing_router = APIRouter(
    tags=["Processing"],
    prefix=env.API_PREFIX + "/processing"
)
```

### Deprecation Warnings

Mark deprecated endpoints in Swagger:

```python
@router.get("/datasets/old-endpoint", deprecated=True)
async def old_endpoint():
    """
    **DEPRECATED**: Use `/datasets/new-endpoint` instead.
    
    This endpoint will be removed in v2.0.
    """
    ...
```

## Pagination

For list endpoints that could return many items:

```python
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: list[DatasetResponse]
    total: int
    page: int
    page_size: int
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [...],
                    "total": 150,
                    "page": 2,
                    "page_size": 50
                }
            ]
        }
    }

@router.get("/datasets")
async def list_datasets(
    page: int = 1,
    page_size: int = 100
) -> PaginatedResponse:
    """
    List datasets with pagination.
    
    **Parameters:**
    - **page**: Page number (starts at 1)
    - **page_size**: Items per page (max 1000)
    
    **Returns:**
    - Paginated list of datasets with total count
    """
    offset = (page - 1) * page_size
    items = query_datasets(limit=page_size, offset=offset)
    total = count_datasets()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )
```

## File Uploads

Keep file handling simple and clear:

```python
from fastapi import UploadFile, File, Form

@router.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(..., description="Dataset file (.nc or .tif)"),
    name: str = Form(..., description="Dataset name"),
    region: str = Form(..., description="Region code")
):
    """
    Upload a dataset file.
    
    **Accepted formats:** .nc (NetCDF), .tif (GeoTIFF)
    
    **Parameters:**
    - **file**: Dataset file to upload
    - **name**: Descriptive name for the dataset
    - **region**: Geographic region identifier
    
    **Errors:**
    - **400**: Invalid file format (only .nc and .tif accepted)
    - **413**: File too large (max 500MB)
    - **500**: Upload processing failed
    """
    # Validate file type
    if not file.filename.endswith(('.nc', '.tif')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format '{file.filename}'. Only .nc and .tif files are supported"
        )
    
    try:
        content = await file.read()
        dataset_id = save_dataset(content, name, region)
        return {"id": dataset_id, "filename": file.filename, "size_bytes": len(content)}
        
    except Exception as e:
        logger.exception(f"Failed to upload file {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed for '{file.filename}': {str(e)}"
        )
```

## Query Filtering

Keep filtering simple and intuitive:

```python
@router.get("/datasets")
async def list_datasets(
    region: str | None = None,
    status: str | None = None,
    created_after: datetime | None = None
) -> list[DatasetResponse]:
    """
    List datasets with optional filters.
    
    All filters are optional and can be combined.
    
    **Parameters:**
    - **region**: Filter by region code (e.g., 'europe', 'asia')
    - **status**: Filter by status ('pending', 'ready', 'error')
    - **created_after**: Only datasets created after this timestamp
    """
    query = build_query()
    
    if region:
        query = query.filter(region=region)
    if status:
        query = query.filter(status=status)
    if created_after:
        query = query.filter(created_at__gte=created_after)
    
    return query.all()
```

## Versioning

Version is handled via `API_PREFIX` in environment:

```python
# In env.py
API_PREFIX = os.getenv("API_PREFIX", "/v1/public")

# In routers
router = APIRouter(prefix=env.API_PREFIX + "/datasets")

# Results in: /v1/public/datasets
```

## Async/Await

Use async for all endpoints:

```python
# ✅ GOOD: Async endpoints
@router.get("/datasets/{id}")
async def get_dataset(id: str):
    dataset = await fetch_dataset(id)  # Async I/O
    return dataset

# ❌ BAD: Sync endpoints (unless necessary)
@router.get("/datasets/{id}")
def get_dataset(id: str):  # Missing async
    ...
```

## Health Check Endpoint

Always include a health check:

```python
@router.get("/healthcheck")
async def healthcheck():
    """
    Service health check.
    
    Returns 200 if the service is operational.
    """
    return {"status": "ok", "service": "template-api"}
```

## Checklist for New Endpoints

Before adding a new endpoint, verify:

- [ ] Uses appropriate HTTP method
- [ ] Has clear, noun-based URL
- [ ] Uses Pydantic models for request/response
- [ ] Includes detailed docstring for Swagger
- [ ] Returns appropriate status codes
- [ ] Handles errors with detailed `HTTPException` messages
- [ ] Logs errors with traceback (`logger.exception()`)
- [ ] Includes specific context in error details (IDs, values, etc.)
- [ ] Has response_model specified
- [ ] Follows existing patterns in codebase
- [ ] Has at least one test (unit or e2e)
- [ ] Uses `env.API_PREFIX` for routing
- [ ] Is async

## Summary

**Keep it simple**:

- Clear, predictable URLs
- Standard HTTP methods and status codes
- **Detailed error messages with context** (IDs, values, what failed)
- **Log exceptions with tracebacks** for debugging
- Pydantic for validation with examples
- **Swagger UI for all documentation**
- Consistent patterns across endpoints

**When in doubt**: Look at existing endpoints in [src/template_api/routers/](../../src/template_api/routers/) and check the Swagger UI at `/docs`.
