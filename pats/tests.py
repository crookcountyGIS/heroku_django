from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def relatedaccounts(account):

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

    related_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/14/query"

    related_response = requests.get(related_url, params=params)
    related_data = related_response.json()

    dfRelList = []
    for elem in related_data['features']:
        print(elem)
        dfRelList.append(elem['attributes'])

    dfrel = pd.DataFrame(dfRelList,
                              columns=['realted_account_id', 'account_type', 'account_desc'])
    dfrel.columns = ['Related Account', 'Account Type', 'Account Description']
    #dfRelTable = dfrel.sort_values(by='Related Account', ascending=True)
    #html_rel_table = dfrel.to_html(classes='table table-dark', table_id='las_table', index=False)

    #context = {'data': prop_data, 'html_rel_table': html_rel_table}

    print(dfrel)

relatedaccounts(19173)
