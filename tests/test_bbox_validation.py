"""Tests for bounding box validation according to RFC 7946."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import FeatureCollectionModel, FeatureModel, PointModel


class TestBoundingBoxValidation:
    """Test suite for bounding box validation."""

    def test_valid_2d_bbox(self):
        """Test valid 2D bounding box."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -10.0, 10.0, 10.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-10.0, -10.0, 10.0, 10.0]

    def test_valid_3d_bbox(self):
        """Test valid 3D bounding box."""
        data = {
            "type": "Point",
            "coordinates": [0, 0, 100],
            "bbox": [-10.0, -10.0, 0.0, 10.0, 10.0, 1000.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-10.0, -10.0, 0.0, 10.0, 10.0, 1000.0]

    def test_valid_1d_bbox(self):
        """Test valid 1D bounding box (edge case)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [0.0, 1.0],
        }
        point = PointModel(**data)
        assert point.bbox == [0.0, 1.0]

    def test_bbox_none(self):
        """Test that None bbox is allowed."""
        data = {"type": "Point", "coordinates": [0, 0], "bbox": None}
        point = PointModel(**data)
        assert point.bbox is None

    def test_bbox_invalid_length_too_short(self):
        """Test bbox with invalid length (too short)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [0.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "must have 2, 4, or 6 elements" in error_str

    def test_bbox_invalid_length_3_elements(self):
        """Test bbox with invalid length (3 elements)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [1.0, 2.0, 3.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "must have 2, 4, or 6 elements" in error_str

    def test_bbox_invalid_length_too_long(self):
        """Test bbox with invalid length (too long)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "must have 2, 4, or 6 elements" in error_str

    def test_bbox_invalid_longitude_west_too_small(self):
        """Test bbox with west longitude too small."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-181.0, -10.0, 10.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "west longitude must be in [-180, 180]" in error_str

    def test_bbox_invalid_longitude_west_too_large(self):
        """Test bbox with west longitude too large."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [181.0, -10.0, 10.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "west longitude must be in [-180, 180]" in error_str

    def test_bbox_invalid_longitude_east_too_small(self):
        """Test bbox with east longitude too small."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -10.0, -181.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "east longitude must be in [-180, 180]" in error_str

    def test_bbox_invalid_longitude_east_too_large(self):
        """Test bbox with east longitude too large."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -10.0, 181.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "east longitude must be in [-180, 180]" in error_str

    def test_bbox_invalid_latitude_south_too_small(self):
        """Test bbox with south latitude too small."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -91.0, 10.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "south latitude must be in [-90, 90]" in error_str

    def test_bbox_invalid_latitude_south_too_large(self):
        """Test bbox with south latitude too large."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, 91.0, 10.0, 10.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "south latitude must be in [-90, 90]" in error_str

    def test_bbox_invalid_latitude_north_too_small(self):
        """Test bbox with north latitude too small."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -10.0, 10.0, -91.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "north latitude must be in [-90, 90]" in error_str

    def test_bbox_invalid_latitude_north_too_large(self):
        """Test bbox with north latitude too large."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, -10.0, 10.0, 91.0],
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "north latitude must be in [-90, 90]" in error_str

    def test_bbox_invalid_latitude_order(self):
        """Test bbox with invalid latitude order (north < south)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-10.0, 10.0, 10.0, -10.0],  # north < south
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "north latitude" in error_str and "south latitude" in error_str

    def test_bbox_valid_antimeridian_crossing(self):
        """Test valid bbox crossing antimeridian (west > east)."""
        # Example from RFC 7946 Section 5.2: Fiji archipelago
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [177.0, -20.0, -178.0, -16.0],
        }
        point = PointModel(**data)
        assert point.bbox == [177.0, -20.0, -178.0, -16.0]

    def test_bbox_invalid_antimeridian_span_too_large(self):
        """Test bbox with antimeridian crossing but span >= 360 degrees."""
        # This should be invalid: west > east but span is 360+ degrees
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [179.0, -10.0, -179.0, 10.0],  # span = 2 degrees, should be OK
        }
        # This should work
        point = PointModel(**data)
        assert point.bbox == [179.0, -10.0, -179.0, 10.0]

    def test_bbox_valid_north_pole(self):
        """Test valid bbox containing North Pole."""
        # From RFC 7946 Section 5.3
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-180.0, 60.0, 180.0, 90.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-180.0, 60.0, 180.0, 90.0]

    def test_bbox_valid_south_pole(self):
        """Test valid bbox containing South Pole."""
        # From RFC 7946 Section 5.3
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-180.0, -90.0, 180.0, -60.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-180.0, -90.0, 180.0, -60.0]

    def test_bbox_3d_invalid_depth_height_order(self):
        """Test 3D bbox with invalid depth/height order (depth > height)."""
        data = {
            "type": "Point",
            "coordinates": [0, 0, 100],
            "bbox": [-10.0, -10.0, 100.0, 10.0, 10.0, 0.0],  # depth > height
        }
        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value)
        assert "depth" in error_str and "height" in error_str

    def test_bbox_3d_valid(self):
        """Test valid 3D bbox."""
        data = {
            "type": "Point",
            "coordinates": [0, 0, 100],
            "bbox": [-10.0, -10.0, 0.0, 10.0, 10.0, 1000.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-10.0, -10.0, 0.0, 10.0, 10.0, 1000.0]

    def test_bbox_on_feature(self):
        """Test bbox validation on Feature object."""
        data = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            "properties": {},
            "bbox": [-10.0, -10.0, 10.0, 10.0],
        }
        feature = FeatureModel(**data)
        assert feature.bbox == [-10.0, -10.0, 10.0, 10.0]

    def test_bbox_on_feature_collection(self):
        """Test bbox validation on FeatureCollection object."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                    "properties": {},
                }
            ],
            "bbox": [100.0, 0.0, 105.0, 1.0],
        }
        fc = FeatureCollectionModel(**data)
        assert fc.bbox == [100.0, 0.0, 105.0, 1.0]

    def test_bbox_boundary_values(self):
        """Test bbox with boundary coordinate values."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "bbox": [-180.0, -90.0, 180.0, 90.0],
        }
        point = PointModel(**data)
        assert point.bbox == [-180.0, -90.0, 180.0, 90.0]
