from typing import List, Union

from pydantic import BaseModel

from ._base import GeometryCollectionFieldType
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class GeometryCollectionModel(BaseModel):
    type: str = GeometryCollectionFieldType
    geometries: List[
        Union[
            PointModel,
            MultiPointModel,
            LineStringModel,
            MultiLineStringModel,
            PolygonModel,
            MultiPolygonModel,
        ],
    ]
