from pydantic import Field, model_validator

from ._base import FeatureCollectionFieldType, GeoJSONModel, validate_no_forbidden_members
from .feature import FeatureModel


class FeatureCollectionModel(GeoJSONModel):
    """Represents a FeatureCollection object in GeoJSON format.

    A FeatureCollection object contains a collection of Feature objects. According
    to RFC 7946 Section 3.3, a FeatureCollection object has a member with the name
    "features". The value of "features" is a JSON array. Each element of the array
    is a Feature object as defined above.

    Attributes:
        type: The object type, must be "FeatureCollection".
        features: An array of Feature objects.
        bbox: Optional bounding box array.
    """

    type: FeatureCollectionFieldType
    features: list[FeatureModel] = Field(
        ...,
        description="A JSON array of Feature objects. Each element is a Feature "
        "object as defined in RFC 7946 Section 3.2.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_forbidden_members(cls, data):
        """Validate that FeatureCollection does not contain forbidden members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_forbidden_members(cls, data)
