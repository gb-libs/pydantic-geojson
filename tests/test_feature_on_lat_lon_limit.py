from pydantic import ValidationError
import pytest
from pydantic_geojson import LineStringModel, PointModel, PolygonModel

data_linestring = {
    "type": "LineString",
    "coordinates": [
        [-180.0, -90],
        [180.0, 90],
    ],
}

data_point = {"type": "Point", "coordinates": [-180, 90]}

data_point_error_lon_min = {"type": "Point", "coordinates": [-181, 90]}

data_point_error_lon_max = {"type": "Point", "coordinates": [181, 90]}


data_point_error_lat_min = {"type": "Point", "coordinates": [-180, -91]}

data_point_error_lat_max = {"type": "Point", "coordinates": [180, 91]}

data_polygon = {
    "type": "Polygon",
    "coordinates": [[[-180, 90], [180, 90], [180, -90], [-180, -90], [180, 90]]],
}


class TestFeatureOnLimit:
    def test_loads_model_linestring(self):
        ls_model = LineStringModel(**data_linestring)
        coordinates = ls_model.coordinates

        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert data_linestring["coordinates"][lsi_key] == [lon, lat]

        assert ls_model.type == data_linestring["type"]

    def test_loads_model_point(self):
        p_model = PointModel(**data_point)
        coordinates = p_model.coordinates

        lon, lat = coordinates.lon, coordinates.lat
        assert data_point["coordinates"] == [lon, lat]

        assert p_model.type == data_point["type"]

    def test_loads_model(self):
        p_model = PolygonModel(**data_polygon)
        coordinates = p_model.coordinates

        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate.lon, p_coordinate.lat
                assert data_polygon["coordinates"][pi_key][pl_key] == [lon, lat]

        assert p_model.type == data_polygon["type"]

    def test_error_in_output_range_lon_min(self):
        with pytest.raises(ValidationError):
            PointModel(**data_point_error_lon_min)

    def test_error_in_output_range_lat_min(self):
        with pytest.raises(ValidationError):
            PointModel(**data_point_error_lat_min)

    def test_error_in_output_range_lon_max(self):
        with pytest.raises(ValidationError):
            PointModel(**data_point_error_lon_max)

    def test_error_in_output_range_lat_max(self):
        with pytest.raises(ValidationError):
            PointModel(**data_point_error_lat_max)
