from typing import List

from ._base import FeatureCollectionFieldType, GeoJSONModel
from .feature import FeatureModel


class FeatureCollectionModel(GeoJSONModel):
    type: FeatureCollectionFieldType
    features: List[FeatureModel]
