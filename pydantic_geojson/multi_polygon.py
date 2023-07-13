from typing import List

from pydantic import BaseModel

from ._base import Coordinates, MultiPolygonFieldType


class MultiPolygonModel(BaseModel):
    type: str = MultiPolygonFieldType
    coordinates: List[List[List[Coordinates]]]
