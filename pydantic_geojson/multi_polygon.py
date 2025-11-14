from typing import Annotated

from pydantic import AfterValidator, Field, model_validator

from ._base import GeoJSONModel, LinearRing, MultiPolygonFieldType, validate_no_feature_members


def validate_polygon_rings(rings: list[LinearRing]) -> list[LinearRing]:
    """Validate that a Polygon has at least one linear ring.

    According to RFC 7946 Section 3.1.6, a Polygon must have an array of linear ring
    coordinate arrays. The first ring is the exterior ring, and any others are interior rings.
    A Polygon must have at least one ring (the exterior ring).

    Args:
        rings: List of LinearRing representing a Polygon.

    Returns:
        The validated rings list.

    Raises:
        ValueError: If the Polygon has no rings.
    """
    if len(rings) == 0:
        raise ValueError(
            "Polygon must have at least one linear ring (the exterior ring). "
            "According to RFC 7946 Section 3.1.6, Polygon coordinates must be an array of linear ring coordinate arrays."
        )
    return rings


PolygonRings = Annotated[list[LinearRing], AfterValidator(validate_polygon_rings)]


class MultiPolygonModel(GeoJSONModel):
    """Represents a MultiPolygon geometry in GeoJSON format.

    A MultiPolygon is a collection of Polygon geometries. According to RFC 7946
    Section 3.1.7, a MultiPolygon geometry object has coordinates that are an
    array of Polygon coordinate arrays.

    Attributes:
        type: The geometry type, must be "MultiPolygon".
        coordinates: An array of Polygon coordinate arrays, where each Polygon
            is represented by an array of linear rings. Each Polygon must have
            at least one ring (the exterior ring).
        bbox: Optional bounding box array.
    """

    type: MultiPolygonFieldType
    coordinates: list[PolygonRings] = Field(
        ...,
        min_length=0,
        description="An array of Polygon coordinate arrays. Each Polygon is "
        "represented by an array of linear rings, with at least one ring (the exterior ring).",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that MultiPolygon does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
