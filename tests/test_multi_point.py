from pydantic import ValidationError
from pydantic_geojson import MultiPointModel
from pydantic_geojson.object_type import MULTI_POINT
import pytest


@pytest.fixture
def valid_multi_point_data():
    return {
        "type": "MultiPoint",
        "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
    }


@pytest.fixture
def invalid_bad_multi_point_type():
    return {
        "type": "LineString",
        "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
    }


class TestMultiPointModel:
    def test_loads_model(self, valid_multi_point_data):
        mp_model = MultiPointModel(**valid_multi_point_data)
        coordinates = mp_model.coordinates

        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item.lon, mp_item.lat
            assert valid_multi_point_data["coordinates"][mpi_key] == [lon, lat]

        assert mp_model.type == valid_multi_point_data["type"]

    def test_model_type(self, valid_multi_point_data):
        mp_model = MultiPointModel(**valid_multi_point_data)
        assert mp_model.type == MULTI_POINT

    def test_valid_type_required(self, invalid_bad_multi_point_type):
        with pytest.raises(ValidationError) as err:
            MultiPointModel(**invalid_bad_multi_point_type)

        assert "Input should be 'MultiPoint'" in str(
            err.value
        ), "Should error from not having literal MultiPoint"
