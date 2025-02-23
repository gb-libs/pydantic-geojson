import copy

import pytest
from pydantic import ValidationError
from pydantic_geojson import GeometryCollectionModel
from pydantic_geojson.object_type import GEOMETRY_COLLECTION


@pytest.fixture
def valid_geometry_collection_data():
    return {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [-80.660805, 35.049392]},
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-80.664582, 35.044965],
                        [-80.663874, 35.04428],
                        [-80.662586, 35.04558],
                        [-80.663444, 35.046036],
                        [-80.664582, 35.044965],
                    ]
                ],
            },
            {
                "type": "LineString",
                "coordinates": [
                    [-80.662372, 35.059509],
                    [-80.662693, 35.059263],
                    [-80.662844, 35.05893],
                ],
            },
        ],
    }


@pytest.fixture
def nested_geometry_collection_data(valid_geometry_collection_data):
    nested = copy.deepcopy(valid_geometry_collection_data)
    valid_geometry_collection_data["geometries"].append(nested)
    return valid_geometry_collection_data


@pytest.fixture
def geometry_collection_bad_type(valid_geometry_collection_data):
    invalid_type = "FeatureCollection"
    valid_geometry_collection_data["type"] = invalid_type
    return valid_geometry_collection_data


class TestGeometryCollectionModel:
    def test_loads_model(self, valid_geometry_collection_data):
        gc_model = GeometryCollectionModel(**valid_geometry_collection_data)
        geometries = gc_model.geometries

        for g_key, g_item in enumerate(geometries):
            assert (
                g_item.type
                == valid_geometry_collection_data["geometries"][g_key]["type"]
            )

        assert gc_model.type == valid_geometry_collection_data["type"]

    def test_model_type(self, valid_geometry_collection_data):
        gc_model = GeometryCollectionModel(**valid_geometry_collection_data)
        assert gc_model.type == GEOMETRY_COLLECTION

    def test_nested_geometry_collection_supported(
        self, nested_geometry_collection_data
    ):
        """
        People shouldn't nest geometry collections, but we should support their validation in case.

        https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.8
        """
        gc_model = GeometryCollectionModel(**nested_geometry_collection_data)
        assert any(isinstance(g, GeometryCollectionModel) for g in gc_model.geometries)

    def test_type_must_be_geometry_collection(self, geometry_collection_bad_type):
        with pytest.raises(ValidationError):
            GeometryCollectionModel(**geometry_collection_bad_type)
