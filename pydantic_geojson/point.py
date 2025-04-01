from ._base import Coordinates, GeoJSONModel, PointFieldType


class PointModel(GeoJSONModel):
    type: PointFieldType
    coordinates: Coordinates
