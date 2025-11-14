"""Utility functions for tests."""

from pydantic_geojson._base import Coordinates


def assert_coordinates_equal(coord: Coordinates, expected: list[float]) -> None:
    """Assert that a Coordinates object matches expected [lon, lat] or [lon, lat, alt]."""
    assert coord.lon == expected[0]
    assert coord.lat == expected[1]
    if len(expected) > 2:
        assert coord.alt == expected[2]
    else:
        assert coord.alt is None
