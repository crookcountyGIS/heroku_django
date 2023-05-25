from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class PsAttributes:
    OBJECTID: str
    search_all: str
    account_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'PsAttributes':
        _OBJECTID = str(obj.get("OBJECTID"))
        _search_all = str(obj.get("search_all"))
        _account_id = str(obj.get("account_id"))
        return PsAttributes(_OBJECTID, _search_all, _account_id)

@dataclass
class Feature:
    attributes: PsAttributes

    @staticmethod
    def from_dict(obj: Any) -> 'Feature':
        _attributes = PsAttributes.from_dict(obj.get("attributes"))
        return Feature(_attributes)

@dataclass
class PsRoot:
    features: List[Feature]

    @staticmethod
    def from_dict(obj: Any) -> 'PsRoot':
        _features = [Feature.from_dict(y) for y in obj.get("features")]
        return PsRoot(_features)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
