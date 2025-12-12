"""Version and metadata management."""

import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict


@lru_cache(maxsize=1)
def _load_project_metadata() -> Dict[str, Any]:
    """Load project metadata from pyproject.toml with caching."""
    # Find pyproject.toml relative to this file
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    pyproject_path = project_root / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")

    with pyproject_path.open("rb") as f:
        return tomllib.load(f)


def get_api_name() -> str:
    """Get the API name from project metadata."""
    metadata = _load_project_metadata()
    return metadata["project"]["name"]


def get_version() -> str:
    """Get the version from project metadata."""
    metadata = _load_project_metadata()
    return metadata["project"]["version"]


def get_description() -> str:
    """Get the description from project metadata."""
    metadata = _load_project_metadata()
    return metadata["project"]["description"]


# Lazy loading of constants
__api_name__ = get_api_name()
__version__ = get_version()
__description__ = get_description()
