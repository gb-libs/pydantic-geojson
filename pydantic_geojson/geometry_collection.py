from typing import Union

from pydantic import Field, model_validator

from ._base import GeoJSONModel, GeometryCollectionFieldType, validate_no_feature_members
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class GeometryCollectionModel(GeoJSONModel):
    """Represents a GeometryCollection in GeoJSON format.

    A GeometryCollection is a collection of geometry objects of any type. According
    to RFC 7946 Section 3.1.8, a GeometryCollection has a "geometries" property
    containing an array of geometry objects.

    A GeometryCollection may contain other GeometryCollection objects, allowing
    for nested collections.

    Attributes:
        type: The geometry type, must be "GeometryCollection".
        geometries: An array of geometry objects. Each geometry can be any valid
            GeoJSON geometry type, including another GeometryCollection.
        bbox: Optional bounding box array.
    """

    type: GeometryCollectionFieldType
    geometries: list[
        Union[
            PointModel,
            MultiPointModel,
            LineStringModel,
            MultiLineStringModel,
            PolygonModel,
            MultiPolygonModel,
            "GeometryCollectionModel",
        ]
    ] = Field(
        ...,
        description="An array of geometry objects. Each geometry can be any valid "
        "GeoJSON geometry type, including another GeometryCollection.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_feature_members(cls, data):
        """Validate that GeometryCollection does not contain Feature-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_feature_members(cls, data)


# Required for recursive type: GeometryCollectionModel contains itself in the geometries list.
# Using string annotation "GeometryCollectionModel" allows forward reference.
# Pydantic needs model_rebuild() to resolve the forward reference to the class itself.
GeometryCollectionModel.model_rebuild()
