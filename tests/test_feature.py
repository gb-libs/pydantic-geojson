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
                [-80.724878, 35.265454],
            ]
        ],
    },
    "properties": {
        "property1": "a string value",
        "property2": 0.666,
        "property3": 1,
        "property4": True,
        "property5": True,
        "property6": None,
    },
}


class TestFeatureModel:
    def test_geometry_model_type(self):
        f_model = FeatureModel(**data)
        assert f_model.geometry.type == data["geometry"]["type"]
        assert f_model.type == data["type"]

    def test_model_type(self):
        f_model = FeatureModel(**data)
        assert f_model.type == FEATURE

    def test_model_properties(self):
        f_model = FeatureModel(**data)
        assert f_model.type == FEATURE
        assert isinstance(f_model.properties, dict)
        assert f_model.properties == data["properties"]

        assert f_model.type == FEATURE

    def test_model_properties_with_validate(self):
        f_model = FeatureModel.model_validate(data)
        assert isinstance(f_model.properties, dict)
        assert f_model.properties == data["properties"]
