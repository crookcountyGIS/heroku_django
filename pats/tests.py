from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.humanize.templatetags.humanize import intcomma
from propClasses import Attributes, Root
from propValueClasses import PvAttributes, PvRoot
from propSearchClasses import PsAttributes, PsRoot, Feature
from functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, search_all, search_account, divide_list_into_chunks
import json
import requests
import pandas as pd
import plotly.express as px
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

    # Create empty lists to append from the dataclasses
    dfList = []
    yrList = []

    # Use dataclass to capture values from JSON
    propvalue = PvRoot.from_dict(value_data)
    for f in propvalue.features:
        dfList.append(f.attributes)
        yrList.append(f.attributes.year)

    # Start creating HTML table from Pandas
    df_appended = pd.DataFrame(dfList, index=yrList).T
    df_appended = df_appended.reindex(sorted(df_appended.columns), axis=1)

    # Drop unwanted rows and make $$ values
    rows_to_drop = ['account_id', 'OBJECTID', 'year', 'county_id', 'original_tax', 'tax_code_area']
    df_filter = df_appended.drop(index=rows_to_drop)

    x_data = df_filter.keys()
    y_data = list(df_filter.loc['rmv_total', :])
    y_data2 = list(df_filter.loc['max_av', :])

    fig = px.line(x=x_data, y=y_data)
    fig.add_trace(px.line(x=x_data, y=y_data2).data[0])
    fig.update_layout(title="RMV Total and Max AV Over Time", xaxis_title="Year", yaxis_title="Value")
    #fig.show()

    chart = fig.to_html()
    #fig = px.line(df_filter, x="", y="")

    #fig.show()
    #df_filter = df_filter.applymap(lambda x: f'${intcomma(int(x))}' if isinstance(x, (int, float)) else x)

    # Rename rows
    index_mapping = {
        'rmv_land': 'Real Market Value - Land',
        'rmv_impr': 'Real Market Value - Structure',
        'rmv_total': 'Total Real Market Value',
        'total_av': 'Total Assessed Value',
        'max_av': 'Maximum Assesses Value',
        'exempt': "Veteran's Exemption"
    }

    df_filter = df_filter.rename(index=index_mapping)


    # Convert to HTML table
    html_table = df_filter.to_html(classes='table table-striped')

    # Send data over as dictionary
    json_records = df_filter.reset_index().to_json(orient='records')
    df_data = json.loads(json_records)

    context = {'account_info': prop_data,
               'value_data': value_data,
               'html_table': html_table,
               'd': df_data}


valuation(1001)