from typing import List

from pydantic import BaseModel

from ._base import Coordinates, PolygonFieldType


class PolygonModel(BaseModel):
    type: str = PolygonFieldType
    coordinates: List[
        List[Coordinates]
    ]
