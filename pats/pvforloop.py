from django.shortcuts import render
from django.http import HttpResponse
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
#from pats.functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, search_all
import json
import requests
import pandas as pd
import os
import sys
import re
import requests

def search_all(value):

    str(value).upper()
    (where_clause := f"search_all LIKE '%{value}%'")

    return where_clause

def search_account(value):
    (where_clause := f"account_id = '{value}'")

    return where_clause


def tableSearchResults(value): # this search form needs error redirecting, or failed response built into the page

    split_value = value.split()
    print(split_value)

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

    print(jr_list)
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
    print(context)
    return context

tableSearchResults('422 beaver')