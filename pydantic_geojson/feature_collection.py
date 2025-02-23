from typing import List, Union

from pydantic import BaseModel

from ._base import FeatureCollectionFieldType, GeoJSONModel
from .feature import FeatureModel


class FeatureCollectionModel(GeoJSONModel):
    type: FeatureCollectionFieldType
    features: List[FeatureModel]
