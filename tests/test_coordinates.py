import pytest
from pydantic_geojson._base import Coordinates


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
        ),  # Altiture not specified for coord_one
        (Coordinates(1, 0, None), Coordinates(0, 0, None), False),  # Latitude not equal
        (
            Coordinates(0, 1, None),
            Coordinates(0, 0, None),
            False,
        ),  # Longitude not equal
        (
            Coordinates(0, 0, 1),
            Coordinates(0, 0, 0),
            False,
        ),  # Altitude specified but not equal
        (
            Coordinates(180, 0, None),
            Coordinates(-180, 0, None),
            False,
        ),  # Plus and minus 180 latitude are not considered equal
    ],
)
def test_coordinate_equality(coord_one, coord_two, is_equal):
    assert (
        coord_one == coord_two
    ) == is_equal, f"Result of {coord_one} == {coord_two} should be {is_equal}"
