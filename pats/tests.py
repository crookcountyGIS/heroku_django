from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px

def mt_query(maptaxlot):

    maptaxlot = maptaxlot[:8] + "-" + maptaxlot[8:]
    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"

    params = {
        "where": f"map_taxlot LIKE '%{maptaxlot}%'",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    prop_response = requests.get(prop_url, params=params)
    prop_data = prop_response.json()

    maptaxlot = []
    for elem in prop_data['features']:
        (root := Root.from_dict(elem))
        mt = root.attributes.map_taxlot
        (account := root.attributes.account_id)
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    print(len(prop_data['features']))

    context = {'data': prop_data, 'maptaxlot': maptaxlot}

    if len(prop_data['features']) == 1:
        print("length of 1")
        #account_query(account)
    else:
        print("length more than 1")



    #print(maptaxlot)
    #print(prop_data)
    for i in prop_data['features']:
        print(i)

mt_query('1515000000300')
#151606AB04100