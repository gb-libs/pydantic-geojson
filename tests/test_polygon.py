from pydantic_geojson import PolygonModel
from pydantic_geojson.object_type import POLYGON

data = {
    'type': 'Polygon',
    'coordinates': [
        [
            [100, 0],
            [101, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}


class TestPolygonModel:
    def test_loads_model(self):
        p_model = PolygonModel(**data)
        coordinates = p_model.coordinates

        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate.lon, p_coordinate.lat
                assert data['coordinates'][pi_key][pl_key] == [lon, lat]

        assert p_model.type == data['type']

    def test_model_type(self):
        p_model = PolygonModel(**data)
        assert p_model.type == POLYGON
