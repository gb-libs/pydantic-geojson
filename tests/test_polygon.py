import pytest
from pydantic import ValidationError
from pydantic_geojson import PolygonModel
from pydantic_geojson.object_type import POLYGON


@pytest.fixture
def valid_polygon_data():
    return {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
    }


@pytest.fixture
def invalid_polygon_data_no_loop():
    return {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [101, 1], [101, 1]]],
    }


@pytest.fixture
def invalid_polygon_data_too_few_points():
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [100, 0],
                [101, 0],
                [100, 0],
            ]
        ],
    }


@pytest.fixture
def invalid_polygon_data_bad_type():
    return {
        "type": "MultiPolygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
    }


class TestPolygonModel:
    def test_loads_model(self, valid_polygon_data):
        p_model = PolygonModel(**valid_polygon_data)
        coordinates = p_model.coordinates

        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate.lon, p_coordinate.lat
                assert valid_polygon_data["coordinates"][pi_key][pl_key] == [lon, lat]

        assert p_model.type == valid_polygon_data["type"]

    def test_model_type(self, valid_polygon_data):
        p_model = PolygonModel(**valid_polygon_data)
        assert p_model.type == POLYGON

    def test_invalid_polygon_bad_type(self, invalid_polygon_data_bad_type):
        with pytest.raises(ValidationError) as err:
            PolygonModel(**invalid_polygon_data_bad_type)

        assert "Input should be 'Polygon'" in str(
            err.value
        ), "Should error from not having literal Polygon"

    def test_invalid_polygon_start_and_end_must_equal(
        self, invalid_polygon_data_no_loop
    ):
        with pytest.raises(ValidationError) as err:
            PolygonModel(**invalid_polygon_data_no_loop)

        assert "Linear Rings must start and end at the same coordinate" in str(
            err.value
        )

    def test_invalid_polygon_length_ge_4(self, invalid_polygon_data_too_few_points):
        with pytest.raises(ValidationError) as err:
            PolygonModel(**invalid_polygon_data_too_few_points)

        assert "Linear Ring length must be >=4, not 3" in str(err.value)
