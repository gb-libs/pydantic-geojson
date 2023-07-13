from typing import List

from pydantic import BaseModel

from ._base import Coordinates, MultiLineStringFieldType


class MultiLineStringModel(BaseModel):
    type: str = MultiLineStringFieldType
    coordinates: List[List[Coordinates]]
