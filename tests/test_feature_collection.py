from pydantic_geojson import FeatureCollectionModel
from pydantic_geojson.object_type import FEATURE_COLLECTION

data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-80.870885, 35.215151]
            },
            "properties": {}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-80.724878, 35.265454],
                        [-80.722646, 35.260338],
                        [-80.720329, 35.260618],
                        [-80.704793, 35.268397],
                        [-80.724878, 35.265454]
                    ]
                ]
            },
            "properties": {}
        }
    ]
}


class TestFeatureCollectionModel:
    def test_loads_model(self):
        fc_model = FeatureCollectionModel(**data)
        features = fc_model.features

        for fc_key, fc_item in enumerate(features):
            assert fc_item.type == data['features'][fc_key]['type']

        assert fc_model.type == data['type']

    def test_model_type(self):
        fc_model = FeatureCollectionModel(**data)
        assert fc_model.type == FEATURE_COLLECTION
