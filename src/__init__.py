"""API to provide online simulation service of TESEO numerical model."""

from src.__version__ import __api_name__, __description__, __version__

__all__ = ["__api_name__", "__description__", "__version__"]


if __name__ == "__main__":
    print(f"\n____ {__api_name__} v{__version__} ____\n")
