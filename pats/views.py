from django.shortcuts import render
from django.http import HttpResponse
from pats.propClasses import Attributes, Root
from pats.functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, regex_filter
import json
import requests
import pandas as pd
import os
import sys
import re
import requests


rootList = []


def base(request):

    return render(request, 'pats/base.html')

def index(request):

    return render(request, 'pats/index.html')
    
def mapPage(request):
        
    return render(request, 'pats/mapPage.html')

def tableSearchResults(request, value):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    where_clause = regex_filter(value)

    url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

    response = requests.get(url)
    jsonResponse = response.json()
    if jsonResponse['features'] == []:
        print("I dont think there is anything here.")

    df_list = []
    for element in jsonResponse['features']:
        # print(element['attributes'])
        df = pd.DataFrame.from_dict(element['attributes'], orient='index').T
        df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    html_table = df.to_html(classes='table table-striped', index=False)
    context = {'html_table': html_table, 'd': data}

    return render(request, 'pats/searchResults.html', context)


def valuation(request, account):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property_values/FeatureServer/0/query"

    where_clause = f"account_id = {account}"
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
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                mt = feature['attributes']['map_taxlot']
                mt_find = mt[:mt.find('-', mt.find('-') + 1)]
                maptaxlot.append(mt_find.replace('-', ''))


    # set empty dictionaries
    real_market_value = {}
    value_structure = {}
    total_real_market = {}
    max_assessed = {}
    total_assessed = {}
    veterans = {}
    year_list = [2018, 2019, 2020, 2021, 2022]

    for keys, value in jsonValueResponse.items():
        if keys == 'features':
            for feature in value:
                for yr in year_list:
                    if feature['attributes']['year_'] == yr:
                        real_market_value[yr] = feature['attributes']['rmv_land']
                        value_structure[yr] = feature['attributes']['rmv_impr']
                        total_real_market[yr] = feature['attributes']['rmv_total']
                        max_assessed[yr] = feature['attributes']['max_av']
                        total_assessed[yr] = feature['attributes']['total_av']
                        veterans[yr] = feature['attributes']['exempt']


    context = {'data':jsonResponse, 'value_data':jsonValueResponse, 'maptaxlot': maptaxlot,
    'value_structure':value_structure, 'max_assessed':max_assessed, 'real_market_value':real_market_value, 'total_real_market':total_real_market, 
    'total_assessed':total_assessed, 'veterans':veterans}
    
    return render(request, 'pats/valuation.html', context)

def account_query(request, account):

    base_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    where_clause = f"account_id = {account}"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    url = f"{base_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    response = requests.get(url)
    jsonResponse = response.json()

    maptaxlot = []
    structure = []
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                mt = feature['attributes']['map_taxlot']
                mt_find = mt[:mt.find('-', mt.find('-') + 1)]
                maptaxlot.append(mt_find.replace('-', ''))

    context = {'data':jsonResponse, 'maptaxlot': maptaxlot}

    return render(request, 'pats/summaryPage.html', context)

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
#         # print(root)
#         # if len(root) < 1:
#         #     print("I dont think there is anything here.")
#         #else:
#         rootList.append(root.attributes)
#         print(root.attributes.owner_name)
#         print(root.attributes.account_id)
#         print(root.attributes.account_type)
#         print(root.attributes.situs_address)
#         print(root.attributes.rmv_total)
#         print(root.attributes.map_taxlot)
#         print(root.attributes.situs_address)


        
#     return f" root values returned "

