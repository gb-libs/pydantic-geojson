[![GitHub Actions status for master branch](https://github.com/gb-libs/pydantic-geojson/actions/workflows/main.yml/badge.svg)](https://github.com/gb-libs/pydantic-geojson/actions?query=workflow%3A%22Python+package%22)
[![Latest PyPI package version](https://badge.fury.io/py/pydantic-geojson.svg)](https://pypi.org/project/pydantic-geojson/)
[![codecov](https://codecov.io/gh/gb-libs/pydantic-geojson/branch/master/graph/badge.svg?token=8LMKSDQTIR)](https://codecov.io/gh/gb-libs/pydantic-geojson)
[![Downloads](https://static.pepy.tech/personalized-badge/pydantic-geojson?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/pydantic-geojson)

pydantic-geojson 🌍
===================


| GeoJSON Objects    | Status |
|--------------------|--------|
| Point              | ✅      |
| MultiPoint         | ✅      |
| LineString         | ✅      |
| MultiLineString    | ✅      |
| Polygon            | ✅      |
| MultiPolygon       | ✅      |
| GeometryCollection | ✅      |
| Feature            | ✅      |
| FeatureCollection  | ✅      |

Installation
------------

pydantic-geojson is compatible with Python 3.7 and up.
The recommended way to install is via [poetry](https://python-poetry.org/):

```
poetry add pydantic_geojson
```

Using pip to install is also possible.

```
pip install pydantic_geojson
```

GEOJSON
-------

[GeoJSON](https://geojson.org/) is a format for encoding a variety of geographic data structures.

```
{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
    },
    "properties": {
        "name": "Dinagat Islands"
    }
}
```

GeoJSON supports the following geometry types: Point, LineString, Polygon,
MultiPoint, MultiLineString, and MultiPolygon. Geometric objects with
additional properties are Feature objects. Sets of features are contained by
FeatureCollection objects.

Examples of using
-----------------

Custom properties:

```
from pydantic import BaseModel
from pydantic_geojson import FeatureModel


class MyPropertiesModel(BaseModel):
    name: str


class MyFeatureModel(FeatureModel):
    properties: MyPropertiesModel


data = {
    "type": "Feature",
    "properties": {
        "name": "foo name",
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-80.724878, 35.265454],
                [-80.722646, 35.260338]
            ]
        ]
    }
}

>>> MyFeatureModel(**data)
>>> type='Feature' geometry=PolygonModel(type='Polygon', coordinates=[[Coordinates(lon=-80.724878, lat=35.265454), Coordinates(lon=-80.722646, lat=35.260338)]]) properties=MyPropertiesModel(name='foo name')
```

Point
-----

Simple example data:

```
from pydantic_geojson import PointModel

data = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422]
}

>>> PointModel(**data)
>>> type='Point' coordinates=Coordinates(lon=-105.01621, lat=39.57422)
```

MultiPoint
----------

Simple example data:

```
from pydantic_geojson import MultiPointModel

data = {
    "type": "MultiPoint",
    "coordinates": [
        [-105.01621, 39.57422],
        [-80.666513, 35.053994]
    ]
}

>>> PointModel(**data)
>>> type='MultiPoint' coordinates=[Coordinates(lon=-105.01621, lat=39.57422), Coordinates(lon=-80.666513, lat=35.053994)]
```

LineString
----------

Simple example data:

```
from pydantic_geojson import LineStringModel

data = {
    "type": "LineString",
    "coordinates": [
        [-99.113159, 38.869651],
        [-99.0802, 38.85682],
        [-98.822021, 38.85682],
        [-98.448486, 38.848264]
    ]
}

>>> LineStringModel(**data)
>>> type='LineString' coordinates=[Coordinates(lon=-99.113159, lat=38.869651), Coordinates(lon=-99.0802, lat=38.85682), Coordinates(lon=-98.822021, lat=38.85682), Coordinates(lon=-98.448486, lat=38.848264)]
```

MultiLineString
---------------

Simple example data:

```
from pydantic_geojson import MultiLineStringModel

data = {
    "type": "MultiLineString",
    "coordinates": [
        [
            [-105.019898, 39.574997],
            [-105.019598, 39.574898],
            [-105.019061, 39.574782]
        ],
        [
            [-105.017173, 39.574402],
            [-105.01698, 39.574385],
            [-105.016636, 39.574385],
            [-105.016508, 39.574402],
            [-105.01595, 39.57427]
        ],
        [
            [-105.014276, 39.573972],
            [-105.014126, 39.574038],
            [-105.013825, 39.57417],
            [-105.01331, 39.574452]
        ]
    ]
}

>>> MultiLineStringModel(**data)
>>> type='MultiLineString' coordinates=[[Coordinates(lon=-105.019898, lat=39.574997), Coordinates(lon=-105.019598, lat=39.574898), Coordinates(lon=-105.019061, lat=39.574782)], [Coordinates(lon=-105.017173, lat=39.574402), Coordinates(lon=-105.01698, lat=39.574385), Coordinates(lon=-105.016636, lat=39.574385), Coordinates(lon=-105.016508, lat=39.574402), Coordinates(lon=-105.01595, lat=39.57427)], [Coordinates(lon=-105.014276, lat=39.573972), Coordinates(lon=-105.014126, lat=39.574038), Coordinates(lon=-105.013825, lat=39.57417), Coordinates(lon=-105.01331, lat=39.574452)]]
```

Polygon
-------

Simple example data:

```
from pydantic_geojson import PolygonModel

data = {
    "type": "Polygon",
    "coordinates": [
        [
            [100, 0],
            [101, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}

>>> PolygonModel(**data)
>>> type='Polygon' coordinates=[[Coordinates(lon=100.0, lat=0.0), Coordinates(lon=101.0, lat=0.0), Coordinates(lon=101.0, lat=1.0), Coordinates(lon=100.0, lat=1.0), Coordinates(lon=100.0, lat=0.0)]]
```

MultiPolygon
------------

Simple example data:

```
from pydantic_geojson import MultiPolygonModel

data = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [107, 7],
                [108, 7],
                [108, 8],
                [107, 8],
                [107, 7]
            ]
        ],
        [
            [
                [100, 0],
                [101, 0],
                [101, 1],
                [100, 1],
                [100, 0]
            ]
        ]
    ]
}

>>> MultiPolygonModel(**data)
>>> type='MultiPolygon' coordinates=[[[Coordinates(lon=107.0, lat=7.0), Coordinates(lon=108.0, lat=7.0), Coordinates(lon=108.0, lat=8.0), Coordinates(lon=107.0, lat=8.0), Coordinates(lon=107.0, lat=7.0)]], [[Coordinates(lon=100.0, lat=0.0), Coordinates(lon=101.0, lat=0.0), Coordinates(lon=101.0, lat=1.0), Coordinates(lon=100.0, lat=1.0), Coordinates(lon=100.0, lat=0.0)]]]
```

GeometryCollection
------------------

Simple example data:

```
from pydantic_geojson import GeometryCollectionModel

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

>>> GeometryCollectionModel(**data)
>>> type='GeometryCollection' geometries=[PointModel(type='Point', coordinates=Coordinates(lon=-80.660805, lat=35.049392)), PolygonModel(type='Polygon', coordinates=[[Coordinates(lon=-80.664582, lat=35.044965), Coordinates(lon=-80.663874, lat=35.04428), Coordinates(lon=-80.662586, lat=35.04558), Coordinates(lon=-80.663444, lat=35.046036), Coordinates(lon=-80.664582, lat=35.044965)]]), LineStringModel(type='LineString', coordinates=[Coordinates(lon=-80.662372, lat=35.059509), Coordinates(lon=-80.662693, lat=35.059263), Coordinates(lon=-80.662844, lat=35.05893)])]
```

Feature
-------

Simple example data:

```
from pydantic_geojson import FeatureModel

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
    }
}

>>> FeatureModel(**data)
>>> type='Feature' geometry=PolygonModel(type='Polygon', coordinates=[[Coordinates(lon=-80.724878, lat=35.265454), Coordinates(lon=-80.722646, lat=35.260338), Coordinates(lon=-80.720329, lat=35.260618), Coordinates(lon=-80.71681, lat=35.255361), Coordinates(lon=-80.704793, lat=35.268397), Coordinates(lon=-82.715179, lat=35.267696), Coordinates(lon=-80.721359, lat=35.267276), Coordinates(lon=-80.724878, lat=35.265454)]])

```

FeatureCollection
-----------------

Simple example data:

```
from pydantic_geojson import FeatureCollectionModel

data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-80.870885, 35.215151]
            }
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
                        [-80.724878, 35.265454]
                    ]
                ]
            }
        }
    ]
}

>>> FeatureCollectionModel(**data)
>>> type='FeatureCollection' features=[FeatureModel(type='Feature', geometry=PointModel(type='Point', coordinates=Coordinates(lon=-80.870885, lat=35.215151))), FeatureModel(type='Feature', geometry=PolygonModel(type='Polygon', coordinates=[[Coordinates(lon=-80.724878, lat=35.265454), Coordinates(lon=-80.722646, lat=35.260338), Coordinates(lon=-80.720329, lat=35.260618), Coordinates(lon=-80.704793, lat=35.268397), Coordinates(lon=-80.724878, lat=35.265454)]]))]

```
