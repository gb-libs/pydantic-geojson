from typing import List

from pydantic import BaseModel

from ._base import Coordinates, GeoJSONModel, LineStringFieldType


class LineStringModel(GeoJSONModel):
    type: str = LineStringFieldType
    coordinates: List[Coordinates]
