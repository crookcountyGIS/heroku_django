from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def landandstructures(account):
    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"

    # Define the query parameters
    params = {
        "where": f"account_id='{account}'",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    las_params = {
        "where": f"account_id='{account}'",  # Retrieve all records
        "outFields": "account_id, description, stat_class, year_built, sqft",
        # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    prop_response = requests.get(prop_url, params=params)
    prop_data = prop_response.json()

    maptaxlot = []
    for elem in prop_data['features']:
        (root := Root.from_dict(elem))
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    las_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/8/query"

    las_response = requests.get(las_url, params=las_params)
    las_data = las_response.json()

    land_char_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/9/query"

    land_char_response = requests.get(land_char_url, params=params)
    land_char_data = land_char_response.json()
    print(land_char_data)


    # dfLandCharList = []
    # for i in land_char_data['features']:
    #     print(i)
    #     dfLandCharList.append(i['attributes'])
    #
    # dflcl = pd.DataFrame(dfLandCharList,
    #                      columns=['land_description', 'decimal_acres', 'land_classification'])
    # dflcl.columns = ['Land Description', 'Acres', 'Land Classification']
    # dfLandCharTable = dflcl.sort_values(by='Acres', ascending=False)
    #html_lcl_table = dflcl.to_html(classes='table table-dark', table_id='las_table', index=False)



landandstructures(426)