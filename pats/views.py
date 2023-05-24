from django.shortcuts import render
from django.http import HttpResponse
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
from pats.functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, search_all, search_account
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

def tableSearchResults(request, value): # this search form needs error redirecting, or failed response built into the page

    split_value = value.split()
    #print(split_value)

    propSearch_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/19/query"
    propTable_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    jr_list = []
    for value in split_value:
        where_clause = search_all(value)
        url = f"{propSearch_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

        response = requests.get(url)
        jsonResponse = response.json()
        jr_list.append(jsonResponse)

    #print(jr_list)
    # if jsonResponse['features'] == []:
    #     print("I dont think there is anything here.")

    df_list = []
    for dicts in jr_list:

        for element in dicts['features']:
            accounts = element['attributes']['account_id']
            where_clause = search_account(accounts)
            table_url = f"{propTable_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

            responseTable = requests.get(table_url)
            jsonResponseTable = responseTable.json()

            for elem in jsonResponseTable['features']:
                root = Root.from_dict(elem)
                df_list.append(root.attributes)

    df = pd.DataFrame(df_list)

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    html_table = df.to_html(classes='table table-striped', index=False)
    context = {'html_table': html_table, 'd': data}

    return render(request, 'pats/searchResults.html', context)

def valuation(request, account):
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
    dfList = []

    for element in jsonResponse['features']:
        root = Root.from_dict(element)
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    propvalue = PvRoot.from_dict(jsonValueResponse)

    for f in propvalue.features:
        dfList.append(f.attributes)

    df_appended = pd.DataFrame(dfList)
    df = df_appended.sort_values(by='year')

    json_records = df.reset_index().to_json(orient='records')
    df_data = json.loads(json_records)

    html_table = df.to_html(classes='table table-striped', index=False)

    context = {'account_info':jsonResponse,
               'value_data':jsonValueResponse,
               'maptaxlot': maptaxlot,
               'html_table': html_table, 
               'd': df_data}

    return render(request, 'pats/valuation.html', context)

# def valuation(request, account):

#     prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
#     propValue_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/12/query"

#     #where_clause = f"account_id = {account}"
#     where_clause = regex_filter(account)
#     out_fields = "*"
#     return_geometry = "false"
#     f = "pjson"

#     url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
#     url_value = f"{propValue_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

#     # set variables
#     response = requests.get(url)
#     responseValue = requests.get(url_value)
#     jsonResponse = response.json()
#     jsonValueResponse = responseValue.json()

#     # set empty lists
#     maptaxlot = []

#     for element in jsonResponse['features']:
#         root = Root.from_dict(element)
#         mt = root.attributes.map_taxlot
#         mt_find = mt[:mt.find('-', mt.find('-') + 1)]
#         maptaxlot.append(mt_find.replace('-', ''))
        

#     # set empty dictionaries
#     real_market_value = {}
#     value_structure = {}
#     total_real_market = {}
#     max_assessed = {}
#     total_assessed = {}
#     veterans = {}
#     year_list = [2018, 2019, 2020, 2021, 2022]

#     # ----------- under construction ---------
#     for element in jsonValueResponse['features']:
#         value_root = PvRoot.from_dict(element)
        

#         #if feature['attributes']['year'] == yr:
#             # real_market_value[yr] = feature['attributes']['rmv_land']
#             # value_structure[yr] = feature['attributes']['rmv_impr']
#             # total_real_market[yr] = feature['attributes']['rmv_total']
#             # max_assessed[yr] = feature['attributes']['max_av']
#             # total_assessed[yr] = feature['attributes']['total_av']
#             # veterans[yr] = feature['attributes']['exempt']


#     context = {'data':jsonResponse, 
#     'value_data':jsonValueResponse, 
#     'maptaxlot': maptaxlot,
#     'value_structure':value_structure, 
#     'max_assessed':max_assessed, 
#     'real_market_value':real_market_value, 
#     'total_real_market':total_real_market, 
#     'total_assessed':total_assessed, 
#     'veterans':veterans}
#     # ----------- under construction ---------
    
#     return render(request, 'pats/valuation.html', context)

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


