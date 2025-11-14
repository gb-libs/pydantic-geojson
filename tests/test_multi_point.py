"""Tests for MultiPointModel."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import MultiPointModel
from pydantic_geojson.object_type import MULTI_POINT
from tests.test_utils import assert_coordinates_equal


class TestMultiPointModel:
    """Test suite for MultiPointModel validation and serialization."""

    def test_valid_multi_point_creation(self, valid_multi_point_data):
        """Test creating a valid MultiPoint model."""
        mp_model = MultiPointModel(**valid_multi_point_data)

        assert mp_model.type == MULTI_POINT
        assert mp_model.type == valid_multi_point_data["type"]
        assert len(mp_model.coordinates) == len(valid_multi_point_data["coordinates"])

        for idx, coord in enumerate(mp_model.coordinates):
            expected = valid_multi_point_data["coordinates"][idx]
            assert_coordinates_equal(coord, expected)

    def test_valid_multi_point_single(self, valid_multi_point_single):
        """Test MultiPoint with a single point."""
        mp_model = MultiPointModel(**valid_multi_point_single)

        assert mp_model.type == MULTI_POINT
        assert len(mp_model.coordinates) == 1

    def test_multi_point_invalid_type(self, invalid_bad_multi_point_type):
        """Test MultiPoint with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            MultiPointModel(**invalid_bad_multi_point_type)

        assert "Input should be 'MultiPoint'" in str(exc_info.value)

    def test_multi_point_serialization(self, valid_multi_point_data):
        """Test MultiPoint model serialization to dict."""
        mp_model = MultiPointModel(**valid_multi_point_data)
        serialized = mp_model.model_dump(mode="json")

        assert serialized["type"] == "MultiPoint"
        assert len(serialized["coordinates"]) == len(valid_multi_point_data["coordinates"])
        # Coordinates may include None for altitude, so check first 2 elements of each coordinate
        for idx, coord in enumerate(serialized["coordinates"]):
            assert coord[:2] == valid_multi_point_data["coordinates"][idx]
        assert "bbox" in serialized

    def test_multi_point_json_serialization(self, valid_multi_point_data):
        """Test MultiPoint model JSON serialization."""
        mp_model = MultiPointModel(**valid_multi_point_data)
        json_str = mp_model.model_dump_json()

        assert '"type":"MultiPoint"' in json_str
        assert str(valid_multi_point_data["coordinates"][0][0]) in json_str

    def test_multi_point_from_json(self, valid_multi_point_data):
        """Test creating MultiPoint from JSON string."""
        import json

        json_str = json.dumps(valid_multi_point_data)
        mp_model = MultiPointModel.model_validate_json(json_str)

        assert mp_model.type == MULTI_POINT
        assert len(mp_model.coordinates) == len(valid_multi_point_data["coordinates"])

    def test_multi_point_with_bbox(self, valid_multi_point_data, bbox_2d):
        """Test MultiPoint with bounding box."""
        data = {**valid_multi_point_data, "bbox": bbox_2d}
        mp_model = MultiPointModel(**data)

        assert mp_model.bbox == bbox_2d
        assert mp_model.type == MULTI_POINT

    def test_multi_point_empty(self):
        """Test MultiPoint with empty coordinates list."""
        data = {"type": "MultiPoint", "coordinates": []}
        mp_model = MultiPointModel(**data)

        assert mp_model.type == MULTI_POINT
        assert len(mp_model.coordinates) == 0
