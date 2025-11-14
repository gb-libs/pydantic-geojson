from pydantic import Field, model_validator

from ._base import Coordinates, GeoJSONModel, MultiPointFieldType, validate_no_feature_members


class MultiPointModel(GeoJSONModel):
    """Represents a MultiPoint geometry in GeoJSON format.

    A MultiPoint is a collection of Point geometries. According to RFC 7946
    Section 3.1.3, a MultiPoint geometry object has coordinates that are an
    array of positions.

    Attributes:
        type: The geometry type, must be "MultiPoint".
        coordinates: An array of coordinate positions, each representing a point.
        bbox: Optional bounding box array.
    """

    type: MultiPointFieldType
    coordinates: list[Coordinates] = Field(
        ...,
        description="An array of positions. Each position is "
        "[longitude, latitude] or [longitude, latitude, altitude].",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that MultiPoint does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)
