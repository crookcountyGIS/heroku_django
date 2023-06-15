from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def account_query(account):
    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"

    # Define the query parameters
    params = {
        "where": f"account_id='{account}'",  # Retrieve all records
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
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    zoning_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/18/query"

    # Define the query parameters
    zoning_params = {
        "where": f"maptaxlot='{maptaxlot[0]}'",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    zoning_response = requests.get(zoning_url, params=zoning_params)
    zoning_data = zoning_response.json()

    for zones in zoning_data['features']:
        (zone := zones['attributes']['zone'])
        (zone_desc := zones['attributes']['zone_desc'])
        (zone_link := zones['attributes']['zone_link'])

    print(prop_data)
    #print(zone)
    #context = {'data': prop_data, 'maptaxlot': maptaxlot, 'zone': zone, 'zone_desc': zone_desc, 'zone_link': zone_link}

account_query(80000)