"""Tests for GeometryCollectionModel."""

import copy

import pytest
from pydantic import ValidationError

from pydantic_geojson import GeometryCollectionModel
from pydantic_geojson.object_type import GEOMETRY_COLLECTION


class TestGeometryCollectionModel:
    """Test suite for GeometryCollectionModel validation and serialization."""

    def test_valid_geometry_collection_creation(self, valid_geometry_collection_data):
        """Test creating a valid GeometryCollection model."""
        gc_model = GeometryCollectionModel(**valid_geometry_collection_data)

        assert gc_model.type == GEOMETRY_COLLECTION
        assert gc_model.type == valid_geometry_collection_data["type"]
        assert len(gc_model.geometries) == len(valid_geometry_collection_data["geometries"])

        for idx, geometry in enumerate(gc_model.geometries):
            expected_geometry = valid_geometry_collection_data["geometries"][idx]
            assert geometry.type == expected_geometry["type"]

    def test_geometry_collection_empty(self, valid_geometry_collection_empty):
        """Test GeometryCollection with empty geometries list."""
        gc_model = GeometryCollectionModel(**valid_geometry_collection_empty)

        assert gc_model.type == GEOMETRY_COLLECTION
        assert len(gc_model.geometries) == 0

    def test_geometry_collection_nested(self, nested_geometry_collection_data):
        """Test GeometryCollection containing another GeometryCollection.

        Note: While nested geometry collections are not recommended by RFC 7946,
        the library should still validate them correctly.
        """
        gc_model = GeometryCollectionModel(**nested_geometry_collection_data)

        assert gc_model.type == GEOMETRY_COLLECTION
        # Check that nested GeometryCollection is present
        assert any(isinstance(g, GeometryCollectionModel) for g in gc_model.geometries)

    def test_geometry_collection_invalid_type(self, geometry_collection_bad_type):
        """Test GeometryCollection with invalid type field."""
        with pytest.raises(ValidationError) as exc_info:
            GeometryCollectionModel(**geometry_collection_bad_type)

        assert "Input should be 'GeometryCollection'" in str(exc_info.value)

    def test_geometry_collection_serialization(self, valid_geometry_collection_data):
        """Test GeometryCollection model serialization to dict."""
        gc_model = GeometryCollectionModel(**valid_geometry_collection_data)
        serialized = gc_model.model_dump(mode="json")

        assert serialized["type"] == "GeometryCollection"
        assert len(serialized["geometries"]) == len(valid_geometry_collection_data["geometries"])
        assert "bbox" in serialized

        # Verify geometries are serialized correctly
        for idx, geometry in enumerate(serialized["geometries"]):
            expected = valid_geometry_collection_data["geometries"][idx]
            assert geometry["type"] == expected["type"]

    def test_geometry_collection_json_serialization(self, valid_geometry_collection_data):
        """Test GeometryCollection model JSON serialization."""
        gc_model = GeometryCollectionModel(**valid_geometry_collection_data)
        json_str = gc_model.model_dump_json()

        assert '"type":"GeometryCollection"' in json_str
        assert '"geometries"' in json_str

    def test_geometry_collection_from_json(self, valid_geometry_collection_data):
        """Test creating GeometryCollection from JSON string."""
        import json

        json_str = json.dumps(valid_geometry_collection_data)
        gc_model = GeometryCollectionModel.model_validate_json(json_str)

        assert gc_model.type == GEOMETRY_COLLECTION
        assert len(gc_model.geometries) == len(valid_geometry_collection_data["geometries"])

    def test_geometry_collection_with_bbox(self, valid_geometry_collection_data, bbox_2d):
        """Test GeometryCollection with bounding box."""
        data = copy.deepcopy(valid_geometry_collection_data)
        data["bbox"] = bbox_2d
        gc_model = GeometryCollectionModel(**data)

        assert gc_model.bbox == bbox_2d
        assert gc_model.type == GEOMETRY_COLLECTION

    def test_geometry_collection_with_all_geometry_types(self):
        """Test GeometryCollection containing all geometry types."""
        data = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [-105.01621, 39.57422]},
                {
                    "type": "MultiPoint",
                    "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
                },
                {
                    "type": "LineString",
                    "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
                },
                {
                    "type": "MultiLineString",
                    "coordinates": [[[-99.113159, 38.869651], [-99.0802, 38.85682]]],
                },
                {
                    "type": "Polygon",
                    "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
                },
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]],
                },
            ],
        }

        gc_model = GeometryCollectionModel(**data)
        assert gc_model.type == GEOMETRY_COLLECTION
        assert len(gc_model.geometries) == 6
        assert gc_model.geometries[0].type == "Point"
        assert gc_model.geometries[1].type == "MultiPoint"
        assert gc_model.geometries[2].type == "LineString"
        assert gc_model.geometries[3].type == "MultiLineString"
        assert gc_model.geometries[4].type == "Polygon"
        assert gc_model.geometries[5].type == "MultiPolygon"
