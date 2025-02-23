from typing import List

from ._base import GeoJSONModel, LinearRing, MultiPolygonFieldType


class MultiPolygonModel(GeoJSONModel):
    type: MultiPolygonFieldType
    coordinates: List[List[LinearRing]]
