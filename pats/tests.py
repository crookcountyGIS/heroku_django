from django.shortcuts import render
from django.http import HttpResponse
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot, Feature
from functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, regex_filter
import json
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

    for element in jsonResponse['features']:
        root = Root.from_dict(element)
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    #print(maptaxlot)

    # # set empty dictionaries
    # real_market_value = {}
    # value_structure = {}
    # total_real_market = {}
    # max_assessed = {}
    # total_assessed = {}
    # veterans = {}
    year_list = ['2018', '2019', '2020', '2021', '2022']

    # for element in jsonValueResponse['features']:
    #     value_root = ValueRoot.from_dict(element)
    #     print(value_root)
    propvalue = PvRoot.from_dict(jsonValueResponse)

    myList = []
    for f in propvalue.features:
        print(f.attributes.year)
        # rmv = int(f.attributes.year)
        myList.append(f.attributes)

    #print(myList[0].acount_id)
        # print(sorted(myList))

    prop_ = [f.attributes for f in propvalue.features]
    #print(prop_)
    # for row in prop_:
    #     if row.year == '2018':
    #         print(row.rmv_land)

    x = [row for row in prop_ if row.year == '2018']


    #print(properties_2021)
    #print(propvalue.features[0].attributes)
    #total_av = [f.attributes.total_av for f in propvalue.features ]
    #print(total_av)

valuation(1001)