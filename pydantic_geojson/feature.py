from typing import Union

from pydantic import BaseModel

from ._base import FeatureFieldType
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class FeatureModel(BaseModel):
    type: str = FeatureFieldType
    geometry: Union[
        PointModel,
        MultiPointModel,
        LineStringModel,
        MultiLineStringModel,
        PolygonModel,
        MultiPolygonModel,
    ]
