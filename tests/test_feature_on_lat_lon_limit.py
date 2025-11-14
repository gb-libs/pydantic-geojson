"""Tests for coordinate boundary validation across geometry types."""

import pytest
from pydantic import ValidationError

from pydantic_geojson import LineStringModel, PointModel, PolygonModel


class TestCoordinateBoundaries:
    """Test suite for coordinate boundary validation in various geometry types."""

    @pytest.mark.parametrize(
        "geometry_type,data",
        [
            (
                "Point",
                {"type": "Point", "coordinates": [-180.0, 90.0]},
            ),
            (
                "LineString",
                {
                    "type": "LineString",
                    "coordinates": [[-180.0, -90.0], [180.0, 90.0]],
                },
            ),
            (
                "Polygon",
                {
                    "type": "Polygon",
                    "coordinates": [
                        [[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0], [-10.0, -10.0]]
                    ],
                },
            ),
        ],
    )
    def test_valid_boundary_coordinates(self, geometry_type, data):
        """Test that geometries accept coordinates at valid boundaries."""
        models = {
            "Point": PointModel,
            "LineString": LineStringModel,
            "Polygon": PolygonModel,
        }

        model_class = models[geometry_type]
        model = model_class(**data)

        assert model.type == data["type"]

    @pytest.mark.parametrize(
        "invalid_coords,expected_error",
        [
            ([-181, 90], "longitude"),  # lon too small
            ([181, 90], "longitude"),  # lon too large
            ([-180, -91], "latitude"),  # lat too small
            ([180, 91], "latitude"),  # lat too large
        ],
    )
    def test_point_invalid_coordinate_ranges(self, invalid_coords, expected_error):
        """Test Point with invalid coordinate ranges."""
        data = {"type": "Point", "coordinates": invalid_coords}

        with pytest.raises(ValidationError) as exc_info:
            PointModel(**data)

        error_str = str(exc_info.value).lower()
        assert (
            expected_error in error_str
            or "greater than or equal to" in error_str
            or "less than or equal to" in error_str
        )

    @pytest.mark.parametrize(
        "invalid_coords",
        [
            [[-181, 0], [0, 0]],  # lon too small in first coord
            [[0, 0], [181, 0]],  # lon too large in second coord
            [[0, -91], [0, 0]],  # lat too small in first coord
            [[0, 0], [0, 91]],  # lat too large in second coord
        ],
    )
    def test_linestring_invalid_coordinate_ranges(self, invalid_coords):
        """Test LineString with invalid coordinate ranges."""
        data = {"type": "LineString", "coordinates": invalid_coords}

        with pytest.raises(ValidationError):
            LineStringModel(**data)

    @pytest.mark.parametrize(
        "invalid_coords",
        [
            [[[-181, 0], [0, 0], [0, 0], [-181, 0]]],  # lon too small
            [[[0, -91], [0, 0], [0, 0], [0, -91]]],  # lat too small
            [[[0, 0], [181, 0], [181, 0], [0, 0]]],  # lon too large
            [[[0, 0], [0, 91], [0, 91], [0, 0]]],  # lat too large
        ],
    )
    def test_polygon_invalid_coordinate_ranges(self, invalid_coords):
        """Test Polygon with invalid coordinate ranges."""
        data = {"type": "Polygon", "coordinates": invalid_coords}

        with pytest.raises(ValidationError):
            PolygonModel(**data)

    def test_boundary_edge_cases(self):
        """Test specific boundary edge cases."""
        # Test exact boundaries
        valid_cases = [
            (PointModel, {"type": "Point", "coordinates": [-180, -90]}),
            (PointModel, {"type": "Point", "coordinates": [180, 90]}),
            (PointModel, {"type": "Point", "coordinates": [-180, 90]}),
            (PointModel, {"type": "Point", "coordinates": [180, -90]}),
            (PointModel, {"type": "Point", "coordinates": [0, 0]}),
        ]

        for model_class, data in valid_cases:
            model = model_class(**data)
            assert model.type == data["type"]

        # Test just outside boundaries
        invalid_cases = [
            (PointModel, {"type": "Point", "coordinates": [-180.0001, 0]}),
            (PointModel, {"type": "Point", "coordinates": [180.0001, 0]}),
            (PointModel, {"type": "Point", "coordinates": [0, -90.0001]}),
            (PointModel, {"type": "Point", "coordinates": [0, 90.0001]}),
        ]

        for model_class, data in invalid_cases:
            with pytest.raises(ValidationError):
                model_class(**data)
