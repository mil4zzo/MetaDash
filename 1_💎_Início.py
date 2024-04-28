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
SHEET_NAME = "[PY] EI.17 - PESQUISA TRAFEGO"
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

# CARREGA DADOS DE GOOGLE SHEETS
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

# CARREGA PLANILHAS #
df_pesquisa = load_sheet(SHEET_NAME, SHEET_PESQUISA_TAB)
df_meta_ads = load_sheet(SHEET_NAME, SHEET_ADS_META_TAB)
df_uploaded_ads = load_sheet(SHEET_NAME, SHEET_ADS_UPLOADED_TAB)

### PESQUISA DE TRÁFEGO ###
# FILTRA COLUNAS E FORMATA VALORES
df_pesquisa = df_pesquisa[COLUMNS_PESQUISA]
df_pesquisa = df_pesquisa[(df_pesquisa['UTM_MEDIUM'] == 'pago') & (df_pesquisa['UTM_SOURCE'] == 'ig')]
df_pesquisa['DATA DA PESQUISA'] = pd.to_datetime(df_pesquisa['DATA DA PESQUISA'])
df_pesquisa['DATA DE CAPTURA'] = pd.to_datetime(df_pesquisa['DATA DE CAPTURA'])
df_pesquisa['UTM_CAMPAIGN'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_CAMPAIGN']]
df_pesquisa['UTM_SOURCE'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_SOURCE']]
df_pesquisa['UTM_MEDIUM'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_MEDIUM']]
df_pesquisa['UTM_ADSET'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_ADSET']]
df_pesquisa['UTM_CONTENT'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_CONTENT']]
df_pesquisa['UTM_TERM'] = [unquote_plus(x) if isinstance(x, str) else x for x in df_pesquisa['UTM_TERM']]
df_pesquisa = df_pesquisa.replace('', pd.NA).replace("{{ad.name}}", pd.NA).dropna(how="any")
df_pesquisa.reset_index(drop=True)

### META ADS ###
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
df_meta_ads['CPM'] = pd.to_numeric(df_meta_ads['CPM'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['VALOR USADO'] = pd.to_numeric(df_meta_ads['VALOR USADO'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['LEADS'] = pd.to_numeric(df_meta_ads['LEADS'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['CPL'] = pd.to_numeric(df_meta_ads['CPL'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['CTR'] = pd.to_numeric(df_meta_ads['CTR'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['IMPRESSÕES'] = pd.to_numeric(df_meta_ads['IMPRESSÕES'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['ALCANCE'] = pd.to_numeric(df_meta_ads['ALCANCE'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['FREQUÊNCIA'] = pd.to_numeric(df_meta_ads['FREQUÊNCIA'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['CLICKS'] = pd.to_numeric(df_meta_ads['CLICKS'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['CLICKS NO LINK'] = pd.to_numeric(df_meta_ads['CLICKS NO LINK'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['PAGEVIEWS'] = pd.to_numeric(df_meta_ads['PAGEVIEWS'], errors='coerce').fillna(0).astype('int32')
df_meta_ads['LP CTR'] = pd.to_numeric(df_meta_ads['LP CTR'], errors='coerce').fillna(0).astype('float32')
df_meta_ads['1s'] = pd.to_numeric(df_meta_ads['1s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['2s'] = pd.to_numeric(df_meta_ads['2s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['3s'] = pd.to_numeric(df_meta_ads['3s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['4s'] = pd.to_numeric(df_meta_ads['4s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['5s'] = pd.to_numeric(df_meta_ads['5s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['6s'] = pd.to_numeric(df_meta_ads['6s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['7s'] = pd.to_numeric(df_meta_ads['7s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['8s'] = pd.to_numeric(df_meta_ads['8s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['9s'] = pd.to_numeric(df_meta_ads['9s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['10s'] = pd.to_numeric(df_meta_ads['10s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['11s'] = pd.to_numeric(df_meta_ads['11s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['12s'] = pd.to_numeric(df_meta_ads['12s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['13s'] = pd.to_numeric(df_meta_ads['13s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['14s'] = pd.to_numeric(df_meta_ads['14s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['15-20s'] = pd.to_numeric(df_meta_ads['15-20s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['20-25s'] = pd.to_numeric(df_meta_ads['20-25s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['25-30s'] = pd.to_numeric(df_meta_ads['25-30s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['30-40s'] = pd.to_numeric(df_meta_ads['30-40s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['40-50s'] = pd.to_numeric(df_meta_ads['40-50s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['50-60s'] = pd.to_numeric(df_meta_ads['50-60s'], errors='coerce').fillna(0).astype('int8')
df_meta_ads['60s+'] = pd.to_numeric(df_meta_ads['60s+'], errors='coerce').fillna(0).astype('int8')
# CALCULA E FORMATA VALORES
df_meta_ads['CONNECT RATE'] = (df_meta_ads['PAGEVIEWS'] / df_meta_ads['CLICKS NO LINK'].replace(0, pd.NA).fillna(0)).astype('float32')
df_meta_ads['CONVERSÃO DA PÁGINA'] = (df_meta_ads['LEADS'] / df_meta_ads['PAGEVIEWS'].replace(0, pd.NA).fillna(0)).astype('float32')
df_meta_ads['PERFIL CTR'] = (df_meta_ads['CTR'] - df_meta_ads['LP CTR']).astype('float32')
df_meta_ads.reset_index(drop=True)
# CONFIGURA COLUNAS
""" column_cfg_meta_ads={
        "STATUS": st.column_config.SelectboxColumn(
            "💡 Status",
            help="Status do anúncio",
            width="medium",
            options=[
                "ATIVO",
                "PAUSADO",
                "REJEITADO",
                "SEM DADOS"
            ],
            required=False,
        )
} """


### ANÚNCIOS SUBIDOS ###
# FILTRA COLUNAS E FORMATA VALORES
df_uploaded_ads = df_uploaded_ads[COLUMNS_ADS_UPLOADED]
df_uploaded_ads = df_uploaded_ads.replace('', pd.NA).dropna(how="all")
df_uploaded_ads.reset_index(drop=True)

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