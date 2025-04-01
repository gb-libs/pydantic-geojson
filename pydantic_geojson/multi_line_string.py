from typing import List

from ._base import Coordinates, GeoJSONModel, MultiLineStringFieldType


class MultiLineStringModel(GeoJSONModel):
    type: MultiLineStringFieldType
    coordinates: List[List[Coordinates]]
