from pydantic_geojson import MultiPointModel
from pydantic_geojson.object_type import MULTI_POINT

data = {
    "type": "MultiPoint",
    "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
}


class TestMultiPointModel:
    def test_loads_model(self):
        mp_model = MultiPointModel(**data)
        coordinates = mp_model.coordinates

        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item.lon, mp_item.lat
            assert data["coordinates"][mpi_key] == [lon, lat]

        assert mp_model.type == data["type"]

    def test_model_type(self):
        mp_model = MultiPointModel(**data)
        assert mp_model.type == MULTI_POINT
