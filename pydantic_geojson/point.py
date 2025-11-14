from pydantic import Field, model_validator

from ._base import Coordinates, GeoJSONModel, PointFieldType, validate_no_feature_members


class PointModel(GeoJSONModel):
    """Represents a Point geometry in GeoJSON format.

    A Point is a single position specified by its coordinates. According to
    RFC 7946 Section 3.1.2, a Point geometry object has coordinates that are
    a single position.

    Attributes:
        type: The geometry type, must be "Point".
        coordinates: A single coordinate position (longitude, latitude, optional altitude).
        bbox: Optional bounding box array.
    """

    type: PointFieldType
    coordinates: Coordinates = Field(
        ...,
        description="A single coordinate position. Must be [longitude, latitude] "
        "or [longitude, latitude, altitude].",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that Point does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
