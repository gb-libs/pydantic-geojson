from pydantic_geojson import FeatureModel
from pydantic_geojson.object_type import FEATURE

data = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-80.724878, 35.265454],
                [-80.722646, 35.260338],
                [-80.720329, 35.260618],
                [-80.71681, 35.255361],
                [-80.704793, 35.268397],
                [-82.715179, 35.267696],
                [-80.721359, 35.267276],
                [-80.724878, 35.265454]
            ]
        ]
    },
    "properties": {}
}


class TestFeatureModel:

    def test_geometry_model_type(self):
        f_model = FeatureModel(**data)
        assert f_model.geometry.type == data['geometry']['type']
        assert f_model.type == data['type']

    def test_model_type(self):
        f_model = FeatureModel(**data)
        assert f_model.type == FEATURE
