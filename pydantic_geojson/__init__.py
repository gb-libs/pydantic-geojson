"""Pydantic GeoJSON - A Pydantic-based library for GeoJSON validation.

This package provides Pydantic models for validating and working with GeoJSON
data according to RFC 7946 specification. It includes models for all GeoJSON
geometry types, Feature objects, and FeatureCollection objects.

Example:
    Basic usage of Point geometry:

    ```python
    from pydantic_geojson import PointModel

    point = PointModel(
        type="Point",
        coordinates=[-105.01621, 39.57422]
    )
    ```
"""

from .feature import FeatureModel
from .feature_collection import FeatureCollectionModel
from .geometry_collection import GeometryCollectionModel
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .object_type import GeometryType
from .point import PointModel
from .polygon import PolygonModel

__version__ = "0.3.0"
__author__ = "Aliaksandr Vaskevich"
__maintainer__ = __author__

__email__ = "vaskevic.an@gmail.com"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    # object type
    "GeometryType",
    # models
    "PointModel",
    "MultiPointModel",
    "LineStringModel",
    "MultiLineStringModel",
    "PolygonModel",
    "MultiPolygonModel",
    "GeometryCollectionModel",
    "FeatureModel",
    "FeatureCollectionModel",
]
