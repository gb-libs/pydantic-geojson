from __future__ import annotations

from typing import List, Union

from ._base import GeoJSONModel, GeometryCollectionFieldType
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class GeometryCollectionModel(GeoJSONModel):
    type: GeometryCollectionFieldType
    geometries: List[Union[
        PointModel,
        MultiPointModel,
        LineStringModel,
        MultiLineStringModel,
        PolygonModel,
        MultiPolygonModel,
        GeometryCollectionModel
    ]]

GeometryCollectionModel.model_rebuild() # Required for recursion 
