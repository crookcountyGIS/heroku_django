import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot, Feature
from functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, regex_filter
import json
import requests
pd.set_option('display.max_columns', None)

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
    dfList = []

    for element in jsonResponse['features']:
        root = Root.from_dict(element)
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    propvalue = PvRoot.from_dict(jsonValueResponse)

    for f in propvalue.features:
        dfList.append(f.attributes)

    df = pd.DataFrame(dfList)
    print(df.sort_values(by='year'))

    prop_ = [f.attributes for f in propvalue.features]
    x = [row for row in prop_ if row.year == '2018']


valuation(1001)