import requests
import pandas as pd
#from propSearchClasses import PsRoot
def tableSearchResults(value):

    splitValue = value.upper().split()

    propSearch_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/19/query"
    propTable_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"

    # Define the query parameters
    params = {
        "where": "1=1",  # Retrieve all records
        "outFields": "*",  # Specify the fields to include in the response
        "returnGeometry": False,  # Exclude geometry information
        "f": "json"  # Specify the response format as JSON
    }

    # Send the HTTP GET request
    search_response = requests.get(propSearch_url, params=params)
    table_response = requests.get(propTable_url, params=params)

    # Parse the JSON response into a dictionary
    search_data = search_response.json()
    table_data = table_response.json()
    #print(data)
    dfList = []
    for elem in search_data['features']:
        #print(elem['attributes'])
        dfList.append(elem['attributes'])

    df_search = pd.DataFrame(dfList)
    query_string = ' and '.join(f"search_all.str.contains('{value}', case=False, na=False)" for value in splitValue)
    filtered_df = df_search.query(query_string)
    print(filtered_df)

    dfTableList = []
    for elem in table_data['features']:
        # print(elem['attributes'])
        dfTableList.append(elem['attributes'])

    df_table = pd.DataFrame(dfTableList, columns=['map_taxlot','account_id','owner_name','situs_address','subdivision','account_type'])
    #print(df_table)

    dfjoin = filtered_df.merge(df_table, left_on='account_id', right_on='account_id')
    print(dfjoin)





tableSearchResults('smith')
# Convert the records to a Pandas DataFrame
#df = pd.DataFrame(data["features"])

# Optional: Flatten nested fields if needed
#

# Print the DataFrame
#print(df)
