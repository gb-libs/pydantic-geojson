from pydantic import Field, model_validator

from ._base import Coordinates, GeoJSONModel, LineStringFieldType, validate_no_feature_members


class LineStringModel(GeoJSONModel):
    """Represents a LineString geometry in GeoJSON format.

    A LineString is a curve with linear interpolation between points. According to
    RFC 7946 Section 3.1.4, a LineString geometry object has coordinates that
    are an array of two or more positions.

    Attributes:
        type: The geometry type, must be "LineString".
        coordinates: An array of two or more coordinate positions that form a line.
        bbox: Optional bounding box array.
    """

    type: LineStringFieldType
    coordinates: list[Coordinates] = Field(
        ...,
        min_length=2,
        description="An array of two or more positions. Each position is "
        "[longitude, latitude] or [longitude, latitude, altitude].",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that LineString does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
