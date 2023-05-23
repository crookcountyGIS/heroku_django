from django.shortcuts import render
from django.http import HttpResponse
from pats.propClasses import Attributes, Root
from pats.propValueClasses import ValueAttributes, ValueRoot
from pats.functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, regex_filter
import json
import requests
import pandas as pd
import os
import sys
import re
import requests



def valuation(account):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/12/query"

    #where_clause = f"account_id = {account}"
    where_clause = regex_filter(account)
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"


    url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    url_value = f"{propValue_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

    # set variables
    response = requests.get(url)
    responseValue = requests.get(url_value)
    jsonResponse = response.json()
    jsonValueResponse = responseValue.json()

    # set empty lists
    maptaxlot = []
    structure = []

    for element in jsonResponse['features']:
        root = Root.from_dict(element)
        mt = root.attributes.map_taxlot
        print(mt)
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))
        
    print(maptaxlot)

    # set empty dictionaries
    real_market_value = {}
    value_structure = {}
    total_real_market = {}
    max_assessed = {}
    total_assessed = {}
    veterans = {}
    year_list = [2018, 2019, 2020, 2021, 2022]

    for element in jsonValueResponse['features']:
        value_root = ValueRoot.from_dict(element)
        yr = [year for year in year_list if value_root.attributes.year == year]
        print(yr)


valuation(1001)





# def valuation(value):

#     prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
#     out_fields = "*"
#     return_geometry = "false"
#     f = "pjson"
   
#     if is_string_numbers(str(value)) is True and len(str(value)) < 6:
#         (where_clause := f"account_id = '{value}'")
#         print(where_clause)
#         print("Account Query")
    
#     elif is_string_letters(str(value)) is True:
#         searched_name = value.upper()
#         (where_clause := f"owner_name LIKE '%{searched_name}%'")
#         print(where_clause)
#         print("Owner Name Query")

#     elif is_string_alphanumeric(str(value)) is True:
#         value = value[:8] + "-" + value[8:]
#         (where_clause := f"map_taxlot LIKE '%{value}%'")
#         print(where_clause)
#         print("Map Taxlot Query")

#     elif is_address(str(value)) is True:
#         situs = value.upper()
#         (where_clause := f"situs_address LIKE '%{situs}%'")
#         print(where_clause)
#         print("Address Query")

#     else:
#         print('search error -- #http redirect??')

#     url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    
#     response = requests.get(url)
#     jsonResponse = response.json()
#     if jsonResponse['features'] == []:
#         print("I dont think there is anything here.")

#     for element in jsonResponse['features']: 
#         root = Root.from_dict(element)
#   
#         rootList.append(root.attributes)
#         print(root.attributes.owner_name)
#         print(root.attributes.account_id)
#         print(root.attributes.account_type)
#         print(root.attributes.situs_address)
#         print(root.attributes.rmv_total)
#         print(root.attributes.map_taxlot)
#         print(root.attributes.situs_address)


        
#     return f" root values returned "
