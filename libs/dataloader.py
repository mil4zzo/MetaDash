import gspread
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import unquote_plus
from libs.utils import cast_number, safe_divide

## DEFINE PLANILHA SOURCE
SHEET_NAME = "[PY] EI.17 - PESQUISA TRAFEGO"

## DEFINE ABA DOS DATASETS
SHEET_PESQUISA_TAB = "DADOS"
SHEET_ADS_META_TAB = "NEW META ADs"
SHEET_ADS_UPLOADED_TAB = "ANUNCIOS SUBIDOS"

## DEFINE COLUNAS OBRIGATÓRIAS EM CADA DATASET
COLUMNS_PESQUISA = ["PATRIMÔNIO", "DATA DA PESQUISA", "DATA DE CAPTURA", "UTM_CAMPAIGN", "UTM_SOURCE", "UTM_MEDIUM", "UTM_ADSET", "UTM_CONTENT", "UTM_TERM"]
COLUMNS_ADS_UPLOADED = ["NOME", "LINK DO DRIVE"]

## DEFINE CONSTANTES DE CALIBRAGEM
TICKET_BRUTO = 1500
TICKET_LIQUIDO = 1050
TX_CONVERSAO = [
    {
        "PATRIMÔNIO": [
            {"Acima de R$1 milhão": 0.0489},
            {"Entre R$500 mil e R$1 milhão": 0.0442},
            {"Entre R$250 mil e R$500 mil": 0.04},
            {"Entre R$100 mil e R$250 mil": 0.0382},
            {"Entre R$20 mil e R$100 mil": 0.0203},
            {"Entre R$5 mil e R$20 mil": 0.0142},
            {"Menos de R$5 mil": 0.0067}
        ]
    }
]


## CARREGA DADOS DE PLANILHA DO GOOGLE SHEETS
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


## PREPARA PLANILHA PESQUISA DE TRÁFEGO
def load_pesquisa():
    df_pesquisa = load_sheet(SHEET_NAME, SHEET_PESQUISA_TAB)
    # FILTRA COLUNAS E FORMATA VALORES
    df_pesquisa = df_pesquisa[COLUMNS_PESQUISA]
    df_pesquisa = df_pesquisa[(df_pesquisa['UTM_MEDIUM'] == 'pago') & (df_pesquisa['UTM_SOURCE'] == 'ig')]
    df_pesquisa['DATA DA PESQUISA'] = pd.to_datetime(df_pesquisa['DATA DA PESQUISA'], dayfirst=True)
    df_pesquisa['DATA DE CAPTURA'] = pd.to_datetime(df_pesquisa['DATA DE CAPTURA'], dayfirst=True)
    df_pesquisa['UTM_CAMPAIGN'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_CAMPAIGN']]
    df_pesquisa['UTM_SOURCE'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_SOURCE']]
    df_pesquisa['UTM_MEDIUM'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_MEDIUM']]
    df_pesquisa['UTM_ADSET'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_ADSET']]
    df_pesquisa['UTM_CONTENT'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_CONTENT']]
    df_pesquisa['UTM_TERM'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_TERM']]
    df_pesquisa = df_pesquisa.replace('', pd.NA).replace("{{ad.name}}", pd.NA).dropna(how="any")
    df_pesquisa.reset_index(drop=True)
    st.session_state['df_pesquisa'] = df_pesquisa
    return df_pesquisa


### PREPARA PLANILHA META ADS
def load_meta_ads():
    df_meta_ads = load_sheet(SHEET_NAME, SHEET_ADS_META_TAB)
    # FORMATA VALORES
    df_meta_ads['STATUS'] = "SEM DADOS"
    df_meta_ads['DATA'] = pd.to_datetime(df_meta_ads['DATA'], dayfirst=True)
    df_meta_ads['CAMPANHA: ID'] = df_meta_ads['CAMPANHA: ID'].astype('string')
    df_meta_ads['CAMPANHA: NOME'] = df_meta_ads['CAMPANHA: NOME'].astype('string')
    df_meta_ads['CONJUNTO: ID'] = df_meta_ads['CONJUNTO: ID'].astype('string')
    df_meta_ads['CONJUNTO: NOME'] = df_meta_ads['CONJUNTO: NOME'].astype('string')
    df_meta_ads['ANÚNCIO: ID'] = df_meta_ads['ANÚNCIO: ID'].astype('string')
    df_meta_ads['ANÚNCIO: NOME'] = df_meta_ads['ANÚNCIO: NOME'].astype('string')
    df_meta_ads['UNIQUE ID'] = df_meta_ads['UNIQUE ID'].astype('string')
    df_meta_ads['CPM'] = cast_number(df_meta_ads['CPM'], 'float32')
    df_meta_ads['VALOR USADO'] = cast_number(df_meta_ads['VALOR USADO'], 'float32')
    df_meta_ads['LEADS'] = cast_number(df_meta_ads['LEADS'], 'int32')
    df_meta_ads['CPL'] = cast_number(df_meta_ads['CPL'], 'float32')
    df_meta_ads['CTR'] = cast_number(df_meta_ads['CTR'], 'float32')
    df_meta_ads['IMPRESSÕES'] = cast_number(df_meta_ads['IMPRESSÕES'], 'int32')
    df_meta_ads['ALCANCE'] = cast_number(df_meta_ads['ALCANCE'], 'int32')
    df_meta_ads['FREQUÊNCIA'] = cast_number(df_meta_ads['FREQUÊNCIA'], 'float32')
    df_meta_ads['CLICKS'] = cast_number(df_meta_ads['CLICKS'], 'int32')
    df_meta_ads['CLICKS NO LINK'] = cast_number(df_meta_ads['CLICKS NO LINK'], 'int32')
    df_meta_ads['PAGEVIEWS'] = cast_number(df_meta_ads['PAGEVIEWS'], 'int32')
    df_meta_ads['LP CTR'] = cast_number(df_meta_ads['LP CTR'], 'float32')
    df_meta_ads['1s'] = cast_number(df_meta_ads['1s'], 'int8')
    df_meta_ads['2s'] = cast_number(df_meta_ads['2s'], 'int8')
    df_meta_ads['3s'] = cast_number(df_meta_ads['3s'], 'int8')
    df_meta_ads['4s'] = cast_number(df_meta_ads['4s'], 'int8')
    df_meta_ads['5s'] = cast_number(df_meta_ads['5s'], 'int8')
    df_meta_ads['6s'] = cast_number(df_meta_ads['6s'], 'int8')
    df_meta_ads['7s'] = cast_number(df_meta_ads['7s'], 'int8')
    df_meta_ads['8s'] = cast_number(df_meta_ads['8s'], 'int8')
    df_meta_ads['9s'] = cast_number(df_meta_ads['9s'], 'int8')
    df_meta_ads['10s'] = cast_number(df_meta_ads['10s'], 'int8')
    df_meta_ads['11s'] = cast_number(df_meta_ads['11s'], 'int8')
    df_meta_ads['12s'] = cast_number(df_meta_ads['12s'], 'int8')
    df_meta_ads['13s'] = cast_number(df_meta_ads['13s'], 'int8')
    df_meta_ads['14s'] = cast_number(df_meta_ads['14s'], 'int8')
    df_meta_ads['15-20s'] = cast_number(df_meta_ads['15-20s'], 'int8')
    df_meta_ads['20-25s'] = cast_number(df_meta_ads['20-25s'], 'int8')
    df_meta_ads['25-30s'] = cast_number(df_meta_ads['25-30s'], 'int8')
    df_meta_ads['30-40s'] = cast_number(df_meta_ads['30-40s'], 'int8')
    df_meta_ads['40-50s'] = cast_number(df_meta_ads['40-50s'], 'int8')
    df_meta_ads['50-60s'] = cast_number(df_meta_ads['50-60s'],'int8')
    df_meta_ads['60s+'] = cast_number(df_meta_ads['60s+'], 'int8')
    # CALCULA E FORMATA VALORES
    df_meta_ads['CONNECT RATE'] = safe_divide(df_meta_ads['PAGEVIEWS'], df_meta_ads['CLICKS NO LINK']).fillna(0).astype('float32')
    df_meta_ads['CONVERSÃO DA PÁGINA'] = safe_divide(df_meta_ads['LEADS'], df_meta_ads['PAGEVIEWS']).fillna(0).astype('float32')
    df_meta_ads['PERFIL CTR'] = cast_number((df_meta_ads['CTR'] - df_meta_ads['LP CTR']), 'float32')
    df_meta_ads.reset_index(drop=True)
    st.session_state['df_meta_ads'] = df_meta_ads
    return df_meta_ads

### PREPARA PLANILHA ANÚNCIOS SUBIDOS
def load_uploaded_ads():
    df_uploaded_ads = load_sheet(SHEET_NAME, SHEET_ADS_UPLOADED_TAB)
    # FILTRA COLUNAS E FORMATA VALORES
    df_uploaded_ads = df_uploaded_ads[COLUMNS_ADS_UPLOADED]
    df_uploaded_ads = df_uploaded_ads.replace('', pd.NA).dropna(how="all")
    df_uploaded_ads.reset_index(drop=True)
    st.session_state['df_uploaded_ads'] =  df_uploaded_ads
    return df_uploaded_ads