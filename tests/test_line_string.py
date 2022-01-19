from pydantic_geojson import LineStringModel
from pydantic_geojson.object_type import LINE_STRING

data = {
    "type": "LineString",
    "coordinates": [
        [-99.113159, 38.869651],
        [-99.0802, 38.85682],
        [-98.822021, 38.85682],
        [-98.448486, 38.848264]
    ]
}


class TestLineStringModel:
    def test_loads_model(self):
        ls_model = LineStringModel(**data)
        coordinates = ls_model.coordinates

        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert data['coordinates'][lsi_key] == [lon, lat]

        assert ls_model.type == data['type']

    def test_model_type(self):
        ls_model = LineStringModel(**data)
        assert ls_model.type == LINE_STRING
