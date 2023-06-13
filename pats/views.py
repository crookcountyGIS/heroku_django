from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px


def base(request):
    return render(request, 'pats/base.html')


def index(request):
    return render(request, 'pats/index.html')


def mapPage(request):
    return render(request, 'pats/mapPage.html')


def tableSearchResults(request,
                       value):  # this search form needs error redirecting, or failed response built into the page

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

    df_table = pd.DataFrame(dfTableList,
                            columns=['map_taxlot', 'account_id', 'owner_name', 'situs_address', 'subdivision',
                                     'account_type'])

    dfjoin = filtered_df.merge(df_table, left_on='account_id', right_on='account_id')

    json_records = dfjoin.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    context = {'d': data, 'search_term': value}

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
    x_data = df_filter.keys()
    y_data = list(df_filter.loc['rmv_total', :])
    y_data2 = list(df_filter.loc['max_av', :])

    fig = px.line(x=x_data, y=y_data)
    fig.add_trace(px.line(x=x_data, y=y_data2).data[0])
    fig.update_layout(title="Total Real Market Value and Maximum Assessed Value Over Time", xaxis_title="Year",
                      yaxis_title="Value")
    # fig.show()
    chart = fig.to_html()

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
    html_table = df_filter.to_html(classes='table table-light table-striped', table_id='val_table')

    # Send data over as dictionary
    json_records = df_filter.reset_index().to_json(orient='records')
    df_data = json.loads(json_records)

    context = {'account_info': prop_data,
               'value_data': value_data,
               'html_table': html_table,
               'd': df_data,
               'chart': chart}

    return render(request, 'pats/valuation.html', context)


def account_query(request, account):
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

    context = {'data': prop_data, 'maptaxlot': maptaxlot}

    if root.attributes.account_type == 'Real':
        return render(request, 'pats/summaryPageV2.html', context)

    elif root.attributes.account_type == 'M/S':
        return render(request, 'pats/summaryPageMS.html', context)

    elif root.attributes.account_type == 'P/P':
        return render(request, 'pats/summaryPagePP.html', context)

    elif root.attributes.account_type == 'UTIL':
        return render(request, 'pats/summaryPageUTIL.html', context)

    else:
        return render(request, 'pats/summaryPageV2.html', context)


def mt_query(request, maptaxlot):
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
    dfTableList = []
    for elem in prop_data['features']:
        dfTableList.append(elem['attributes'])
        root = Root.from_dict(elem)
        mt = root.attributes.map_taxlot
        mt_find = mt[:mt.find('-', mt.find('-') + 1)]
        maptaxlot.append(mt_find.replace('-', ''))

    df_table = pd.DataFrame(dfTableList,
                            columns=['map_taxlot', 'account_id', 'owner_name', 'situs_address', 'subdivision',
                                     'account_type'])

    json_records = df_table.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    if len(df_table) == 1:
        account_id = df_table.iloc[0]['account_id']
        return redirect('account_query', account=account_id)

    else:
        context = {'d': data, 'search_term': maptaxlot}
        return render(request, 'pats/searchResults.html', context)


def owner_query(request, name):
    splitValue = name.upper().split()

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
    query_string = ' and '.join(f"owner_name.str.contains('{name}', case=False, na=False)" for name in splitValue)

    filtered_df = df_search.query(query_string)
    df_table = pd.DataFrame(filtered_df,
                            columns=['map_taxlot', 'account_id', 'owner_name', 'situs_address', 'subdivision',
                                     'account_type'])

    json_records = df_table.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    if len(df_table) == 1:
        account_id = df_table.iloc[0]['account_id']
        return redirect('account_query', account=account_id)

    else:
        context = {'d': data}
        return render(request, 'pats/searchResults.html', context)


def address_query(request, address):
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

    if len(df_table) == 1:
        account_id = df_table.iloc[0]['account_id']
        return redirect('account_query', account=account_id)

    else:
        context = {'d': data}
        return render(request, 'pats/searchResults.html', context)








