import math
from typing import List, Literal, NamedTuple, Optional, Union

from pydantic import AfterValidator, BaseModel, ConfigDict, Field
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

AltField = Annotated[
    Union[float, int],
    Field(
        title="Coordinate altitude",
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
    alt: Optional[AltField] = None

    def __eq__(self, other):
        # Note that +180 and -180 are not considered equal latitude here
        lon_equal = math.isclose(self.lon, other.lon)
        lat_equal = math.isclose(self.lat, other.lat)
        alt_equal = (
            self.alt is None
            and other.alt is None
            or (
                self.alt is not None
                and other.alt is not None
                and math.isclose(self.alt, other.alt)
            )
        )
        return lon_equal and lat_equal and alt_equal


def check_linear_ring(linear_ring: List[Coordinates]) -> List[Coordinates]:
    if (length := len(linear_ring)) < 4:
        raise ValueError(f"Linear Ring length must be >=4, not {length}")

    if (start := linear_ring[0]) != (end := linear_ring[-1]):
        raise ValueError(
            "Linear Rings must start and end at the same coordinate. "
            f"Start {start}, End {end}."
        )

    return linear_ring


LinearRing = Annotated[List[Coordinates], AfterValidator(check_linear_ring)]


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
