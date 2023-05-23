from typing import List
from typing import Any
from dataclasses import dataclass
import json
from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class PvAttributes:
    OBJECTID: int
    county_id: str
    account_id: str
    year: str
    rmv_land: float
    rmv_impr: float
    rmv_total: float
    total_av: float
    max_av: float
    exempt: float
    original_tax: float
    tax_code_area: str

    @staticmethod
    def from_dict(obj: Any) -> 'PvAttributes':
        _OBJECTID = int(obj.get("OBJECTID"))
        _county_id = str(obj.get("county_id"))
        _account_id = str(obj.get("account_id"))
        _year = str(obj.get("year"))
        _rmv_land = float(obj.get("rmv_land"))
        _rmv_impr = float(obj.get("rmv_impr"))
        _rmv_total = float(obj.get("rmv_total"))
        _total_av = float(obj.get("total_av"))
        _max_av = float(obj.get("max_av"))
        _exempt = float(obj.get("exempt"))
        _original_tax = float(obj.get("original_tax"))
        _tax_code_area = str(obj.get("tax_code_area"))
        return PvAttributes(_OBJECTID, _county_id, _account_id, _year, _rmv_land, _rmv_impr, _rmv_total, _total_av, _max_av, _exempt, _original_tax, _tax_code_area)

@dataclass
class Feature:
    attributes: PvAttributes

    @staticmethod
    def from_dict(obj: Any) -> 'Feature':
        _attributes = PvAttributes.from_dict(obj.get("attributes"))
        return Feature(_attributes)

@dataclass
class PvRoot:
    features: List[Feature]

    @staticmethod
    def from_dict(obj: Any) -> 'PvRoot':
        _features = [Feature.from_dict(y) for y in obj.get("features")]
        return PvRoot(_features)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = PvRoot.from_dict(jsonstring)
