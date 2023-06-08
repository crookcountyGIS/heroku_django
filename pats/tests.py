from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px

def address_query(address):
    splitValue = address.upper().split()

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"

    # Define the query parameters
    params = {
        "where": "1=1",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }
    # Send the HTTP GET request
    table_response = requests.get(prop_url, params=params)
    # Parse the JSON response into a dictionary
    prop_data = table_response.json()

    maptaxlot = []
    dfList = []
    for elem in prop_data['features']:
        dfList.append(elem['attributes'])
        root = Root.from_dict(elem)
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    df_search = pd.DataFrame(dfList)
    query_string = ' and '.join(
        f"situs_address.str.contains('{address}', case=False, na=False)" for address in splitValue)

    filtered_df = df_search.query(query_string)
    df_table = pd.DataFrame(filtered_df,
                            columns=['map_taxlot', 'account_id', 'owner_name', 'situs_address', 'subdivision',
                                     'account_type'])

    json_records = df_table.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    print(len(df_table))

    if len(df_table) == 1:
        account_id = df_table.iloc[0]['account_id']
        print(str(account_id))
        #for result in df_table.itertuples():
        #    print(result.account_id)
       #context = {'data': prop_data, 'maptaxlot': maptaxlot}
        #return render(request, 'pats/summaryPage.html', context)
        #print(context)
    else:
        print("more than 1")

address_query('650 nw 2nd st')