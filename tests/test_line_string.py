"""Tests for LineStringModel."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import LineStringModel
from pydantic_geojson.object_type import LINE_STRING
from tests.test_utils import assert_coordinates_equal


class TestLineStringModel:
    """Test suite for LineStringModel validation and serialization."""

    def test_valid_linestring_creation(self, valid_linestring_data):
        """Test creating a valid LineString model."""
        ls_model = LineStringModel(**valid_linestring_data)

        assert ls_model.type == LINE_STRING
        assert ls_model.type == valid_linestring_data["type"]
        assert len(ls_model.coordinates) == len(valid_linestring_data["coordinates"])

        for idx, coord in enumerate(ls_model.coordinates):
            expected = valid_linestring_data["coordinates"][idx]
            assert_coordinates_equal(coord, expected)

    def test_valid_linestring_minimal(self, valid_linestring_minimal):
        """Test LineString with minimal required coordinates (2 points)."""
        ls_model = LineStringModel(**valid_linestring_minimal)

        assert ls_model.type == LINE_STRING
        assert len(ls_model.coordinates) == 2

    def test_linestring_must_have_at_least_two_coords(self, invalid_linestring_one_coordinate):
        """Test that LineString requires at least 2 coordinates."""
        with pytest.raises(ValidationError) as exc_info:
            LineStringModel(**invalid_linestring_one_coordinate)

        error_str = str(exc_info.value)
        assert "too_short" in error_str or "at least 2" in error_str.lower()

    def test_linestring_empty_coordinates(self, invalid_linestring_empty):
        """Test that LineString cannot have empty coordinates."""
        with pytest.raises(ValidationError) as exc_info:
            LineStringModel(**invalid_linestring_empty)

        error_str = str(exc_info.value)
        assert "too_short" in error_str or "at least 2" in error_str.lower()

    def test_linestring_invalid_type(self, invalid_linestring_bad_type):
        """Test LineString with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            LineStringModel(**invalid_linestring_bad_type)

        assert "Input should be 'LineString'" in str(exc_info.value)

    def test_linestring_serialization(self, valid_linestring_data):
        """Test LineString model serialization to dict."""
        ls_model = LineStringModel(**valid_linestring_data)
        serialized = ls_model.model_dump(mode="json")

        assert serialized["type"] == "LineString"
        assert len(serialized["coordinates"]) == len(valid_linestring_data["coordinates"])
        # Coordinates may include None for altitude, so check first 2 elements of each coordinate
        for idx, coord in enumerate(serialized["coordinates"]):
            assert coord[:2] == valid_linestring_data["coordinates"][idx]
        assert "bbox" in serialized

    def test_linestring_json_serialization(self, valid_linestring_data):
        """Test LineString model JSON serialization."""
        ls_model = LineStringModel(**valid_linestring_data)
        json_str = ls_model.model_dump_json()

        assert '"type":"LineString"' in json_str
        assert len(valid_linestring_data["coordinates"]) > 0
        # Check that coordinates are in JSON
        assert str(valid_linestring_data["coordinates"][0][0]) in json_str

    def test_linestring_from_json(self, valid_linestring_data):
        """Test creating LineString from JSON string."""
        import json

        json_str = json.dumps(valid_linestring_data)
        ls_model = LineStringModel.model_validate_json(json_str)

        assert ls_model.type == LINE_STRING
        assert len(ls_model.coordinates) == len(valid_linestring_data["coordinates"])

    def test_linestring_with_bbox(self, valid_linestring_data, bbox_2d):
        """Test LineString with bounding box."""
        data = {**valid_linestring_data, "bbox": bbox_2d}
        ls_model = LineStringModel(**data)

        assert ls_model.bbox == bbox_2d
        assert ls_model.type == LINE_STRING

    def test_linestring_boundary_coordinates(self, boundary_coordinates):
        """Test LineString with coordinates at valid boundaries."""
        coords = [
            boundary_coordinates["corner_sw"],
            boundary_coordinates["corner_ne"],
        ]
        data = {"type": "LineString", "coordinates": coords}
        ls_model = LineStringModel(**data)

        assert ls_model.type == LINE_STRING
        assert len(ls_model.coordinates) == 2
