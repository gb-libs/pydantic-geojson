from typing import List

from pydantic import BaseModel

from ._base import Coordinates, MultiPointFieldType


class MultiPointModel(BaseModel):
    type: str = MultiPointFieldType
    coordinates: List[Coordinates]
