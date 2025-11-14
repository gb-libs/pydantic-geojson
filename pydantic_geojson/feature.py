from typing import Any, Optional, Union

from pydantic import Field, model_validator

from ._base import FeatureFieldType, GeoJSONModel, validate_no_geometry_members
from .geometry_collection import GeometryCollectionModel
from .line_string import LineStringModel
from .multi_line_string import MultiLineStringModel
from .multi_point import MultiPointModel
from .multi_polygon import MultiPolygonModel
from .point import PointModel
from .polygon import PolygonModel


class FeatureModel(GeoJSONModel):
    """Represents a Feature object in GeoJSON format.

    A Feature object represents a spatially bounded thing. According to RFC 7946
    Section 3.2, a Feature object has a "geometry" property and a "properties"
    property. The value of the geometry property is a geometry object as defined
    above or a JSON null value. The value of the properties property is a JSON
    object or a JSON null value.

    A Feature object may have a member named "id". If present, the value of the
    id member is either a JSON string or number.

    Attributes:
        type: The object type, must be "Feature".
        properties: Optional dictionary containing feature properties. Can be
            any JSON-serializable dictionary or None.
        geometry: Optional geometry object. Can be any valid GeoJSON geometry
            type (Point, MultiPoint, LineString, MultiLineString, Polygon,
            MultiPolygon, GeometryCollection) or None.
        id: Optional feature identifier. Can be a string or integer, or None.
        bbox: Optional bounding box array.
    """

    type: FeatureFieldType
    properties: Optional[dict[str, Any]] = Field(
        default=None,
        description="A JSON object or JSON null value containing feature properties.",
    )
    geometry: Optional[
        Union[
            PointModel,
            MultiPointModel,
            LineStringModel,
            MultiLineStringModel,
            PolygonModel,
            MultiPolygonModel,
            GeometryCollectionModel,
        ]
    ] = Field(
        default=None,
        description="A geometry object as defined above or a JSON null value.",
    )
    id: Optional[Union[int, str]] = Field(
        default=None,
        description="A unique identifier for the feature. If present, must be a JSON string or number.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_no_geometry_members(cls, data):
        """Validate that Feature does not contain Geometry-defining members.

        Args:
            cls: The model class.
            data: Input data (dict or model instance).

        Returns:
            The input data if valid.

        Raises:
            ValueError: If forbidden members are present.
        """
        return validate_no_geometry_members(cls, data)
