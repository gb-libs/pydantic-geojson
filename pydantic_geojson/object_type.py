from enum import Enum

"""
https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
"""

POINT = "Point"
MULTI_POINT = "MultiPoint"
LINE_STRING = "LineString"
MULTI_LINE_STRING = "MultiLineString"
POLYGON = "Polygon"
MULTI_POLYGON = "MultiPolygon"
GEOMETRY_COLLECTION = "GeometryCollection"


class GeometryType(str, Enum):
    """
    Inside this document, the term "geometry type" refers to seven
    case-sensitive strings: "Point", "MultiPoint", "LineString",
    "MultiLineString", "Polygon", "MultiPolygon", and
    "GeometryCollection".
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
