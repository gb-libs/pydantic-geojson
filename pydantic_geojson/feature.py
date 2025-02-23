from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from ._base import FeatureFieldType, GeoJSONModel
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class FeatureModel(GeoJSONModel):
    type: FeatureFieldType
    properties: Optional[Dict[str, Any]]
    geometry: Optional[
        Union[
            PointModel,
            MultiPointModel,
            LineStringModel,
            MultiLineStringModel,
            PolygonModel,
            MultiPolygonModel,
        ]
    ]
    id: Optional[Union[int, str]] = Field(
        default=None,
    )
