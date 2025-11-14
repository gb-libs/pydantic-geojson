"""Tests for PolygonModel."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import PolygonModel
from pydantic_geojson.object_type import POLYGON
from tests.test_utils import assert_coordinates_equal


class TestPolygonModel:
    """Test suite for PolygonModel validation and serialization."""

    def test_valid_polygon_creation(self, valid_polygon_data):
        """Test creating a valid Polygon model."""
        p_model = PolygonModel(**valid_polygon_data)

        assert p_model.type == POLYGON
        assert p_model.type == valid_polygon_data["type"]
        assert len(p_model.coordinates) == len(valid_polygon_data["coordinates"])

        for ring_idx, ring in enumerate(p_model.coordinates):
            expected_ring = valid_polygon_data["coordinates"][ring_idx]
            assert len(ring) == len(expected_ring)

            for coord_idx, coord in enumerate(ring):
                expected_coord = expected_ring[coord_idx]
                assert_coordinates_equal(coord, expected_coord)

    def test_valid_polygon_with_holes(self, valid_polygon_with_holes):
        """Test Polygon with interior rings (holes)."""
        p_model = PolygonModel(**valid_polygon_with_holes)

        assert p_model.type == POLYGON
        assert len(p_model.coordinates) == 2  # exterior + 1 hole

    def test_polygon_linear_ring_must_close(self, invalid_polygon_data_no_loop):
        """Test that Polygon linear rings must start and end at the same coordinate."""
        with pytest.raises(ValidationError) as exc_info:
            PolygonModel(**invalid_polygon_data_no_loop)

        error_str = str(exc_info.value)
        assert "Linear Rings must start and end at the same coordinate" in error_str

    def test_polygon_linear_ring_minimum_length(self, invalid_polygon_data_too_few_points):
        """Test that Polygon linear rings must have at least 4 points."""
        with pytest.raises(ValidationError) as exc_info:
            PolygonModel(**invalid_polygon_data_too_few_points)

        error_str = str(exc_info.value)
        assert "Linear Ring length must be >=4" in error_str
        assert "not 3" in error_str

    def test_polygon_invalid_type(self, invalid_polygon_data_bad_type):
        """Test Polygon with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            PolygonModel(**invalid_polygon_data_bad_type)

        assert "Input should be 'Polygon'" in str(exc_info.value)

    def test_polygon_serialization(self, valid_polygon_data):
        """Test Polygon model serialization to dict."""
        p_model = PolygonModel(**valid_polygon_data)
        serialized = p_model.model_dump(mode="json")

        assert serialized["type"] == "Polygon"
        assert len(serialized["coordinates"]) == len(valid_polygon_data["coordinates"])
        assert "bbox" in serialized

        # Verify coordinates structure
        for ring_idx, ring in enumerate(serialized["coordinates"]):
            expected_ring = valid_polygon_data["coordinates"][ring_idx]
            assert len(ring) == len(expected_ring)

    def test_polygon_json_serialization(self, valid_polygon_data):
        """Test Polygon model JSON serialization."""
        p_model = PolygonModel(**valid_polygon_data)
        json_str = p_model.model_dump_json()

        assert '"type":"Polygon"' in json_str
        # Verify coordinates are in JSON
        assert str(valid_polygon_data["coordinates"][0][0][0]) in json_str

    def test_polygon_from_json(self, valid_polygon_data):
        """Test creating Polygon from JSON string."""
        import json

        json_str = json.dumps(valid_polygon_data)
        p_model = PolygonModel.model_validate_json(json_str)

        assert p_model.type == POLYGON
        assert len(p_model.coordinates) == len(valid_polygon_data["coordinates"])

    def test_polygon_with_bbox(self, valid_polygon_data, bbox_2d):
        """Test Polygon with bounding box."""
        data = {**valid_polygon_data, "bbox": bbox_2d}
        p_model = PolygonModel(**data)

        assert p_model.bbox == bbox_2d
        assert p_model.type == POLYGON

    def test_polygon_exterior_ring_validation(self):
        """Test that exterior ring is properly validated."""
        # Valid polygon with exactly 4 points (minimum)
        data = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        }
        p_model = PolygonModel(**data)
        assert p_model.type == POLYGON
        assert len(p_model.coordinates[0]) == 4
