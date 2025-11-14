"""Tests for object_type module."""

import pytest

from pydantic_geojson import object_type


class TestFormatStringType:
    """Test suite for object type string constants."""

    @pytest.mark.parametrize(
        "constant,expected_value",
        [
            (object_type.POINT, "Point"),
            (object_type.MULTI_POINT, "MultiPoint"),
            (object_type.LINE_STRING, "LineString"),
            (object_type.MULTI_LINE_STRING, "MultiLineString"),
            (object_type.POLYGON, "Polygon"),
            (object_type.MULTI_POLYGON, "MultiPolygon"),
            (object_type.GEOMETRY_COLLECTION, "GeometryCollection"),
            (object_type.FEATURE, "Feature"),
            (object_type.FEATURE_COLLECTION, "FeatureCollection"),
        ],
    )
    def test_format_string_constants(self, constant, expected_value):
        """Test that all object type constants have correct string values."""
        assert constant == expected_value


class TestGeometryType:
    """Test suite for GeometryType enum."""

    @pytest.mark.parametrize(
        "enum_member,expected_value",
        [
            (object_type.GeometryType.point, object_type.POINT),
            (object_type.GeometryType.multi_point, object_type.MULTI_POINT),
            (object_type.GeometryType.line_string, object_type.LINE_STRING),
            (object_type.GeometryType.multi_line_string, object_type.MULTI_LINE_STRING),
            (object_type.GeometryType.polygon, object_type.POLYGON),
            (object_type.GeometryType.multi_polygon, object_type.MULTI_POLYGON),
            (object_type.GeometryType.geometry_collection, object_type.GEOMETRY_COLLECTION),
        ],
    )
    def test_geometry_type_values(self, enum_member, expected_value):
        """Test that GeometryType enum members have correct values."""
        assert enum_member.value == expected_value

    def test_geometry_type_length(self):
        """Test that GeometryType enum has correct number of members."""
        assert len(list(object_type.GeometryType)) == 7

    def test_geometry_type_iteration(self):
        """Test that GeometryType can be iterated."""
        types = list(object_type.GeometryType)
        assert len(types) == 7
        assert all(hasattr(t, "value") for t in types)
