from pydantic import ValidationError
import pytest
from pydantic_geojson import PointModel
from pydantic_geojson.object_type import POINT


@pytest.fixture
def valid_point_data():
    return {"type": "Point", "coordinates": [-105.01621, 39.57422]}


@pytest.fixture
def invalid_point_bad_type():
    return {"type": "MultiPoint", "coordinates": [-105.01621, 39.57422]}


class TestPointModel:
    def test_loads_model(self, valid_point_data):
        p_model = PointModel(**valid_point_data)
        coordinates = p_model.coordinates

        lon, lat = coordinates.lon, coordinates.lat
        assert valid_point_data["coordinates"] == [lon, lat]

        assert p_model.type == valid_point_data["type"]

    def test_model_type(self, valid_point_data):
        p_model = PointModel(**valid_point_data)
        assert p_model.type == POINT

    def test_model_type_required(self, invalid_point_bad_type):
        with pytest.raises(ValidationError) as err:
            PointModel(**invalid_point_bad_type)

        assert "Input should be 'Point'" in str(
            err.value
        ), "Should error from not having literal Point"
