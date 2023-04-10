from typing import NamedTuple, Union

from pydantic import Field
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
        title='Coordinate longitude',
        ge=-180,
        le=180,
    ),
]

LatField = Annotated[
    Union[float, int],
    Field(
        title='Coordinate latitude',
        ge=-90,
        le=90,
    ),
]

PointFieldType = Field(
    POINT,
    const=True,
    title='Point',
)

MultiPointFieldType = Field(
    MULTI_POINT,
    const=True,
    title='Multi Point',
)

LineStringFieldType = Field(
    LINE_STRING,
    const=True,
    title='LineS String',
)

MultiLineStringFieldType = Field(
    MULTI_LINE_STRING,
    const=True,
    title='Multi Line String',
)

PolygonFieldType = Field(
    POLYGON,
    const=True,
    title='Polygon',
)

MultiPolygonFieldType = Field(
    MULTI_POLYGON,
    const=True,
    title='Multi Polygon',
)

GeometryCollectionFieldType = Field(
    GEOMETRY_COLLECTION,
    const=True,
    title='Geometry Collection',
)

FeatureFieldType = Field(
    FEATURE,
    const=True,
    title='Feature',
)

FeatureCollectionFieldType = Field(
    FEATURE_COLLECTION,
    const=True,
    title='Feature Collection',
)


class Coordinates(NamedTuple):
    lon: LonField
    lat: LatField
