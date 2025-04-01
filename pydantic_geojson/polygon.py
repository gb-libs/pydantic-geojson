from typing import List

from ._base import GeoJSONModel, LinearRing, PolygonFieldType


class PolygonModel(GeoJSONModel):
    type: PolygonFieldType
    coordinates: List[LinearRing]
