import pytest
from pydantic import ValidationError
from pydantic_geojson import FeatureModel
from pydantic_geojson.object_type import FEATURE


@pytest.fixture()
def valid_feature_all_fields():
    return {
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
        "id": "TestFeature",
    }


@pytest.fixture
def valid_feature_type_only():
    return {"type": "Feature", "geometry": None, "properties": None, "id": None}


@pytest.fixture
def invalid_feature_wrong_type(valid_feature_all_fields):
    wrong_type = "Point"
    return {**valid_feature_all_fields, "type": wrong_type}


class TestFeatureModel:
    def test_geometry_model_type(self, valid_feature_all_fields):
        f_model = FeatureModel(**valid_feature_all_fields)
        assert f_model.geometry.type == valid_feature_all_fields["geometry"]["type"]
        assert f_model.type == valid_feature_all_fields["type"]

    def test_model_type(self, valid_feature_all_fields):
        f_model = FeatureModel(**valid_feature_all_fields)
        assert f_model.type == FEATURE

    def test_model_properties(self, valid_feature_all_fields):
        f_model = FeatureModel(**valid_feature_all_fields)
        assert f_model.type == FEATURE
        assert isinstance(f_model.properties, dict)
        assert f_model.properties == valid_feature_all_fields["properties"]

        assert f_model.type == FEATURE

    def test_model_properties_with_validate(self, valid_feature_all_fields):
        f_model = FeatureModel.model_validate(valid_feature_all_fields)
        assert isinstance(f_model.properties, dict)
        assert f_model.properties == valid_feature_all_fields["properties"]

    def test_model_nullable_properties(self, valid_feature_type_only):
        f_model = FeatureModel(**valid_feature_type_only)
        assert f_model.type == valid_feature_type_only["type"]

    def test_invalid_type_not_accepted(self, invalid_feature_wrong_type):
        with pytest.raises(ValidationError) as err:
            FeatureModel(**invalid_feature_wrong_type)

        assert "Input should be 'Feature'" in str(
            err.value
        ), "Should error from not having literal Feature"
