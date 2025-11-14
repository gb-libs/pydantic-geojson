"""Tests for FeatureCollectionModel."""

import copy

import pytest
from pydantic import ValidationError

from pydantic_geojson import FeatureCollectionModel
from pydantic_geojson.object_type import FEATURE_COLLECTION


class TestFeatureCollectionModel:
    """Test suite for FeatureCollectionModel validation and serialization."""

    def test_valid_feature_collection_creation(self, valid_feature_collection_data):
        """Test creating a valid FeatureCollection model."""
        fc_model = FeatureCollectionModel(**valid_feature_collection_data)

        assert fc_model.type == FEATURE_COLLECTION
        assert fc_model.type == valid_feature_collection_data["type"]
        assert len(fc_model.features) == len(valid_feature_collection_data["features"])

        for idx, feature in enumerate(fc_model.features):
            assert feature.type == "Feature"
            expected_feature = valid_feature_collection_data["features"][idx]
            assert feature.geometry is not None
            assert feature.geometry.type == expected_feature["geometry"]["type"]

    def test_feature_collection_empty(self, valid_feature_collection_empty):
        """Test FeatureCollection with empty features list."""
        fc_model = FeatureCollectionModel(**valid_feature_collection_empty)

        assert fc_model.type == FEATURE_COLLECTION
        assert len(fc_model.features) == 0

    def test_feature_collection_invalid_type(self, invalid_feature_collection_wrong_type):
        """Test FeatureCollection with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            FeatureCollectionModel(**invalid_feature_collection_wrong_type)

        assert "Input should be 'FeatureCollection'" in str(exc_info.value)

    def test_feature_collection_serialization(self, valid_feature_collection_data):
        """Test FeatureCollection model serialization to dict."""
        fc_model = FeatureCollectionModel(**valid_feature_collection_data)
        serialized = fc_model.model_dump(mode="json")

        assert serialized["type"] == "FeatureCollection"
        assert len(serialized["features"]) == len(valid_feature_collection_data["features"])
        assert "bbox" in serialized

        # Verify features are serialized correctly
        for idx, feature in enumerate(serialized["features"]):
            assert feature["type"] == "Feature"
            expected = valid_feature_collection_data["features"][idx]
            assert feature["geometry"]["type"] == expected["geometry"]["type"]

    def test_feature_collection_json_serialization(self, valid_feature_collection_data):
        """Test FeatureCollection model JSON serialization."""
        fc_model = FeatureCollectionModel(**valid_feature_collection_data)
        json_str = fc_model.model_dump_json()

        assert '"type":"FeatureCollection"' in json_str
        assert '"features"' in json_str

    def test_feature_collection_from_json(self, valid_feature_collection_data):
        """Test creating FeatureCollection from JSON string."""
        import json

        json_str = json.dumps(valid_feature_collection_data)
        fc_model = FeatureCollectionModel.model_validate_json(json_str)

        assert fc_model.type == FEATURE_COLLECTION
        assert len(fc_model.features) == len(valid_feature_collection_data["features"])

    def test_feature_collection_with_bbox(self, valid_feature_collection_data, bbox_2d):
        """Test FeatureCollection with bounding box."""
        data = copy.deepcopy(valid_feature_collection_data)
        data["bbox"] = bbox_2d
        fc_model = FeatureCollectionModel(**data)

        assert fc_model.bbox == bbox_2d
        assert fc_model.type == FEATURE_COLLECTION

    def test_feature_collection_with_multiple_geometry_types(self):
        """Test FeatureCollection with features containing different geometry types."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]},
                    "properties": {},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
                    },
                    "properties": {},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
                    },
                    "properties": {},
                },
            ],
        }

        fc_model = FeatureCollectionModel(**data)
        assert fc_model.type == FEATURE_COLLECTION
        assert len(fc_model.features) == 3
        assert fc_model.features[0].geometry is not None
        assert fc_model.features[0].geometry.type == "Point"
        assert fc_model.features[1].geometry is not None
        assert fc_model.features[1].geometry.type == "LineString"
        assert fc_model.features[2].geometry is not None
        assert fc_model.features[2].geometry.type == "Polygon"
