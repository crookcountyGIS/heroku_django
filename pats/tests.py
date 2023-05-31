from django.shortcuts import render
#from django.http import HttpResponse
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
from propSearchClasses import PsAttributes, PsRoot, Feature
from functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, search_all, search_account, divide_list_into_chunks
import json
import requests
import pandas as pd
pd.set_option('display.max_columns', None)

def valuation(account):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/12/query"

    # Define the query parameters
    params = {
        "where": f"account_id='{account}'",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    # Send the HTTP GET request
    propValue_response = requests.get(propValue_url, params=params)
    prop_response = requests.get(prop_url, params=params)

    # Parse the JSON response into a dictionary
    value_data = propValue_response.json()
    prop_data = prop_response.json()

    #print(value_data)
    print('--------------------')
    #print(prop_data)

    # # set empty lists
    # maptaxlot = []
    dfList = []
    yrList = []
    #
    # for element in prop_data['features']:
    #     root = Root.from_dict(element)
    #     mt = root.attributes.map_taxlot
    #     mt_find = mt[:mt.find('-', mt.find('-') + 1)]
    #     maptaxlot.append(mt_find.replace('-', ''))
    #
    propvalue = PvRoot.from_dict(value_data)

    for f in propvalue.features:
        dfList.append(f.attributes)
        yrList.append(f.attributes.year)

    df_appended = pd.DataFrame(dfList, index=yrList).T
    #df = df_appended.sort_values(by='year')

    json_records = df_appended.reset_index().to_json(orient='records')
    df_data = json.loads(json_records)

    html_table = df_appended.to_html(classes='table table-striped')
    print(df_appended)

    print(df_data)

    context = {'account_info':prop_data,
               'value_data':value_data,
               'html_table': html_table,
               'd': df_data}

    #print(context)



valuation(1001)