"""GeoJSON object type constants and enumeration.

This module defines constants and enumeration for GeoJSON object types
according to RFC 7946 Section 1.4.

Reference: https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
"""

from enum import Enum

POINT = "Point"
MULTI_POINT = "MultiPoint"
LINE_STRING = "LineString"
MULTI_LINE_STRING = "MultiLineString"
POLYGON = "Polygon"
MULTI_POLYGON = "MultiPolygon"
GEOMETRY_COLLECTION = "GeometryCollection"


class GeometryType(str, Enum):
    """Enumeration of valid GeoJSON geometry types.

    According to RFC 7946, the term "geometry type" refers to seven
    case-sensitive strings: "Point", "MultiPoint", "LineString",
    "MultiLineString", "Polygon", "MultiPolygon", and "GeometryCollection".

    Attributes:
        point: Point geometry type.
        multi_point: MultiPoint geometry type.
        line_string: LineString geometry type.
        multi_line_string: MultiLineString geometry type.
        polygon: Polygon geometry type.
        multi_polygon: MultiPolygon geometry type.
        geometry_collection: GeometryCollection geometry type.
    """

    point = POINT
    multi_point = MULTI_POINT
    line_string = LINE_STRING
    multi_line_string = MULTI_LINE_STRING
    polygon = POLYGON
    multi_polygon = MULTI_POLYGON
    geometry_collection = GEOMETRY_COLLECTION


FEATURE = "Feature"
FEATURE_COLLECTION = "FeatureCollection"
