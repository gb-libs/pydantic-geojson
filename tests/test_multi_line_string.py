from pydantic_geojson import MultiLineStringModel
from pydantic_geojson.object_type import MULTI_LINE_STRING

data = {
    "type": "MultiLineString",
    "coordinates": [
        [[-105.019898, 39.574997], [-105.019598, 39.574898], [-105.019061, 39.574782]],
        [
            [-105.017173, 39.574402],
            [-105.01698, 39.574385],
            [-105.016636, 39.574385],
            [-105.016508, 39.574402],
            [-105.01595, 39.57427],
        ],
        [
            [-105.014276, 39.573972],
            [-105.014126, 39.574038],
            [-105.013825, 39.57417],
            [-105.01331, 39.574452],
        ],
    ],
}


class TestMultiLineStringModel:
    def test_loads_model(self):
        mls_model = MultiLineStringModel(**data)
        coordinates = mls_model.coordinates

        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate.lon, mls_coordinate.lat
                assert data["coordinates"][mlsi_key][mls_key] == [lon, lat]

        assert mls_model.type == data["type"]

    def test_model_type(self):
        mls_model = MultiLineStringModel(**data)
        assert mls_model.type == MULTI_LINE_STRING
