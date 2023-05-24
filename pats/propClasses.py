from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Attributes:
    OBJECTID: int
    county_id: str
    account_id: str
    map_taxlot: str
    account_type: str
    owner_name: str
    real_account_id: str
    unit_number: str
    park_name: str
    owner_line_care_of: str
    owner_mailing_address1: str
    owner_mailing_address2: str
    owner_mailing_address3: str
    owner_mailing_city: str
    owner_mailing_state: str
    owner_mailing_zip: str
    current_property_tax: float
    tax_id: str
    situs_address: str
    pdf_file_exists: int
    rmv_total: float
    taxable_av: float
    maximum_av: float
    veterans_exemption: float
    x_number: str
    year: str
    sqft: int
    tax_status: str
    property_class: str
    property_class_description: str
    subdivision: str
    block: str
    lot: str
    land_size_acres: float
    rmv_land: float
    rmv_improvements: float
    property_tax_current_year: float
    tax_code_area: str
    last_sale_date: float
    last_sale_amount: float
    related_accounts: int
    agent_name: str
    business_class_description: str

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        _OBJECTID = int(obj.get("OBJECTID"))
        _county_id = str(obj.get("county_id"))
        _account_id = str(obj.get("account_id"))
        _map_taxlot = str(obj.get("map_taxlot"))
        _account_type = str(obj.get("account_type"))
        _owner_name = str(obj.get("owner_name"))
        _real_account_id = str(obj.get("real_account_id"))
        _unit_number = str(obj.get("unit_number"))
        _park_name = str(obj.get("park_name"))
        _owner_line_care_of = str(obj.get("owner_line_care_of"))
        _owner_mailing_address1 = str(obj.get("owner_mailing_address1"))
        _owner_mailing_address2 = str(obj.get("owner_mailing_address2"))
        _owner_mailing_address3 = str(obj.get("owner_mailing_address3"))
        _owner_mailing_city = str(obj.get("owner_mailing_city"))
        _owner_mailing_state = str(obj.get("owner_mailing_state"))
        _owner_mailing_zip = str(obj.get("owner_mailing_zip"))
        _current_property_tax = float(obj.get("current_property_tax"))
        _tax_id = str(obj.get("tax_id"))
        _situs_address = str(obj.get("situs_address"))
        _pdf_file_exists = int(obj.get("pdf_file_exists"))
        _rmv_total = float(obj.get("rmv_total"))
        _taxable_av = float(obj.get("taxable_av"))
        _maximum_av = float(obj.get("maximum_av"))
        _veterans_exemption = float(obj.get("veterans_exemption"))
        _x_number = str(obj.get("x_number"))
        _year = str(obj.get("year"))
        _sqft = str(obj.get("sqft"))
        _tax_status = str(obj.get("tax_status"))
        _property_class = str(obj.get("property_class"))
        _property_class_description = str(obj.get("property_class_description"))
        _subdivision = str(obj.get("subdivision"))
        _block = str(obj.get("block"))
        _lot = str(obj.get("lot"))
        _land_size_acres = float(obj.get("land_size_acres"))
        _rmv_land = float(obj.get("rmv_land"))
        _rmv_improvements = float(obj.get("rmv_improvements"))
        _property_tax_current_year = float(obj.get("property_tax_current_year"))
        _tax_code_area = str(obj.get("tax_code_area"))
        _last_sale_date = float(obj.get("last_sale_date"))
        _last_sale_amount = float(obj.get("last_sale_amount"))
        _related_accounts = int(obj.get("related_accounts"))
        _agent_name = str(obj.get("agent_name"))
        _business_class_description = str(obj.get("business_class_description"))
        return Attributes(_OBJECTID, _county_id, _account_id, _map_taxlot, _account_type, _owner_name, _real_account_id, _unit_number, _park_name, _owner_line_care_of, _owner_mailing_address1, _owner_mailing_address2, _owner_mailing_address3, _owner_mailing_city, _owner_mailing_state, _owner_mailing_zip, _current_property_tax, _tax_id, _situs_address, _pdf_file_exists, _rmv_total, _taxable_av, _maximum_av, _veterans_exemption, _x_number, _year, _sqft, _tax_status, _property_class, _property_class_description, _subdivision, _block, _lot, _land_size_acres, _rmv_land, _rmv_improvements, _property_tax_current_year, _tax_code_area, _last_sale_date, _last_sale_amount, _related_accounts, _agent_name, _business_class_description)

@dataclass
class Root:
    attributes: Attributes

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _attributes = Attributes.from_dict(obj.get("attributes"))
        return Root(_attributes)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
