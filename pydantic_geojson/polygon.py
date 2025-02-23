from typing import List

from pydantic import BaseModel

from ._base import Coordinates, GeoJSONModel, PolygonFieldType


class PolygonModel(GeoJSONModel):
    type: str = PolygonFieldType
    coordinates: List[List[Coordinates]]
