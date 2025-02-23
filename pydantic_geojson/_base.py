from typing import List, Literal, NamedTuple, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
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

PointFieldType = Annotated[Literal[POINT], Field(POINT, title="Point")]  # type: ignore

MultiPointFieldType = Annotated[
    Literal[MULTI_POINT],  # type: ignore
    Field(
        MULTI_POINT,
        title="Multi Point",
    ),
]

LineStringFieldType = Annotated[
    Literal[LINE_STRING],  # type: ignore
    Field(
        LINE_STRING,
        title="Line String",
    ),
]

MultiLineStringFieldType = Annotated[
    Literal[MULTI_LINE_STRING],  # type: ignore
    Field(
        MULTI_LINE_STRING,
        title="Multi Line String",
    ),
]

PolygonFieldType = Annotated[
    Literal[POLYGON],  # type: ignore
    Field(
        POLYGON,
        title="Polygon",
    ),
]

MultiPolygonFieldType = Annotated[
    Literal[MULTI_POLYGON],  # type: ignore
    Field(
        MULTI_POLYGON,
        title="Multi Polygon",
    ),
]

GeometryCollectionFieldType = Annotated[
    Literal[GEOMETRY_COLLECTION],  # type: ignore
    Field(
        GEOMETRY_COLLECTION,
        title="Geometry Collection",
    ),
]

FeatureFieldType = Annotated[
    Literal[FEATURE],  # type: ignore
    Field(
        FEATURE,
        title="Feature",
    ),
]

FeatureCollectionFieldType = Annotated[
    Literal[FEATURE_COLLECTION,],  # type: ignore
    Field(
        FEATURE_COLLECTION,
        title="Feature Collection",
    ),
]


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
    """Base class for GeoJSON models."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Union[
        PointFieldType,
        MultiPointFieldType,
        PolygonFieldType,
        MultiPolygonFieldType,
        LineStringFieldType,
        MultiLineStringFieldType,
        GeometryCollectionFieldType,
        FeatureFieldType,
        FeatureCollectionFieldType,
    ]
    bbox: BoundingBox
