from typing import List

from pydantic import BaseModel

from ._base import Coordinates, LineStringFieldType


class LineStringModel(BaseModel):
    type: str = LineStringFieldType
    coordinates: List[Coordinates]
