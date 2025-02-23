from typing import List, Literal, NamedTuple, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .object_type import (
    FEATURE,
    FEATURE_COLLECTION,
    GEOMETRY_COLLECTION,
    LINE_STRING,
    MULTI_LINE_STRING,
    MULTI_POINT,
    MULTI_POLYGON,
    POINT,
    POLYGON,
)

LonField = Annotated[
    Union[float, int],
    Field(
        title="Coordinate longitude",
        ge=-180,
        le=180,
    ),
]

LatField = Annotated[
    Union[float, int],
    Field(
        title="Coordinate latitude",
        ge=-90,
        le=90,
    ),
]

PointFieldType = Field(
    POINT,
    title="Point",
)

MultiPointFieldType = Field(
    MULTI_POINT,
    title="Multi Point",
)

LineStringFieldType = Field(
    LINE_STRING,
    title="LineS String",
)

MultiLineStringFieldType = Field(
    MULTI_LINE_STRING,
    title="Multi Line String",
)

PolygonFieldType = Field(
    POLYGON,
    title="Polygon",
)

MultiPolygonFieldType = Field(
    MULTI_POLYGON,
    title="Multi Polygon",
)

GeometryCollectionFieldType = Field(
    GEOMETRY_COLLECTION,
    title="Geometry Collection",
)

FeatureFieldType = Field(
    FEATURE,
    title="Feature",
)

FeatureCollectionFieldType = Field(
    FEATURE_COLLECTION,
    title="Feature Collection",
)


class Coordinates(NamedTuple):
    lon: LonField
    lat: LatField


BoundingBox = Annotated[
    Optional[List[float]],
    Field(
        default=None,
        title="Bounding Box",
        description="Coordinate range for a GeoJSON Object",
        min_length=2,  # 1D
        max_length=6,  # 3D
    ),
]


class GeoJSONModel(BaseModel):
    bbox: BoundingBox
