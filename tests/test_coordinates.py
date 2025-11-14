"""Tests for Coordinates class."""

import pytest

from pydantic_geojson._base import Coordinates


class TestCoordinates:
    """Test suite for Coordinates validation and equality."""

    @pytest.mark.parametrize(
        "coord_one,coord_two,is_equal",
        [
            (
                Coordinates(0, 0, None),
                Coordinates(0, 0, None),
                True,
            ),  # None and None are equivalent
            (
                Coordinates(0, 0, 0),
                Coordinates(0, 0, 0),
                True,
            ),  # Zero and Zero are equivalent
            (
                Coordinates(0, 0, None),
                Coordinates(0, 0, 0),
                False,
            ),  # Altitude not specified for coord_one
            (
                Coordinates(1, 0, None),
                Coordinates(0, 0, None),
                False,
            ),  # Longitude not equal
            (
                Coordinates(0, 1, None),
                Coordinates(0, 0, None),
                False,
            ),  # Latitude not equal
            (
                Coordinates(0, 0, 1),
                Coordinates(0, 0, 0),
                False,
            ),  # Altitude specified but not equal
            (
                Coordinates(180, 0, None),
                Coordinates(-180, 0, None),
                False,
            ),  # Plus and minus 180 longitude are not considered equal
            (
                Coordinates(0, 90, None),
                Coordinates(0, -90, None),
                False,
            ),  # Plus and minus 90 latitude are not considered equal
            (
                Coordinates(0.1, 0.1, None),
                Coordinates(0.1, 0.1, None),
                True,
            ),  # Floating point equality
            (
                Coordinates(0.1 + 1e-10, 0.1, None),
                Coordinates(0.1, 0.1, None),
                True,
            ),  # Floating point precision tolerance
        ],
    )
    def test_coordinate_equality(self, coord_one, coord_two, is_equal):
        """Test coordinate equality comparison."""
        assert (coord_one == coord_two) == is_equal, (
            f"Result of {coord_one} == {coord_two} should be {is_equal}"
        )

    @pytest.mark.parametrize(
        "lon,lat,alt",
        [
            (0, 0, None),
            (0, 0, 100.5),
            (10.5, 20.3, 100.0),
        ],
    )
    def test_coordinates_creation(self, lon, lat, alt):
        """Test creating coordinates with different dimensions."""
        coord = Coordinates(lon, lat, alt)
        assert coord.lon == lon
        assert coord.lat == lat
        assert coord.alt == alt

    @pytest.mark.parametrize(
        "lon,lat",
        [
            (-180, -90),
            (-180, 90),
            (180, -90),
            (180, 90),
            (0, -90),
            (0, 90),
            (-180, 0),
            (180, 0),
        ],
    )
    def test_coordinates_boundary_values(self, lon, lat):
        """Test coordinates at boundary values."""
        coord = Coordinates(lon, lat)
        assert coord.lon == lon
        assert coord.lat == lat

    def test_coordinates_repr(self):
        """Test coordinates string representation."""
        coord = Coordinates(10.5, 20.3, 100.0)
        repr_str = repr(coord)
        assert "10.5" in repr_str
        assert "20.3" in repr_str
        assert "100.0" in repr_str

    def test_coordinates_hashable(self):
        """Test that Coordinates can be used in sets/dicts."""
        coord1 = Coordinates(0, 0)
        coord2 = Coordinates(0, 0)
        coord3 = Coordinates(1, 1)

        # Coordinates are NamedTuple, so they should be hashable
        coord_set = {coord1, coord2, coord3}
        # coord1 and coord2 are equal, so set should have 2 items
        assert len(coord_set) == 2
