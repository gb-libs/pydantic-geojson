from pydantic import Field, model_validator

from ._base import GeoJSONModel, LinearRing, PolygonFieldType, validate_no_feature_members


class PolygonModel(GeoJSONModel):
    """Represents a Polygon geometry in GeoJSON format.

    A Polygon is a planar surface defined by one exterior boundary and zero or
    more interior boundaries. According to RFC 7946 Section 3.1.6, a Polygon
    geometry object has coordinates that are an array of linear ring coordinate arrays.

    The first element of the coordinates array represents the exterior ring.
    Any subsequent elements represent interior rings (holes).

    Attributes:
        type: The geometry type, must be "Polygon".
        coordinates: An array of linear rings. The first ring is the exterior
            boundary, subsequent rings are interior boundaries (holes).
        bbox: Optional bounding box array.
    """

    type: PolygonFieldType
    coordinates: list[LinearRing] = Field(
        ...,
        description="An array of linear ring coordinate arrays. The first ring "
        "is the exterior boundary, subsequent rings are interior boundaries (holes). "
        "Each linear ring must have at least 4 positions and be closed.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that Polygon does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
