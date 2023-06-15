from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    df_rmv_av = df_filter.iloc[2:4, :]
    df_chart = df_rmv_av.T
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_chart.index,
        y=df_chart['rmv_total'],
        mode='lines+markers+text',  # Add 'markers' mode to display markers
        name='RMV Total',
        line=dict(color='#4300F0', width=3, dash='dash'),
        marker=dict(color='#4300F0', size=8),  # Marker color and size
        text=df_chart.rmv_total
    ))

    fig.add_trace(go.Scatter(
        x=df_chart.index,
        y=df_chart['total_av'],
        mode='lines+markers+text',  # Add 'markers' mode to display markers
        name='AV Total',
        line=dict(color='#18F02E', width=3, dash='dash'),
        marker=dict(color='#18F02E', size=8),  # Marker color and size
        text=df_chart.total_av
    ))

    fig.update_layout(margin=dict(l=5, r=5, t=50, b=5),
                      title="Total Real Market Value and Total Assessed Value Over Time", xaxis_title="Year",
                      yaxis_title="Value")
    fig.update_traces(textposition="bottom right", texttemplate='%{text:$,.0f}',
                      hovertemplate='%{text:$,.0f}<br />%{x}',
                      selector=dict(type='scatter'))
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
    html_table = df_filter.to_html(classes='table table-dark table-striped', table_id='val_table')

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

    if root.attributes.account_type == 'UTIL':
        (context := {'data': prop_data})
    else:
        (context := {'data': prop_data, 'maptaxlot': maptaxlot, 'zone': zone, 'zone_desc': zone_desc, 'zone_link': zone_link})

    if root.attributes.account_type == 'Real':
        return render(request, 'pats/summaryPage.html', context)

    elif root.attributes.account_type == 'M/S':
        return render(request, 'pats/summaryPageMS.html', context)

    elif root.attributes.account_type == 'P/P':
        return render(request, 'pats/summaryPagePP.html', context)

    elif root.attributes.account_type == 'UTIL':
        return render(request, 'pats/summaryPageUTIL.html', context)

    else:
        return render(request, 'pats/summaryPage.html', context)


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

def landandstructures(request, account):
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

    las_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/8/query"

    las_response = requests.get(las_url, params=params)
    las_data = las_response.json()

    dfLasList = []
    for elem in las_data['features']:
        print(elem)
        dfLasList.append(elem['attributes'])

    dflt = pd.DataFrame(dfLasList,
                              columns=['description', 'stat_class', 'year_built', 'sqft'])
    dflt.columns = ['Description', 'Stat Class', 'Year Built', 'SQFT']
    dfLasTable = dflt.sort_values(by='SQFT', ascending=False)
    html_las_table = dfLasTable.to_html(classes='table table-dark table-striped', table_id='las_table', index=False)

    land_char_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/9/query"

    land_char_response = requests.get(land_char_url, params=params)
    land_char_data = land_char_response.json()

    dfLandCharList = []
    for elem in land_char_data['features']:
        dfLandCharList.append(elem['attributes'])

    dflcl = pd.DataFrame(dfLandCharList,
                        columns=['land_description', 'decimal_acres', 'land_classification'])
    dflcl.columns = ['Land Description', 'Acres', 'Land Classification']
    #dfLandCharTable = dflcl.sort_values(by='Acres', ascending=False)
    html_lcl_table = dflcl.to_html(classes='table table-dark table-striped', table_id='las_table', index=False)


    context = {'data': prop_data, 'html_las_table': html_las_table, 'html_lcl_table': html_lcl_table}

    return render(request, 'pats/landandstructures.html', context)

def relatedaccounts(request, account):

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

    dfPropList = []
    for elem in prop_data['features']:
        dfPropList.append(elem['attributes'])

    dfprop = pd.DataFrame(dfPropList,
                         columns=['account_id', 'owner_name'])


    related_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/14/query"

    related_response = requests.get(related_url, params=params)
    related_data = related_response.json()

    dfRelList = []
    for elem in related_data['features']:
        #print(elem)
        dfRelList.append(elem['attributes'])

    dfrel = pd.DataFrame(dfRelList,
                              columns=['realted_account_id', 'account_type', 'account_desc'])
    dfrel.columns = ['Related Account', 'Account Type', 'Account Description']
    dfRelTable = dfrel.sort_values(by='Related Account', ascending=True)

    dfjoin = dfRelTable.merge(dfprop, left_on='Related Account', right_on='account_id', how='left')

    html_rel_table = dfjoin.to_html(classes='table table-dark table-striped', table_id='las_table', index=False)

    context = {'data': prop_data, 'html_rel_table': html_rel_table}

    return render(request, 'pats/relatedaccounts.html', context)







