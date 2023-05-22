import json
import os
import sys
import re
import requests
from PropClasses import Attributes, Root

rootList = []

def is_string_numbers(regex):
    match = re.match(r"^\d+$", regex)
    return match is not None

def is_string_letters(regex):
    match = re.match(r"^[a-zA-Z]+(?: [a-zA-Z]+)*(?: [a-zA-Z]+)*$", regex)
    return match is not None

def is_string_alphanumeric(regex):
    match = re.match(r"^\w+$", regex)
    return match is not None

def is_address(regex):
    match = re.match(r"^(\d+)\s+(.+?)$", regex)
    return match is not None

def valuation(value):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"
   
    if is_string_numbers(str(value)) is True and len(str(value)) < 6:
        (where_clause := f"account_id = '{value}'")
        print(where_clause)
        print("Account Query")
    
    elif is_string_letters(str(value)) is True:
        searched_name = value.upper()
        (where_clause := f"owner_name LIKE '%{searched_name}%'")
        print(where_clause)
        print("Owner Name Query")

    elif is_string_alphanumeric(str(value)) is True:
        value = value[:8] + "-" + value[8:]
        (where_clause := f"map_taxlot LIKE '%{value}%'")
        print(where_clause)
        print("Map Taxlot Query")

    elif is_address(str(value)) is True:
        situs = value.upper()
        (where_clause := f"situs_address LIKE '%{situs}%'")
        print(where_clause)
        print("Address Query")

    else:
        print('search error -- #http redirect??')

    url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    
    response = requests.get(url)
    jsonResponse = response.json()
    if jsonResponse['features'] == []:
        print("I dont think there is anything here.")

    for element in jsonResponse['features']: 
        root = Root.from_dict(element)
        # print(root)
        # if len(root) < 1:
        #     print("I dont think there is anything here.")
        #else:
        rootList.append(root.attributes)
        print(root.attributes.owner_name)
        print(root.attributes.account_id)
        print(root.attributes.account_type)
        print(root.attributes.situs_address)
        print(root.attributes.rmv_total)
        print(root.attributes.map_taxlot)
        print(root.attributes.situs_address)
        
    return f" root values returned "

try:
    valuation('422 nw beaver, prineville, or')
except TypeError:
    print("Type Error")
except NoneType:
    print("None Type")




# def is_address(value):
#     match = re.match(r"^(\d+)\s+(.+?)$", value)
#     print(match)
#     return match is not None


# if is_address('640 nw 2nd st, prineville, or') is True:
#     print(True)