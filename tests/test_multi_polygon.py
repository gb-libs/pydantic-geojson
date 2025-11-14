"""Tests for MultiPolygonModel."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import MultiPolygonModel
from pydantic_geojson.object_type import MULTI_POLYGON
from tests.test_utils import assert_coordinates_equal


class TestMultiPolygonModel:
    """Test suite for MultiPolygonModel validation and serialization."""

    def test_valid_multi_polygon_creation(self, valid_multi_polygon):
        """Test creating a valid MultiPolygon model."""
        mp_model = MultiPolygonModel(**valid_multi_polygon)

        assert mp_model.type == MULTI_POLYGON
        assert mp_model.type == valid_multi_polygon["type"]
        assert len(mp_model.coordinates) == len(valid_multi_polygon["coordinates"])

        for poly_idx, polygon in enumerate(mp_model.coordinates):
            expected_polygon = valid_multi_polygon["coordinates"][poly_idx]
            assert len(polygon) == len(expected_polygon)

            for ring_idx, ring in enumerate(polygon):
                expected_ring = expected_polygon[ring_idx]
                assert len(ring) == len(expected_ring)

                for coord_idx, coord in enumerate(ring):
                    expected_coord = expected_ring[coord_idx]
                    assert_coordinates_equal(coord, expected_coord)

    def test_multi_polygon_invalid_type(self, invalid_multi_polygon_wrong_type):
        """Test MultiPolygon with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            MultiPolygonModel(**invalid_multi_polygon_wrong_type)

        assert "Input should be 'MultiPolygon'" in str(exc_info.value)

    def test_multi_polygon_linear_ring_validation(
        self, invalid_multi_polygon_linear_ring_validation
    ):
        """Test MultiPolygon with invalid linear rings."""
        with pytest.raises(ValidationError) as exc_info:
            MultiPolygonModel(**invalid_multi_polygon_linear_ring_validation)

        error_str = str(exc_info.value)
        # Should have errors for both invalid rings
        assert (
            "Linear Ring length must be >=4" in error_str
            or "Linear Rings must start and end at the same coordinate" in error_str
        )

    def test_multi_polygon_serialization(self, valid_multi_polygon):
        """Test MultiPolygon model serialization to dict."""
        mp_model = MultiPolygonModel(**valid_multi_polygon)
        serialized = mp_model.model_dump(mode="json")

        assert serialized["type"] == "MultiPolygon"
        assert len(serialized["coordinates"]) == len(valid_multi_polygon["coordinates"])
        assert "bbox" in serialized

    def test_multi_polygon_json_serialization(self, valid_multi_polygon):
        """Test MultiPolygon model JSON serialization."""
        mp_model = MultiPolygonModel(**valid_multi_polygon)
        json_str = mp_model.model_dump_json()

        assert '"type":"MultiPolygon"' in json_str
        assert str(valid_multi_polygon["coordinates"][0][0][0][0]) in json_str

    def test_multi_polygon_from_json(self, valid_multi_polygon):
        """Test creating MultiPolygon from JSON string."""
        import json

        json_str = json.dumps(valid_multi_polygon)
        mp_model = MultiPolygonModel.model_validate_json(json_str)

        assert mp_model.type == MULTI_POLYGON
        assert len(mp_model.coordinates) == len(valid_multi_polygon["coordinates"])

    def test_multi_polygon_with_bbox(self, valid_multi_polygon, bbox_2d):
        """Test MultiPolygon with bounding box."""
        data = {**valid_multi_polygon, "bbox": bbox_2d}
        mp_model = MultiPolygonModel(**data)

        assert mp_model.bbox == bbox_2d
        assert mp_model.type == MULTI_POLYGON

    def test_multi_polygon_empty(self):
        """Test MultiPolygon with empty coordinates list."""
        data = {"type": "MultiPolygon", "coordinates": []}
        mp_model = MultiPolygonModel(**data)

        assert mp_model.type == MULTI_POLYGON
        assert len(mp_model.coordinates) == 0

    def test_multi_polygon_empty_polygon_rejected(self):
        """Test MultiPolygon with empty Polygon (no rings) is rejected."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [[]],  # Empty Polygon (no rings)
        }
        with pytest.raises(ValidationError) as exc_info:
            MultiPolygonModel(**data)

        error_str = str(exc_info.value)
        assert "at least one linear ring" in error_str or "Polygon must have" in error_str
        assert "RFC 7946" in error_str or "Section 3.1.6" in error_str

    def test_multi_polygon_mixed_valid_invalid_rejected(self):
        """Test MultiPolygon with mix of valid and invalid Polygons is rejected."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],  # Valid Polygon (1 ring)
                [],  # Invalid Polygon (no rings)
            ],
        }
        with pytest.raises(ValidationError) as exc_info:
            MultiPolygonModel(**data)

        error_str = str(exc_info.value)
        assert "at least one linear ring" in error_str or "Polygon must have" in error_str

    def test_multi_polygon_minimal_valid(self):
        """Test MultiPolygon with minimal valid Polygons (one ring each)."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],  # Minimal valid Polygon (1 ring)
                [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]],  # Another minimal valid Polygon
            ],
        }
        mp_model = MultiPolygonModel(**data)
        assert mp_model.type == MULTI_POLYGON
        assert len(mp_model.coordinates) == 2
        assert len(mp_model.coordinates[0]) == 1  # One ring
        assert len(mp_model.coordinates[1]) == 1  # One ring

    def test_multi_polygon_with_holes_valid(self):
        """Test MultiPolygon with Polygons that have holes (multiple rings)."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],  # Exterior ring
                    [[2, 2], [8, 2], [8, 8], [2, 8], [2, 2]],  # Interior ring (hole)
                ],
            ],
        }
        mp_model = MultiPolygonModel(**data)
        assert mp_model.type == MULTI_POLYGON
        assert len(mp_model.coordinates) == 1
        assert len(mp_model.coordinates[0]) == 2  # Exterior + 1 hole
