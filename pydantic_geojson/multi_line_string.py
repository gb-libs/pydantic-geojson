from typing import Annotated

from pydantic import AfterValidator, Field, model_validator

from ._base import Coordinates, GeoJSONModel, MultiLineStringFieldType, validate_no_feature_members


def validate_linestring_coordinates(coords: list[Coordinates]) -> list[Coordinates]:
    """Validate that a LineString has at least 2 coordinates.

    According to RFC 7946 Section 3.1.4, a LineString must have two or more positions.

    Args:
        coords: List of Coordinates representing a LineString.

    Returns:
        The validated coordinates list.

    Raises:
        ValueError: If the LineString has fewer than 2 coordinates.
    """
    if len(coords) < 2:
        raise ValueError(
            f"LineString must have at least 2 coordinates (got {len(coords)}). "
            "According to RFC 7946 Section 3.1.4, LineString coordinates must be an array of two or more positions."
        )
    return coords


LineStringCoordinates = Annotated[
    list[Coordinates], AfterValidator(validate_linestring_coordinates)
]


class MultiLineStringModel(GeoJSONModel):
    """Represents a MultiLineString geometry in GeoJSON format.

    A MultiLineString is a collection of LineString geometries. According to
    RFC 7946 Section 3.1.5, a MultiLineString geometry object has coordinates
    that are an array of LineString coordinate arrays.

    Attributes:
        type: The geometry type, must be "MultiLineString".
        coordinates: An array of LineString coordinate arrays, where each inner
            array contains two or more positions.
        bbox: Optional bounding box array.
    """

    type: MultiLineStringFieldType
    coordinates: list[LineStringCoordinates] = Field(
        ...,
        min_length=0,
        description="An array of LineString coordinate arrays. Each inner array "
        "must contain at least 2 positions.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that MultiLineString does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
