from pydantic import ValidationError
from pydantic_geojson import FeatureCollectionModel
from pydantic_geojson.object_type import FEATURE_COLLECTION
import pytest

@pytest.fixture
def valid_feature_collection_data():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-80.870885, 35.215151]},
                "properties": {},
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
                            [-80.724878, 35.265454],
                        ]
                    ],
                },
                "properties": {},
            },
        ],
    }


class TestFeatureCollectionModel:
    def test_loads_model(self, valid_feature_collection_data):
        fc_model = FeatureCollectionModel(**valid_feature_collection_data)
        features = fc_model.features

        for fc_key, fc_item in enumerate(features):
            assert fc_item.type == valid_feature_collection_data["features"][fc_key]["type"]

        assert fc_model.type == valid_feature_collection_data["type"]

    def test_model_type(self, valid_feature_collection_data):
        fc_model = FeatureCollectionModel(**valid_feature_collection_data)
        assert fc_model.type == FEATURE_COLLECTION

    def test_correct_feature_type_required(self, valid_feature_collection_data):
        invalid_type = "Geometry Collection"
        valid_feature_collection_data["type"] = invalid_type
        with pytest.raises(ValidationError):
            FeatureCollectionModel(**valid_feature_collection_data)
