import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(layout="wide")

# Function to authenticate and access the spreadsheet
def load_data():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('metadash-gcsac.json', scope)
    client = gspread.authorize(creds)
    
    # Open the Google spreadsheet
    sheet = client.open('EI.17 - ADS ANALYTICS').worksheet('META ADs')  # Replace with your actual sheet name
    
    # Get all data from the sheet
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Load the data
df = load_data()

# Streamlit app
st.title('EI.17 - Dados da pesquisa de tráfego')
st.dataframe(df)  # Display the dataframe as a tables

df = pd.to_numeric(df['CLICKS'], errors='coerce').dropna()