import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from urllib.parse import unquote_plus

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Início",
    page_icon="💎"
)

# DEFINE PLANILHA SOURCE E ABAS
SHEET_NAME = "EI.17 - PESQUISA TRAFEGO"
SHEET_PESQUISA_TAB = "DADOS"
SHEET_ADS_META_TAB = "NEW META ADs"
SHEET_ADS_UPLOADED_TAB = "ANUNCIOS SUBIDOS"

# DEFINE COLUNAS OBRIGATÓRIAS
COLUMNS_PESQUISA = ["PATRIMÔNIO", "DATA DA PESQUISA", "DATA DE CAPTURA", "UTM_CAMPAIGN", "UTM_SOURCE", "UTM_MEDIUM", "UTM_ADSET", "UTM_CONTENT", "UTM_TERM"]
COLUMNS_ADS_UPLOADED = ["NOME", "LINK DO DRIVE"]

# INICIA CONSTANTES
TICKET_BRUTO = 1500
TICKET_LIQUIDO = 1050
TX_CONVERSAO = [
    {
        "pergunta": "PATRIMÔNIO",
        "conversoes": [
            {"resposta": "Acima de R$1 milhão", "taxa": 0.0489},
            {"resposta": "Entre R$500 mil e R$1 milhão", "taxa": 0.0442},
            {"resposta": "Entre R$250 mil e R$500 mil", "taxa": 0.04},
            {"resposta": "Entre R$100 mil e R$250 mil", "taxa": 0.0382},
            {"resposta": "Entre R$20 mil e R$100 mil", "taxa": 0.0203},
            {"resposta": "Entre R$5 mil e R$20 mil", "taxa": 0.0142},
            {"resposta": "Menos de R$5 mil", "taxa": 0.0067}
        ]
    }
]

# Function to authenticate and access the spreadsheet
@st.cache_data(show_spinner="Carregando dados...", ttl=9000)
def load_sheet(sheet_name, worksheet_name):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('metadash-gcsac.json', scope)
    client = gspread.authorize(creds)
    
    # Open the Google spreadsheet
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    
    # Get all data from the sheet
    data = sheet.get_all_records()

    return pd.DataFrame(data)

# Load the data
df_pesquisa = load_sheet(SHEET_NAME, SHEET_PESQUISA_TAB)
df_meta_ads = load_sheet(SHEET_NAME, SHEET_ADS_META_TAB)
df_uploaded_ads = load_sheet(SHEET_NAME, SHEET_ADS_UPLOADED_TAB)

# FORMATA DADOS PESQUISA
df_pesquisa = df_pesquisa[COLUMNS_PESQUISA]
df_pesquisa["PATRIMÔNIO"] = df_pesquisa["PATRIMÔNIO"].astype("string")
df_pesquisa['DATA DA PESQUISA'] = pd.to_datetime(df_pesquisa['DATA DA PESQUISA'])
df_pesquisa['DATA DE CAPTURA'] = pd.to_datetime(df_pesquisa['DATA DE CAPTURA'])
df_pesquisa["UTM_CAMPAIGN"] = df_pesquisa["UTM_CAMPAIGN"].astype("string")
df_pesquisa["UTM_SOURCE"] = df_pesquisa["UTM_SOURCE"].astype("string")
df_pesquisa["UTM_MEDIUM"] = df_pesquisa["UTM_MEDIUM"].astype("string")
df_pesquisa["UTM_CONTENT"] = df_pesquisa["UTM_CONTENT"].astype("string")
df_pesquisa['UTM_ADSET'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_ADSET']]
df_pesquisa['UTM_ADSET'] = df_pesquisa['UTM_ADSET'].astype('string')
df_pesquisa['UTM_TERM'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_TERM']]
df_pesquisa['UTM_TERM'] = df_pesquisa['UTM_TERM'].astype('string')

df_pesquisa.dtypes

# FORMATA DADOS ANÚNCIOS SUBIDOS
df_uploaded_ads = df_uploaded_ads[COLUMNS_ADS_UPLOADED]
df_uploaded_ads = df_uploaded_ads.replace('', pd.NA).dropna(how="all")

st.session_state['df_pesquisa'] = df_pesquisa
st.session_state['df_meta_ads'] = df_meta_ads
st.session_state['df_uploaded_ads'] = df_uploaded_ads

# Streamlit app
st.title('💎 Início')

st.markdown("## DADOS PESQUISA")
st.dataframe(df_pesquisa, use_container_width=True)

st.markdown("## META ADS")
st.dataframe(df_meta_ads, use_container_width=True)

st.markdown("## ANUNCIOS SUBIDOS")
st.dataframe(df_uploaded_ads, use_container_width=True)

st.sidebar.write(f"Ticket bruto: {TICKET_BRUTO}")
st.sidebar.write(f"Ticket liquido: {TICKET_LIQUIDO}")
st.sidebar.table(pd.DataFrame(TX_CONVERSAO[0]['conversoes']).style.format({"taxa": "{:.2%}"}))