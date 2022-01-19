from pydantic import BaseModel

from ._base import Coordinates, PointFieldType


class PointModel(BaseModel):
    type: str = PointFieldType
    coordinates: Coordinates
