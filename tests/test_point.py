"""Tests for PointModel."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import PointModel
from pydantic_geojson.object_type import POINT
from tests.test_utils import assert_coordinates_equal


class TestPointModel:
    """Test suite for PointModel validation and serialization."""

    def test_valid_point_creation(self, valid_point_data):
        """Test creating a valid Point model."""
        point = PointModel(**valid_point_data)

        assert point.type == POINT
        assert point.type == valid_point_data["type"]
        assert_coordinates_equal(point.coordinates, valid_point_data["coordinates"])

    def test_valid_point_with_altitude(self, valid_point_3d_data):
        """Test creating a Point with altitude."""
        point = PointModel(**valid_point_3d_data)

        assert point.type == POINT
        assert_coordinates_equal(point.coordinates, valid_point_3d_data["coordinates"])

    @pytest.mark.parametrize(
        "name,coords",
        [
            ("lon_min", [-180, 0]),
            ("lon_max", [180, 0]),
            ("lat_min", [0, -90]),
            ("lat_max", [0, 90]),
            ("corner_sw", [-180, -90]),
            ("corner_ne", [180, 90]),
            ("corner_nw", [-180, 90]),
            ("corner_se", [180, -90]),
        ],
    )
    def test_point_boundary_coordinates(self, name, coords):
        """Test Point with coordinates at valid boundaries."""
        data = {"type": "Point", "coordinates": coords}
        point = PointModel(**data)
        assert point.type == POINT
        assert_coordinates_equal(point.coordinates, coords)

    @pytest.mark.parametrize(
        "invalid_coord",
        [
            "lon_too_small",
            "lon_too_large",
            "lat_too_small",
            "lat_too_large",
        ],
    )
    def test_point_invalid_coordinates(self, invalid_coordinates, invalid_coord):
        """Test Point with invalid coordinate ranges."""
        data = {"type": "Point", "coordinates": invalid_coordinates[invalid_coord]}
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert (
            "Input should be greater than or equal to -180" in error_str
            or "Input should be less than or equal to 180" in error_str
            or "Input should be greater than or equal to -90" in error_str
            or "Input should be less than or equal to 90" in error_str
        )

    def test_point_invalid_type(self, invalid_point_bad_type):
        """Test Point with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**invalid_point_bad_type)

        assert "Input should be 'Point'" in str(exc_info.value)

    def test_point_serialization(self, valid_point_data):
        """Test Point model serialization to dict."""
        point = PointModel(**valid_point_data)
        serialized = point.model_dump(mode="json")

        assert serialized["type"] == "Point"
        # Coordinates may include None for altitude, so check first 2 elements
        assert serialized["coordinates"][:2] == valid_point_data["coordinates"]
        assert "bbox" in serialized
        assert serialized["bbox"] is None

    def test_point_json_serialization(self, valid_point_data):
        """Test Point model JSON serialization."""
        point = PointModel(**valid_point_data)
        json_str = point.model_dump_json()

        assert '"type":"Point"' in json_str
        assert str(valid_point_data["coordinates"][0]) in json_str
        assert str(valid_point_data["coordinates"][1]) in json_str

    def test_point_from_json(self, valid_point_data):
        """Test creating Point from JSON string."""
        import json

        json_str = json.dumps(valid_point_data)
        point = PointModel.model_validate_json(json_str)

        assert point.type == POINT
        assert_coordinates_equal(point.coordinates, valid_point_data["coordinates"])

    def test_point_with_bbox(self, valid_point_data, bbox_2d):
        """Test Point with bounding box."""
        data = {**valid_point_data, "bbox": bbox_2d}
        point = PointModel(**data)

        assert point.bbox == bbox_2d
        assert point.type == POINT

    def test_point_with_bbox_3d(self, valid_point_3d_data, bbox_3d):
        """Test Point with 3D bounding box."""
        data = {**valid_point_3d_data, "bbox": bbox_3d}
        point = PointModel(**data)

        assert point.bbox == bbox_3d
        assert point.type == POINT
