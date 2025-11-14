import math
from typing import Annotated, Literal, NamedTuple, Optional, Union

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

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

PointFieldType = Annotated[Literal["Point"], Field(title="Point")]

MultiPointFieldType = Annotated[
    Literal["MultiPoint"],
    Field(title="Multi Point"),
]

LineStringFieldType = Annotated[
    Literal["LineString"],
    Field(title="Line String"),
]

MultiLineStringFieldType = Annotated[
    Literal["MultiLineString"],
    Field(title="Multi Line String"),
]

PolygonFieldType = Annotated[
    Literal["Polygon"],
    Field(title="Polygon"),
]

MultiPolygonFieldType = Annotated[
    Literal["MultiPolygon"],
    Field(title="Multi Polygon"),
]

GeometryCollectionFieldType = Annotated[
    Literal["GeometryCollection"],
    Field(title="Geometry Collection"),
]

FeatureFieldType = Annotated[
    Literal["Feature"],
    Field(title="Feature"),
]

FeatureCollectionFieldType = Annotated[
    Literal["FeatureCollection"],
    Field(title="Feature Collection"),
]


class Coordinates(NamedTuple):
    """Represents a geographic coordinate with longitude, latitude, and optional altitude.

    Coordinates are validated according to GeoJSON specification:
    - Longitude must be between -180 and 180 degrees
    - Latitude must be between -90 and 90 degrees
    - Altitude is optional and can be any numeric value

    Attributes:
        lon: Longitude in decimal degrees. Must be between -180 and 180.
        lat: Latitude in decimal degrees. Must be between -90 and 90.
        alt: Optional altitude/elevation value. Defaults to None.
    """

    lon: LonField
    lat: LatField
    alt: Optional[AltField] = None

    def __eq__(self, other):
        """Compare two Coordinates for equality using floating-point comparison.

        Uses math.isclose() for floating-point comparison to handle precision issues.
        Note that +180 and -180 are not considered equal longitude here.

        Args:
            other: Another Coordinates instance to compare with.

        Returns:
            True if coordinates are equal (within floating-point precision),
            False otherwise. Altitude is considered equal if both are None
            or both have the same value.
        """
        # Note that +180 and -180 are not considered equal latitude here
        lon_equal = math.isclose(self.lon, other.lon)
        lat_equal = math.isclose(self.lat, other.lat)
        alt_equal = (
            self.alt is None
            and other.alt is None
            or (
                self.alt is not None and other.alt is not None and math.isclose(self.alt, other.alt)
            )
        )
        return lon_equal and lat_equal and alt_equal


def check_linear_ring(linear_ring: list[Coordinates]) -> list[Coordinates]:
    """Validate that a linear ring meets GeoJSON requirements.

    A linear ring is a closed LineString with four or more positions. The first
    and last positions must be equivalent (they must contain identical values).

    Args:
        linear_ring: List of Coordinates representing the linear ring.

    Returns:
        The validated linear ring (same list).

    Raises:
        ValueError: If the linear ring has fewer than 4 coordinates.
        ValueError: If the first and last coordinates are not equal.
    """
    if (length := len(linear_ring)) < 4:
        raise ValueError(f"Linear Ring length must be >=4, not {length}")

    if (start := linear_ring[0]) != (end := linear_ring[-1]):
        raise ValueError(
            f"Linear Rings must start and end at the same coordinate. Start {start}, End {end}."
        )

    return linear_ring


LinearRing = Annotated[list[Coordinates], AfterValidator(check_linear_ring)]


def validate_bbox(bbox: Optional[list[float]]) -> Optional[list[float]]:
    """Validate bounding box according to RFC 7946 Section 5.

    A bounding box must be an array of length 2*n where n is the number of dimensions.
    For 2D: [west, south, east, north]
    For 3D: [west, south, depth, east, north, height]

    Args:
        bbox: Optional list of floats representing bounding box coordinates.

    Returns:
        The validated bbox (same list if valid).

    Raises:
        ValueError: If bbox doesn't meet RFC 7946 requirements.
    """
    if bbox is None:
        return None

    length = len(bbox)
    if length not in (2, 4, 6):
        raise ValueError(
            f"Bounding box must have 2, 4, or 6 elements (got {length}). "
            "According to RFC 7946, bbox length must be 2*n where n is the number of dimensions."
        )

    # Validate 2D bbox: [west, south, east, north]
    if length == 4:
        west, south, east, north = bbox

        # Validate longitude range
        if not (-180 <= west <= 180):
            raise ValueError(f"Bounding box west longitude must be in [-180, 180], got {west}")
        if not (-180 <= east <= 180):
            raise ValueError(f"Bounding box east longitude must be in [-180, 180], got {east}")

        # Validate latitude range
        if not (-90 <= south <= 90):
            raise ValueError(f"Bounding box south latitude must be in [-90, 90], got {south}")
        if not (-90 <= north <= 90):
            raise ValueError(f"Bounding box north latitude must be in [-90, 90], got {north}")

        # Validate latitude order (south <= north)
        # According to RFC 7946 Section 5.3, poles are special cases but still follow south <= north
        # For North Pole: bbox can be [-180.0, minlat, 180.0, 90.0] where north = 90.0
        # For South Pole: bbox can be [-180.0, -90.0, 180.0, maxlat] where south = -90.0
        if north < south:
            raise ValueError(
                f"Bounding box north latitude ({north}) must be >= south latitude ({south}). "
                "According to RFC 7946 Section 5.3, even pole cases follow this rule."
            )

        # Validate longitude order
        # According to RFC 7946 Section 5.2, antimeridian crossing is allowed (west > east)
        # But we should validate that it's a reasonable case
        if west > east:
            # Antimeridian crossing: check that it's reasonable
            # The span should be less than 360 degrees
            span = (180 - west) + (east - (-180))
            if span >= 360:
                raise ValueError(
                    f"Bounding box with antimeridian crossing: west ({west}) > east ({east}) "
                    "but span is >= 360 degrees, which is invalid."
                )

    # Validate 3D bbox: [west, south, depth, east, north, height]
    elif length == 6:
        west, south, depth, east, north, height = bbox

        # Validate longitude range
        if not (-180 <= west <= 180):
            raise ValueError(f"Bounding box west longitude must be in [-180, 180], got {west}")
        if not (-180 <= east <= 180):
            raise ValueError(f"Bounding box east longitude must be in [-180, 180], got {east}")

        # Validate latitude range
        if not (-90 <= south <= 90):
            raise ValueError(f"Bounding box south latitude must be in [-90, 90], got {south}")
        if not (-90 <= north <= 90):
            raise ValueError(f"Bounding box north latitude must be in [-90, 90], got {north}")

        # Validate latitude order (south <= north)
        # According to RFC 7946 Section 5.3, poles are special cases but still follow south <= north
        if north < south:
            raise ValueError(
                f"Bounding box north latitude ({north}) must be >= south latitude ({south}). "
                "According to RFC 7946 Section 5.3, even pole cases follow this rule."
            )

        # Validate longitude order (antimeridian crossing allowed)
        if west > east:
            span = (180 - west) + (east - (-180))
            if span >= 360:
                raise ValueError(
                    f"Bounding box with antimeridian crossing: west ({west}) > east ({east}) "
                    "but span is >= 360 degrees, which is invalid."
                )

        # Validate depth/height order (depth <= height)
        if depth > height:
            raise ValueError(f"Bounding box depth ({depth}) must be <= height ({height})")

    # For 1D bbox (length == 2), we don't have specific validation rules in RFC 7946
    # but we can validate that values are numeric
    elif length == 2:
        if not all(isinstance(x, (int, float)) for x in bbox):
            raise ValueError("Bounding box must contain only numeric values")

    return bbox


BoundingBox = Annotated[
    Optional[list[float]],
    AfterValidator(validate_bbox),
    Field(
        default=None,
        title="Bounding Box",
        description="Coordinate range for a GeoJSON Object. Must be array of length 2*n "
        "where n is the number of dimensions (2, 4, or 6 elements). "
        "For 2D: [west, south, east, north]. "
        "For 3D: [west, south, depth, east, north, height].",
    ),
]


# ============================================================================
# Common validators for type mixing prevention (RFC 7946 Section 7.1)
# ============================================================================


def validate_no_feature_members(cls, data):
    """Validate that Geometry objects do not contain Feature-defining members.

    According to RFC 7946 Section 7.1, Geometry objects MUST NOT contain
    "geometry" or "properties" members (which define Feature objects).
    Geometry objects also MUST NOT contain "features" member (which defines
    FeatureCollection objects).

    This validator should be used with @model_validator(mode="before") on
    Geometry model classes.

    Args:
        cls: The model class (used to get the class name).
        data: Input data (dict or model instance).

    Returns:
        The input data if valid.

    Raises:
        ValueError: If forbidden members are present.
    """
    if isinstance(data, dict):
        geometry_type_name = cls.__name__.replace("Model", "")
        forbidden_fields = {"geometry", "properties", "features"}
        for field in forbidden_fields:
            if field in data:
                obj_type = "Feature" if field in ("geometry", "properties") else "FeatureCollection"
                raise ValueError(
                    f'{geometry_type_name} objects MUST NOT contain "{field}" member. '
                    f"According to RFC 7946 Section 7.1, '{field}' defines {obj_type} objects."
                )
    return data


def validate_no_geometry_members(cls, data):
    """Validate that Feature objects do not contain Geometry-defining members.

    According to RFC 7946 Section 7.1, Feature objects MUST NOT contain
    "coordinates" or "geometries" members (which define Geometry objects).
    Feature objects also MUST NOT contain "features" member (which defines
    FeatureCollection objects).

    This validator should be used with @model_validator(mode="before") on
    Feature model classes.

    Args:
        cls: The model class (unused, kept for consistency).
        data: Input data (dict or model instance).

    Returns:
        The input data if valid.

    Raises:
        ValueError: If forbidden members are present.
    """
    if isinstance(data, dict):
        forbidden_fields = {"coordinates", "geometries", "features"}
        for field in forbidden_fields:
            if field in data:
                obj_type = (
                    "Geometry" if field in ("coordinates", "geometries") else "FeatureCollection"
                )
                raise ValueError(
                    f'Feature objects MUST NOT contain "{field}" member. '
                    f"According to RFC 7946 Section 7.1, '{field}' defines {obj_type} objects."
                )
    return data


def validate_no_forbidden_members(cls, data):
    """Validate that FeatureCollection objects do not contain forbidden members.

    According to RFC 7946 Section 7.1:
    - FeatureCollection MUST NOT contain "coordinates" or "geometries" (Geometry-defining)
    - FeatureCollection MUST NOT contain "geometry" or "properties" (Feature-defining)

    This validator should be used with @model_validator(mode="before") on
    FeatureCollection model classes.

    Args:
        cls: The model class (unused, kept for consistency).
        data: Input data (dict or model instance).

    Returns:
        The input data if valid.

    Raises:
        ValueError: If forbidden members are present.
    """
    if isinstance(data, dict):
        forbidden_fields = {"coordinates", "geometries", "geometry", "properties"}
        for field in forbidden_fields:
            if field in data:
                obj_type = "Geometry" if field in ("coordinates", "geometries") else "Feature"
                raise ValueError(
                    f'FeatureCollection objects MUST NOT contain "{field}" member. '
                    f"According to RFC 7946 Section 7.1, '{field}' defines {obj_type} objects."
                )
    return data


class GeoJSONModel(BaseModel):
    """Base class for all GeoJSON models.

    This class provides the common structure for all GeoJSON objects according to
    RFC 7946 specification. All GeoJSON objects must have a "type" field and may
    optionally include a "bbox" (bounding box) field.

    Attributes:
        type: The type of GeoJSON object. Must be one of the valid GeoJSON types.
        bbox: Optional bounding box array. Can contain 2, 4, or 6 elements for
            1D, 2D, or 3D bounding boxes respectively.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

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
