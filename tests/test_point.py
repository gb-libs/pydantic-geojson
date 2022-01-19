from pydantic_geojson import PointModel
from pydantic_geojson.object_type import POINT

data = {
    'type': 'Point',
    'coordinates': [-105.01621, 39.57422]
}


class TestPointModel:
    def test_loads_model(self):
        p_model = PointModel(**data)
        coordinates = p_model.coordinates

        lon, lat = coordinates.lon, coordinates.lat
        assert data['coordinates'] == [lon, lat]

        assert p_model.type == data['type']

    def test_model_type(self):
        p_model = PointModel(**data)
        assert p_model.type == POINT
