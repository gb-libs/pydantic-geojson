from typing import List

from pydantic import BaseModel

from ._base import Coordinates, GeoJSONModel, MultiPolygonFieldType


class MultiPolygonModel(GeoJSONModel):
    type: str = MultiPolygonFieldType
    coordinates: List[List[List[Coordinates]]]
