from typing import List

from pydantic import BaseModel

from ._base import Coordinates, GeoJSONModel, MultiPointFieldType


class MultiPointModel(GeoJSONModel):
    type: str = MultiPointFieldType
    coordinates: List[Coordinates]
