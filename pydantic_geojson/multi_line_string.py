from typing import List

from pydantic import BaseModel

from ._base import Coordinates, GeoJSONModel, MultiLineStringFieldType


class MultiLineStringModel(GeoJSONModel):
    type: str = MultiLineStringFieldType
    coordinates: List[List[Coordinates]]
