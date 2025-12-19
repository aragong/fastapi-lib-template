---
applyTo: '**/*.py'
---

# Architecture & Stack Guidelines

## Technology Stack

### Core Framework

- **FastAPI** - Modern async web framework
  - Use async/await for all I/O operations
  - Leverage automatic API documentation (OpenAPI/Swagger)
  - Prefer dependency injection for shared resources
  - Use Pydantic models for request/response validation

### Data Processing Stack

- **xarray** - Multi-dimensional labeled arrays
  - Use for NetCDF, GRIB, and climate data
  - Leverage lazy loading with Dask for large datasets
  - Prefer DataArrays over raw numpy for metadata preservation
  - Use `.sel()`, `.isel()` for dimension-based indexing

- **GeoPandas** - Geospatial data operations
  - Use for vector data (shapefiles, GeoJSON)
  - Leverage spatial joins and geometric operations
  - Prefer `GeoDataFrame` over raw shapely objects
  - Use `.to_crs()` for coordinate system transformations

### Validation & Serialization

- **Pydantic** - Data validation using Python type hints
  - Define all API models with Pydantic BaseModel
  - Use Field() for validation constraints and metadata
  - Leverage validators for complex business rules
  - Prefer model_validator over field validators when checking multiple fields

### Key Dependencies

- **httpx** - Async HTTP client (prefer over requests)
- **numpy** - Numerical operations (via xarray/geopandas)
- **pandas** - Tabular data (via geopandas)
- **matplotlib** - Visualization and plotting
- **shapely** - Geometric operations (via geopandas)

## Architectural Principles

### 1. KISS (Keep It Simple, Stupid)

**Philosophy**: Simplicity over cleverness

```python
# ✅ GOOD: Simple and clear
def calculate_average(values: list[float]) -> float:
    return sum(values) / len(values)

# ❌ BAD: Unnecessary complexity
def calculate_average(values: list[float]) -> float:
    return reduce(lambda x, y: x + y, values) / len(values)
```

**Apply to**:

- Function design: One function, one purpose
- API endpoints: Clear, predictable URLs
- Data models: Flat structures when possible
- Avoid premature optimization

### 2. CLEAN CODE

**Philosophy**: Code is read more than written

#### Naming Conventions

```python
# ✅ GOOD: Descriptive names
def fetch_temperature_data(start_date: datetime, end_date: datetime) -> xr.DataArray:
    ...

# ❌ BAD: Cryptic abbreviations
def get_tmp_dat(sd: datetime, ed: datetime) -> xr.DataArray:
    ...
```

#### Function Length

- **Target**: 10-20 lines per function
- **Maximum**: 50 lines (if exceeded, refactor)
- **Extract**: Complex logic into separate functions

#### Comments

```python
# ✅ GOOD: Explain WHY, not WHAT
# Apply offset to align with local timezone (UTC+1)
adjusted_time = timestamp + timedelta(hours=1)

# ❌ BAD: Redundant comments
# Add 1 hour to timestamp
adjusted_time = timestamp + timedelta(hours=1)
```

#### Type Hints

Always use type hints for function signatures

##### Input Parameters: Be General (Accept Broad Types)

Use abstract types to maximize flexibility and reusability:

```python
from collections.abc import Sequence, Mapping, Iterable

# ✅ GOOD: Accepts list, tuple, range, etc.
def calculate_mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)

# ✅ GOOD: Accepts dict, OrderedDict, etc.
def process_config(config: Mapping[str, Any]) -> None:
    ...

# ✅ GOOD: Accepts any iterable
def filter_data(items: Iterable[int]) -> list[int]:
    return [x for x in items if x > 0]

# ❌ BAD: Too specific, rejects valid inputs
def calculate_mean(values: list[float]) -> float:  # Won't accept tuples!
    return sum(values) / len(values)
```

##### Return Types: Be Specific (Return Concrete Types)

Use concrete types to make the contract clear:

```python
# ✅ GOOD: Caller knows exactly what they get
def get_user_ids() -> list[int]:
    return [1, 2, 3]

def load_config() -> dict[str, str]:
    return {"key": "value"}

# ❌ BAD: Ambiguous return type
def get_user_ids() -> Sequence[int]:  # Is it list? tuple? range?
    return [1, 2, 3]
```

##### Complete Example

```python
from collections.abc import Sequence, Mapping
from pathlib import Path

# ✅ GOOD: General inputs, specific outputs
def process_dataset(
    data: xr.Dataset,                    # Specific library type
    variables: Sequence[str],             # General: accepts list, tuple
    config: Mapping[str, Any],           # General: accepts any dict-like
    output_format: str = "netcdf"
) -> Path:                               # Specific: always returns Path
    """
    Process dataset with given variables.
    
    Args:
        data: Input dataset
        variables: Variable names to process (list, tuple, etc.)
        config: Configuration mapping
        output_format: Output format
    
    Returns:
        Path to output file
    """
    ...
    return Path("output.nc")

# ❌ BAD: Too specific inputs, too general output
def process_dataset(
    data: xr.Dataset,
    variables: list[str],                 # Rejects tuples!
    config: dict[str, Any],              # Rejects OrderedDict!
    output_format: str = "netcdf"
) -> object:                             # What type is this?
    ...
```

##### Union Types for Flexibility

```python
from pathlib import Path

# ✅ GOOD: Accept multiple input types
def load_data(source: Path | str) -> xr.Dataset:
    path = Path(source) if isinstance(source, str) else source
    return xr.open_dataset(path)

# ✅ GOOD: Specific return type with optional
def find_user(user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
```

##### Summary: Input vs Output Types

| Aspect | Input Parameters | Return Types |
|--------|-----------------|--------------|
| **Guideline** | Be general/abstract | Be specific/concrete |
| **Why** | Accept more types | Clear contract |
| **Example** | `Sequence[T]` | `list[T]` |
| **Example** | `Mapping[K,V]` | `dict[K,V]` |
| **Example** | `Iterable[T]` | `list[T]` |
| **Benefit** | Reusable functions | Predictable behavior |

### 3. DRY (Don't Repeat Yourself)

**Philosophy**: Every piece of knowledge should have a single, authoritative representation

#### Extract Common Logic

```python
# ✅ GOOD: Reusable function
def validate_coordinates(lat: float, lon: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lon <= 180

def endpoint_a(lat: float, lon: float):
    if not validate_coordinates(lat, lon):
        raise ValueError("Invalid coordinates")
    ...

def endpoint_b(lat: float, lon: float):
    if not validate_coordinates(lat, lon):
        raise ValueError("Invalid coordinates")
    ...

# ❌ BAD: Duplicated validation
def endpoint_a(lat: float, lon: float):
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates")
    ...

def endpoint_b(lat: float, lon: float):
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates")
    ...
```

#### Use Pydantic Models for Validation

```python
# ✅ GOOD: Single source of truth
class CoordinateModel(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

@router.post("/process")
async def process(coords: CoordinateModel):
    # Validation happens automatically
    ...

# ❌ BAD: Manual validation in every endpoint
```

### 4. LEAN

**Philosophy**: Eliminate waste, maximize value

#### Avoid Over-Engineering

```python
# ✅ GOOD: Simple solution for current needs
def get_data_format(filename: str) -> str:
    if filename.endswith('.nc'):
        return 'netcdf'
    elif filename.endswith('.tif'):
        return 'geotiff'
    return 'unknown'

# ❌ BAD: Complex abstraction for simple problem
class FormatDetectorFactory:
    def create_detector(self, strategy: str) -> FormatDetector:
        ...
```

#### Build Incrementally

- Start with minimal viable feature
- Add complexity only when needed
- Refactor based on actual usage patterns
- Delete unused code immediately

#### Lazy Loading

```python
# ✅ GOOD: Load data only when needed
def process_large_dataset(file_path: Path) -> xr.Dataset:
    # xarray lazy loading - no data in memory yet
    ds = xr.open_dataset(file_path, chunks={'time': 100})
    # Computation happens only when needed
    result = ds.sel(time=slice('2020', '2021')).mean('time')
    return result.compute()  # Explicit computation

# ❌ BAD: Load everything upfront
def process_large_dataset(file_path: Path) -> xr.Dataset:
    ds = xr.open_dataset(file_path)  # Loads all data immediately
    return ds.sel(time=slice('2020', '2021')).mean('time')
```

## Code Organization Patterns

### Service Layer Pattern

```python
# src/template_lib/services/processing.py
def process_climate_data(dataset: xr.Dataset) -> xr.Dataset:
    """Pure business logic - no FastAPI dependencies"""
    return dataset.mean('time')

# src/template_api/routers/climate.py
@router.post("/process")
async def process_endpoint(file: UploadFile):
    """API layer - handles HTTP, delegates to service"""
    dataset = await load_dataset(file)
    result = process_climate_data(dataset)  # Calls library
    return {"status": "success"}
```

### Dependency Injection

```python
# ✅ GOOD: Testable and flexible
async def get_database_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.get("/data")
async def get_data(db: Session = Depends(get_database_session)):
    return db.query(Model).all()
```

### Error Handling

```python
# ✅ GOOD: Specific, informative errors
from fastapi import HTTPException, status

@router.get("/dataset/{dataset_id}")
async def get_dataset(dataset_id: str):
    try:
        dataset = load_dataset(dataset_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset {dataset_id} not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid dataset format: {str(e)}"
        )
    return dataset
```

## xarray Best Practices

### Use Coordinates and Attributes

```python
# ✅ GOOD: Self-documenting data
data = xr.DataArray(
    values,
    coords={
        'time': pd.date_range('2020-01-01', periods=365),
        'lat': np.arange(-90, 91),
        'lon': np.arange(-180, 180)
    },
    dims=['time', 'lat', 'lon'],
    attrs={
        'units': 'degrees_celsius',
        'long_name': 'Surface Temperature'
    }
)
```

### Chunking for Large Data

```python
# ✅ GOOD: Efficient memory usage
ds = xr.open_dataset('large_file.nc', chunks={'time': 100, 'lat': 50, 'lon': 50})
result = ds.mean('time').compute()  # Parallel computation with Dask
```

## GeoPandas Best Practices

### CRS Awareness

```python
# ✅ GOOD: Always check and transform CRS
gdf = gpd.read_file('data.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
```

### Spatial Joins

```python
# ✅ GOOD: Use built-in spatial operations
points_in_polygons = gpd.sjoin(points_gdf, polygons_gdf, predicate='within')
```

## When to Break Rules

These are guidelines, not laws. Break them when:

- **Performance**: Measured bottleneck requires optimization
- **External constraints**: Third-party API requires specific structure
- **Team agreement**: Documented exception with clear reasoning

Always document why you're deviating from these principles.
