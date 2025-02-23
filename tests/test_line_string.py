import pytest
from pydantic import ValidationError
from pydantic_geojson import LineStringModel
from pydantic_geojson.object_type import LINE_STRING


@pytest.fixture
def valid_linestring_data():
    return {
        "type": "LineString",
        "coordinates": [
            [-99.113159, 38.869651],
            [-99.0802, 38.85682],
            [-98.822021, 38.85682],
            [-98.448486, 38.848264],
        ],
    }


@pytest.fixture
def invalid_linestring_one_coordinate():
    return {"type": "LineString", "coordinates": [[1, 1]]}


@pytest.fixture
def invalid_linestring_bad_type():
    return {"type": "NotALineString", "coordinates": [[1, 1], [2, 2]]}


class TestLineStringModel:
    def test_loads_model(self, valid_linestring_data):
        ls_model = LineStringModel(**valid_linestring_data)
        coordinates = ls_model.coordinates

        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert valid_linestring_data["coordinates"][lsi_key] == [lon, lat]

        assert ls_model.type == valid_linestring_data["type"]

    def test_model_type(self, valid_linestring_data):
        ls_model = LineStringModel(**valid_linestring_data)
        assert ls_model.type == LINE_STRING

    def test_linestring_must_have_two_coords(self, invalid_linestring_one_coordinate):
        with pytest.raises(ValidationError) as err:
            LineStringModel(**invalid_linestring_one_coordinate)

        assert "too_short" in str(err.value), "Should be a too_short error"

    def test_linestring_type(self, invalid_linestring_bad_type):
        with pytest.raises(ValidationError) as err:
            LineStringModel(**invalid_linestring_bad_type)

        assert "Input should be 'LineString'" in str(
            err.value
        ), "Should error from not having literal LineString"
