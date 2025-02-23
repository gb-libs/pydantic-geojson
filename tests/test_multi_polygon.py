import pytest
from pydantic import ValidationError
from pydantic_geojson import MultiPolygonModel
from pydantic_geojson.object_type import MULTI_POLYGON


@pytest.fixture
def valid_multi_polygon():
    return {
        "type": "MultiPolygon",
        "coordinates": [
            [[[107, 7], [108, 7], [108, 8], [107, 8], [107, 7]]],
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
        ],
    }


@pytest.fixture
def invalid_multi_polygon_wrong_type():
    return {
        "type": "MultiLineString",
        "coordinates": [
            [[[107, 7], [108, 7], [108, 8], [107, 8], [107, 7]]],
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
        ],
    }


@pytest.fixture
def invalid_multi_polygon_linear_ring_validation():
    return {
        "type": "MultiLineString",
        "coordinates": [
            [[[107, 7], [108, 7]]],  # too short
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 90]]],  # no loop
        ],
    }


class TestMultiPolygonModel:
    def test_loads_model(self, valid_multi_polygon):
        mp_model = MultiPolygonModel(**valid_multi_polygon)
        coordinates = mp_model.coordinates

        for mp_l_key, mp_l in enumerate(coordinates):
            for mp_i_key, mp_i in enumerate(mp_l):
                for mpl_key, mp_coordinate in enumerate(mp_i):
                    lon, lat = mp_coordinate.lon, mp_coordinate.lat
                    assert valid_multi_polygon["coordinates"][mp_l_key][mp_i_key][
                        mpl_key
                    ] == [
                        lon,
                        lat,
                    ]

        assert mp_model.type == valid_multi_polygon["type"]

    def test_model_type(self, valid_multi_polygon):
        mp_model = MultiPolygonModel(**valid_multi_polygon)
        assert mp_model.type == MULTI_POLYGON

    def test_invalid_model_type(self, invalid_multi_polygon_wrong_type):
        with pytest.raises(ValidationError) as err:
            MultiPolygonModel(**invalid_multi_polygon_wrong_type)

        assert "Input should be 'MultiPolygon'" in str(
            err.value
        ), "Should error from not having literal MultiPolygon"

    def test_invalid_model_bad_linear_ring_valisation(
        self, invalid_multi_polygon_linear_ring_validation
    ):
        with pytest.raises(ValidationError) as err:
            MultiPolygonModel(**invalid_multi_polygon_linear_ring_validation)

        assert "Linear Ring length must be >=4, not 2" in str(err.value)

        assert "Linear Rings must start and end at the same coordinate" in str(
            err.value
        )
