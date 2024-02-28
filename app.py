import streamlit as st
import pandas as pd
import requests
import os
import json


def retrieve_data(api_key, selected_option):

    # pass the URL for the AEO data
    url_fore = f"https://api.eia.gov/v2/aeo/2023/data/?frequency=annual&data[0]=value&facets[scenario][]=ref2023&facets[seriesId][]=prce_nom_resd_NA_elc_NA_neengl_ndlrpmbtu&start=2021&end=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000https://api.eia.gov/v2/aeo/2023/data/?frequency=annual&data[0]=value&facets[scenario][]=ref2023&facets[seriesId][]=prce_nom_comm_NA_elc_NA_neengl_ndlrpmbtu&start=2022&end=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000https://api.eia.gov/v2/aeo/2023/data/?frequency=annual&data[0]=value&facets[scenario][]=ref2023&facets[seriesId][]=prce_nom_idal_NA_elc_NA_neengl_ndlrpmbtu&start=2022&end=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
    url_hist = f"https://api.eia.gov/v2/electricity/retail-sales/data/?frequency=annual&data[0]=price&facets[stateid][]=RI&facets[sectorid][]=ALL&facets[sectorid][]=COM&facets[sectorid][]=IND&facets[sectorid][]=RES&start=2001&end=2023&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
    
    # select the URL
    if selected_option == "Historical Price Data":
        url = url_hist
        filename_suffix = "Historical_"
    elif selected_option == "Forecasted Price Data":
        url = url_fore
        filename_suffix = "Forecasted_"
    else:
        st.warning("Please select a valid option.")
        return None

    # make the api request
    response = response = requests.get(url, verify=False)

    # check response codes
    if response.status_code == 403:
        st.error("The API key is incorrect. Please enter a valid API key")
        return None

    # parse the JSON from the response
    data_dict = json.loads(response.text)

    # extract data from dict -- interested in the 'response' column
    series = data_dict['response']
    data = series['data']
    data = pd.DataFrame(data)
    
    return data, filename_suffix#df_pivoted

def process_eia_data(data, selected_option):
    if selected_option == "Historical Price Data":
        # convert series to a pandas dataframe
        df = pd.DataFrame(data)
        df['price'] = df['price'].astype(float)
        df_piv = df.pivot_table(index='period', columns='sectorName', values='price')
        df_piv.reset_index(inplace=True)
        df_piv.rename(columns={"period":"year"}, inplace=True)
        df_piv.sort_values(by='year', ascending=False)
        st.subheader("Final dataset to be downloaded:")
    elif selected_option == "Forecasted Price Data":
         # convert series to a pandas dataframe
         df = pd.DataFrame(data)
         df['value'] = df['value'].astype(float)
         df_piv = df.pivot_table(index='period', columns='seriesName', values='value')
         df_piv.rename(columns={"period":"year"}, inplace=True)
         st.subheader("Final dataset to be downloaded:")

    return df_piv



def main():
    st.title("EIA Data Retrieval App")

    # Ask user for the API
    api_key = st.text_input("Enter the API key:")

    # select variable
    selected_option = st.selectbox("Select data to retrieve:", ["Historical Price Data", "Forecasted Price Data"])

    # retreive data on click
    if st.button("Retrieve Data"):
        if api_key:
            data, filename_suffix = retrieve_data(api_key, selected_option)
             

            if data is not None:
                data
                df = process_eia_data(data, selected_option)
                st.dataframe(df)
    else:
        st.warning("Please enter API key")

if __name__ == "__main__":
    main()











