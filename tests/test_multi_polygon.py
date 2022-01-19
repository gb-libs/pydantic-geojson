from pydantic_geojson import MultiPolygonModel
from pydantic_geojson.object_type import MULTI_POLYGON

data = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [107, 7],
                [108, 7],
                [108, 8],
                [107, 8],
                [107, 7]
            ]
        ],
        [
            [
                [100, 0],
                [101, 0],
                [101, 1],
                [100, 1],
                [100, 0]
            ]
        ]
    ]
}


class TestMultiPolygonModel:
    def test_loads_model(self):
        mp_model = MultiPolygonModel(**data)
        coordinates = mp_model.coordinates

        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate.lon, mp_coordinate.lat
                    assert data['coordinates'][mp_list_key][mp_item_key][
                               mpl_key] == [lon, lat]

        assert mp_model.type == data['type']

    def test_model_type(self):
        mp_model = MultiPolygonModel(**data)
        assert mp_model.type == MULTI_POLYGON
