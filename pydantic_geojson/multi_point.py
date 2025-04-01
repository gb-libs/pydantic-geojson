from typing import List

from ._base import Coordinates, GeoJSONModel, MultiPointFieldType


class MultiPointModel(GeoJSONModel):
    type: MultiPointFieldType
    coordinates: List[Coordinates]
