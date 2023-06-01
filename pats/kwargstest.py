from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px

def tableSearchResults(account): # this search form needs error redirecting, or failed response built into the page

    #splitValue = value.upper().split()

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    #propSearch_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/19/query"

    # Define the query parameters
    params = {
        "where": f"account_id='{account}'",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    # Send the HTTP GET request
    #search_response = requests.get(propSearch_url, params=params)
    table_response = requests.get(prop_url, params=params)

    # Parse the JSON response into a dictionary
    #search_data = search_response.json()
    prop_data = table_response.json()

    print(prop_data)

    # dfList = []
    # for elem in search_data['features']:
    #     dfList.append(elem['attributes'])

    # df_search = pd.DataFrame(dfList)
    # query_string = ' and '.join(f"search_all.str.contains('{value}', case=False, na=False)" for value in splitValue)
    # filtered_df = df_search.query(query_string)

    # dfTableList = []
    # for elem in prop_data['features']:
    #     dfTableList.append(elem['attributes'])
    #
    # df_table = pd.DataFrame(dfTableList, columns=['map_taxlot','account_id','owner_name','situs_address','subdivision','account_type'])
    #
    # dfjoin = filtered_df.merge(df_table, left_on='account_id', right_on='account_id')
    #
    # json_records = dfjoin.reset_index().to_json(orient='records')
    # data = json.loads(json_records)

    #html_table = dfjoin.to_html(classes='table table-striped', index=False)
    #context = {'d': data}


tableSearchResults(1001)