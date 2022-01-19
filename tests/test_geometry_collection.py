from pydantic_geojson import GeometryCollectionModel
from pydantic_geojson.object_type import GEOMETRY_COLLECTION

data = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [-80.660805, 35.049392]
        },
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [-80.664582, 35.044965],
                    [-80.663874, 35.04428],
                    [-80.662586, 35.04558],
                    [-80.663444, 35.046036],
                    [-80.664582, 35.044965]
                ]
            ]
        },
        {
            "type": "LineString",
            "coordinates": [
                [-80.662372, 35.059509],
                [-80.662693, 35.059263],
                [-80.662844, 35.05893]
            ]
        }
    ]
}


class TestGeometryCollectionModel:
    def test_loads_model(self):
        gc_model = GeometryCollectionModel(**data)
        geometries = gc_model.geometries

        for g_key, g_item in enumerate(geometries):
            assert g_item.type == data['geometries'][g_key]['type']

        assert gc_model.type == data['type']

    def test_model_type(self):
        gc_model = GeometryCollectionModel(**data)
        assert gc_model.type == GEOMETRY_COLLECTION
