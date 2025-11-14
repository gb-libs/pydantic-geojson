"""Shared fixtures and utilities for GeoJSON model tests."""

import copy

import pytest

# ============================================================================
# Coordinate fixtures
# ============================================================================


@pytest.fixture
def sample_coordinate_2d():
    """A simple 2D coordinate (longitude, latitude)."""
    return [-105.01621, 39.57422]


@pytest.fixture
def sample_coordinate_3d():
    """A 3D coordinate with altitude."""
    return [-105.01621, 39.57422, 100.5]


@pytest.fixture
def boundary_coordinates():
    """Coordinates at the boundaries of valid ranges."""
    return {
        "lon_min": [-180, 0],
        "lon_max": [180, 0],
        "lat_min": [0, -90],
        "lat_max": [0, 90],
        "corner_sw": [-180, -90],
        "corner_ne": [180, 90],
        "corner_nw": [-180, 90],
        "corner_se": [180, -90],
    }


@pytest.fixture
def invalid_coordinates():
    """Invalid coordinates outside valid ranges."""
    return {
        "lon_too_small": [-181, 0],
        "lon_too_large": [181, 0],
        "lat_too_small": [0, -91],
        "lat_too_large": [0, 91],
    }


# ============================================================================
# Point fixtures
# ============================================================================


@pytest.fixture
def valid_point_data(sample_coordinate_2d):
    """Valid Point GeoJSON data."""
    return {"type": "Point", "coordinates": sample_coordinate_2d}


@pytest.fixture
def valid_point_3d_data(sample_coordinate_3d):
    """Valid Point GeoJSON data with altitude."""
    return {"type": "Point", "coordinates": sample_coordinate_3d}


@pytest.fixture
def invalid_point_bad_type(sample_coordinate_2d):
    """Invalid Point with wrong type."""
    return {"type": "MultiPoint", "coordinates": sample_coordinate_2d}


# ============================================================================
# LineString fixtures
# ============================================================================


@pytest.fixture
def valid_linestring_data():
    """Valid LineString GeoJSON data."""
    return {
        "type": "LineString",
        "coordinates": [
            [-99.113159, 38.869651],
            [-99.0802, 38.85682],
            [-98.822021, 38.85682],
            [-98.448486, 38.848264],
        ],
    }


@pytest.fixture
def valid_linestring_minimal():
    """Minimal valid LineString (2 coordinates)."""
    return {"type": "LineString", "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]]}


@pytest.fixture
def invalid_linestring_one_coordinate():
    """Invalid LineString with only one coordinate."""
    return {"type": "LineString", "coordinates": [[1, 1]]}


@pytest.fixture
def invalid_linestring_empty():
    """Invalid LineString with no coordinates."""
    return {"type": "LineString", "coordinates": []}


@pytest.fixture
def invalid_linestring_bad_type():
    """Invalid LineString with wrong type."""
    return {"type": "NotALineString", "coordinates": [[1, 1], [2, 2]]}


# ============================================================================
# Polygon fixtures
# ============================================================================


@pytest.fixture
def valid_polygon_data():
    """Valid Polygon GeoJSON data."""
    return {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
    }


@pytest.fixture
def valid_polygon_with_holes():
    """Valid Polygon with interior rings (holes)."""
    return {
        "type": "Polygon",
        "coordinates": [
            [[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]],  # exterior ring
            [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],  # hole
        ],
    }


@pytest.fixture
def invalid_polygon_data_no_loop():
    """Invalid Polygon where first and last coordinates don't match."""
    return {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0.5]]],
    }


@pytest.fixture
def invalid_polygon_data_too_few_points():
    """Invalid Polygon with fewer than 4 points."""
    return {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [100, 0]]],
    }


@pytest.fixture
def invalid_polygon_data_bad_type():
    """Invalid Polygon with wrong type."""
    return {
        "type": "MultiPolygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
    }


# ============================================================================
# MultiPoint fixtures
# ============================================================================


@pytest.fixture
def valid_multi_point_data():
    """Valid MultiPoint GeoJSON data."""
    return {
        "type": "MultiPoint",
        "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
    }


@pytest.fixture
def valid_multi_point_single():
    """Valid MultiPoint with single point."""
    return {"type": "MultiPoint", "coordinates": [[-105.01621, 39.57422]]}


@pytest.fixture
def invalid_bad_multi_point_type():
    """Invalid MultiPoint with wrong type."""
    return {
        "type": "LineString",
        "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
    }


# ============================================================================
# MultiLineString fixtures
# ============================================================================


@pytest.fixture
def valid_multi_line_string_data():
    """Valid MultiLineString GeoJSON data."""
    return {
        "type": "MultiLineString",
        "coordinates": [
            [
                [-105.019898, 39.574997],
                [-105.019598, 39.574898],
                [-105.019061, 39.574782],
            ],
            [
                [-105.017173, 39.574402],
                [-105.01698, 39.574385],
                [-105.016636, 39.574385],
                [-105.016508, 39.574402],
                [-105.01595, 39.57427],
            ],
            [
                [-105.014276, 39.573972],
                [-105.014126, 39.574038],
                [-105.013825, 39.57417],
                [-105.01331, 39.574452],
            ],
        ],
    }


@pytest.fixture
def invalid_multi_line_string_bad_type():
    """Invalid MultiLineString with wrong type."""
    return {
        "type": "LineString",
        "coordinates": [[[1, 1], [2, 2]], [[2, 2], [3, 3]]],
    }


@pytest.fixture
def invalid_multi_line_string_empty():
    """Invalid MultiLineString with empty coordinates."""
    return {"type": "MultiLineString", "coordinates": []}


@pytest.fixture
def invalid_multi_line_string_single_coord():
    """Invalid MultiLineString with LineString having only one coordinate."""
    return {
        "type": "MultiLineString",
        "coordinates": [[[1, 1]]],
    }


# ============================================================================
# MultiPolygon fixtures
# ============================================================================


@pytest.fixture
def valid_multi_polygon():
    """Valid MultiPolygon GeoJSON data."""
    return {
        "type": "MultiPolygon",
        "coordinates": [
            [[[107, 7], [108, 7], [108, 8], [107, 8], [107, 7]]],
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
        ],
    }


@pytest.fixture
def invalid_multi_polygon_wrong_type():
    """Invalid MultiPolygon with wrong type."""
    return {
        "type": "MultiLineString",
        "coordinates": [
            [[[107, 7], [108, 7], [108, 8], [107, 8], [107, 7]]],
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
        ],
    }


@pytest.fixture
def invalid_multi_polygon_linear_ring_validation():
    """Invalid MultiPolygon with bad linear ring validation."""
    return {
        "type": "MultiPolygon",
        "coordinates": [
            [[[107, 7], [108, 7]]],  # too short
            [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 90]]],  # no loop
        ],
    }


# ============================================================================
# Feature fixtures
# ============================================================================


@pytest.fixture
def valid_feature_all_fields():
    """Valid Feature with all fields populated."""
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
    """Valid Feature with only required type field."""
    return {"type": "Feature", "geometry": None, "properties": None, "id": None}


@pytest.fixture
def valid_feature_point_geometry(sample_coordinate_2d):
    """Valid Feature with Point geometry."""
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": sample_coordinate_2d},
        "properties": {"name": "Test Point"},
    }


@pytest.fixture
def invalid_feature_wrong_type(valid_feature_all_fields):
    """Invalid Feature with wrong type."""
    wrong_type = "Point"
    return {**valid_feature_all_fields, "type": wrong_type}


# ============================================================================
# FeatureCollection fixtures
# ============================================================================


@pytest.fixture
def valid_feature_collection_data():
    """Valid FeatureCollection GeoJSON data."""
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


@pytest.fixture
def valid_feature_collection_empty():
    """Valid FeatureCollection with empty features list."""
    return {"type": "FeatureCollection", "features": []}


@pytest.fixture
def invalid_feature_collection_wrong_type(valid_feature_collection_data):
    """Invalid FeatureCollection with wrong type."""
    invalid_data = copy.deepcopy(valid_feature_collection_data)
    invalid_data["type"] = "GeometryCollection"
    return invalid_data


# ============================================================================
# GeometryCollection fixtures
# ============================================================================


@pytest.fixture
def valid_geometry_collection_data():
    """Valid GeometryCollection GeoJSON data."""
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
def valid_geometry_collection_empty():
    """Valid GeometryCollection with empty geometries list."""
    return {"type": "GeometryCollection", "geometries": []}


@pytest.fixture
def nested_geometry_collection_data(sample_coordinate_2d):
    """GeometryCollection containing another GeometryCollection.

    This fixture creates a GeometryCollection with a nested GeometryCollection inside.
    Can be used both for GeometryCollectionModel tests and Feature tests.
    """
    return {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": sample_coordinate_2d},
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "LineString",
                        "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
                    },
                ],
            },
        ],
    }


@pytest.fixture
def geometry_collection_bad_type(valid_geometry_collection_data):
    """Invalid GeometryCollection with wrong type."""
    invalid_data = copy.deepcopy(valid_geometry_collection_data)
    invalid_data["type"] = "FeatureCollection"
    return invalid_data


# ============================================================================
# Bounding box fixtures
# ============================================================================


@pytest.fixture
def bbox_2d():
    """2D bounding box [min_lon, min_lat, max_lon, max_lat]."""
    return [-180.0, -90.0, 180.0, 90.0]


@pytest.fixture
def bbox_3d():
    """3D bounding box [min_lon, min_lat, min_alt, max_lon, max_lat, max_alt]."""
    return [-180.0, -90.0, 0.0, 180.0, 90.0, 1000.0]


@pytest.fixture
def invalid_bbox_too_short():
    """Invalid bounding box with too few elements."""
    return [0.0]


@pytest.fixture
def invalid_bbox_too_long():
    """Invalid bounding box with too many elements."""
    return [-180.0, -90.0, 0.0, 180.0, 90.0, 1000.0, 2000.0]


# ============================================================================
# Parametrized geometry fixtures for Feature tests
# ============================================================================


@pytest.fixture
def geometry_fixtures(sample_coordinate_2d):
    """Dictionary of geometry fixtures for testing Feature with different geometry types."""
    return {
        "Point": {"type": "Point", "coordinates": sample_coordinate_2d},
        "MultiPoint": {
            "type": "MultiPoint",
            "coordinates": [sample_coordinate_2d, [-80.666513, 35.053994]],
        },
        "LineString": {
            "type": "LineString",
            "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
        },
        "MultiLineString": {
            "type": "MultiLineString",
            "coordinates": [[[-99.113159, 38.869651], [-99.0802, 38.85682]]],
        },
        "Polygon": {
            "type": "Polygon",
            "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
        },
        "MultiPolygon": {
            "type": "MultiPolygon",
            "coordinates": [[[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]],
        },
        "GeometryCollection": {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": sample_coordinate_2d},
            ],
        },
    }


# ============================================================================
# Parametrized fixtures for Feature ID tests
# ============================================================================


@pytest.fixture
def feature_id_values():
    """Valid Feature ID values for testing."""
    return [
        ("string_id", "feature-123"),
        ("integer_id", 123),
        ("numeric_string_id", "456"),
        ("large_integer_id", 999999),
    ]


@pytest.fixture
def feature_with_geometry_collection(sample_coordinate_2d):
    """Feature with GeometryCollection geometry."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": sample_coordinate_2d},
                {
                    "type": "LineString",
                    "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
                },
            ],
        },
        "properties": {"name": "Test GeometryCollection"},
    }


@pytest.fixture
def feature_with_nested_geometry_collection(nested_geometry_collection_data):
    """Feature with nested GeometryCollection in geometry.

    Reuses nested_geometry_collection_data fixture to avoid duplication.
    """
    return {
        "type": "Feature",
        "geometry": nested_geometry_collection_data,
        "properties": {"name": "Test Nested GeometryCollection"},
    }
