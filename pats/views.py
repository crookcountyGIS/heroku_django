from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
#from django.http import HttpResponse
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
from pats.propSearchClasses import PsAttributes, PsRoot, Feature
from pats.functions import is_string_numbers, is_string_letters, is_string_alphanumeric, is_address, search_all, search_account, divide_list_into_chunks
import json
import requests
import pandas as pd

def base(request):

    return render(request, 'pats/base.html')

def index(request):

    return render(request, 'pats/index.html')
    
def mapPage(request):
        
    return render(request, 'pats/mapPage.html')

def tableSearchResults(request, value): # this search form needs error redirecting, or failed response built into the page

    splitValue = value.upper().split()

    prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
    propSearch_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/19/query"

    # Define the query parameters
    params = {
        "where": "1=1",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    # Send the HTTP GET request
    search_response = requests.get(propSearch_url, params=params)
    table_response = requests.get(prop_url, params=params)

    # Parse the JSON response into a dictionary
    search_data = search_response.json()
    prop_data = table_response.json()

    dfList = []
    for elem in search_data['features']:
        dfList.append(elem['attributes'])

    df_search = pd.DataFrame(dfList)
    query_string = ' and '.join(f"search_all.str.contains('{value}', case=False, na=False)" for value in splitValue)
    filtered_df = df_search.query(query_string)

    dfTableList = []
    for elem in prop_data['features']:
        dfTableList.append(elem['attributes'])

    df_table = pd.DataFrame(dfTableList, columns=['map_taxlot','account_id','owner_name','situs_address','subdivision','account_type'])

    dfjoin = filtered_df.merge(df_table, left_on='account_id', right_on='account_id')

    json_records = dfjoin.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    #html_table = dfjoin.to_html(classes='table table-striped', index=False)
    context = {'d': data}

    return render(request, 'pats/searchResults.html', context)

def valuation(request, account):

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
    df_filter = df_filter.applymap(lambda x: f'${intcomma(int(x))}' if isinstance(x, (int, float)) else x)

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

    return render(request, 'pats/valuation.html', context)

# def valuation(request, account):

#     prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
#     propValue_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/12/query"

#     #where_clause = f"account_id = {account}"
#     where_clause = regex_filter(account)
#     out_fields = "*"
#     return_geometry = "false"
#     f = "pjson"

#     url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
#     url_value = f"{propValue_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

#     # set variables
#     response = requests.get(url)
#     responseValue = requests.get(url_value)
#     jsonResponse = response.json()
#     jsonValueResponse = responseValue.json()

#     # set empty lists
#     maptaxlot = []

#     for element in jsonResponse['features']:
#         root = Root.from_dict(element)
#         mt = root.attributes.map_taxlot
#         mt_find = mt[:mt.find('-', mt.find('-') + 1)]
#         maptaxlot.append(mt_find.replace('-', ''))
        

#     # set empty dictionaries
#     real_market_value = {}
#     value_structure = {}
#     total_real_market = {}
#     max_assessed = {}
#     total_assessed = {}
#     veterans = {}
#     year_list = [2018, 2019, 2020, 2021, 2022]

#     # ----------- under construction ---------
#     for element in jsonValueResponse['features']:
#         value_root = PvRoot.from_dict(element)
        

#         #if feature['attributes']['year'] == yr:
#             # real_market_value[yr] = feature['attributes']['rmv_land']
#             # value_structure[yr] = feature['attributes']['rmv_impr']
#             # total_real_market[yr] = feature['attributes']['rmv_total']
#             # max_assessed[yr] = feature['attributes']['max_av']
#             # total_assessed[yr] = feature['attributes']['total_av']
#             # veterans[yr] = feature['attributes']['exempt']


#     context = {'data':jsonResponse, 
#     'value_data':jsonValueResponse, 
#     'maptaxlot': maptaxlot,
#     'value_structure':value_structure, 
#     'max_assessed':max_assessed, 
#     'real_market_value':real_market_value, 
#     'total_real_market':total_real_market, 
#     'total_assessed':total_assessed, 
#     'veterans':veterans}
#     # ----------- under construction ---------
    
#     return render(request, 'pats/valuation.html', context)

def account_query(request, account):

    base_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    where_clause = f"account_id = {account}"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    url = f"{base_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    response = requests.get(url)
    jsonResponse = response.json()

    maptaxlot = []
    structure = []
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                mt = feature['attributes']['map_taxlot']
                mt_find = mt[:mt.find('-', mt.find('-') + 1)]
                maptaxlot.append(mt_find.replace('-', ''))

    context = {'data':jsonResponse, 'maptaxlot': maptaxlot}

    return render(request, 'pats/summaryPage.html', context)


