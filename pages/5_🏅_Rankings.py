import streamlit as st
import pandas as pd
from libs.dataloader import load_meta_ads, load_pesquisa, load_uploaded_ads
from libs.swag import COLUMNS_CFG_PERFORMANCE, COLUMNS_ORDER_PERFORMANCE
from libs.utils import safe_divide

st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_title='Anúncios',
    page_icon='🧲'
)

## DEFINE COLUNAS DE PERFORMANCE
COL_META_INDEX = 'ANÚNCIO: NOME'
COL_PESQUISA_INDEX = 'UTM_TERM'

## DEFINE ORDEM FINAL DAS COLUNAS
COL_ORDER = [COL_META_INDEX] + COLUMNS_ORDER_PERFORMANCE

## INICIA DATASET
df_pesquisa = (st.session_state.get('df_pesquisa', load_pesquisa())).copy()
df_meta_ads = (st.session_state.get('df_meta_ads', load_meta_ads())).copy()
df_uploaded_ads = (st.session_state.get('df_uploaded_ads', load_uploaded_ads())).copy()

## AGRUPA POR CONJUNTO
df_meta_ads = df_meta_ads.groupby(COL_META_INDEX, as_index=False).agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum',
    'ALCANCE': 'sum',
}, )

## CALCULA COLUNAS
df_meta_ads['CPL'] = safe_divide(df_meta_ads['VALOR USADO'], df_meta_ads['LEADS']).fillna(0)
df_meta_ads['CTR'] = safe_divide(df_meta_ads['CLICKS'], df_meta_ads['IMPRESSÕES']).fillna(0) * 100
df_meta_ads['CONNECT RATE'] = safe_divide(df_meta_ads['PAGEVIEWS'], df_meta_ads['CLICKS NO LINK']).fillna(0) * 100
df_meta_ads['CONVERSÃO DA PÁGINA'] = safe_divide(df_meta_ads['LEADS'], df_meta_ads['PAGEVIEWS']).fillna(0) * 100
df_meta_ads['FREQUÊNCIA'] = safe_divide(df_meta_ads['IMPRESSÕES'], df_meta_ads['ALCANCE']).fillna(0)

## CROSSTABS DE PESQUISA vs PATRIMONIO
patrimonio_relativo = pd.crosstab(df_pesquisa[COL_PESQUISA_INDEX], df_pesquisa['PATRIMÔNIO'], normalize='index')
patrimonio_relativo *= 100
patrimonio_relativo = patrimonio_relativo.round(2)
patrimonio_relativo['DISTRIBUIÇÃO'] = patrimonio_relativo.values.tolist()
patrimonio_absoluto = pd.crosstab(df_pesquisa[COL_PESQUISA_INDEX], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto['PESQUISAS'] = patrimonio_absoluto.sum(axis=1)

## ADD Nº RESPOSTAS DE PESQUISA
df_meta_ads = df_meta_ads.merge(patrimonio_absoluto[['PESQUISAS']], left_on=COL_META_INDEX, right_on=COL_PESQUISA_INDEX, how='inner')
## ORDENA COLUNAS
df_meta_ads = df_meta_ads[COL_ORDER]
## ADD % DAS FAIXAS PATRIMÔNIAIS (ao final)
df_meta_ads = df_meta_ads.merge(patrimonio_relativo, left_on=COL_META_INDEX, right_on=COL_PESQUISA_INDEX, how='inner')

# Streamlit app
col1, col2, col3 = st.columns([5,1,1])
col1.title('⚡ Performance por Anúncio')
col2.metric("Pesquisas", df_pesquisa.count()[0])
col3.metric("Anúncios", df_meta_ads.count()[0])

# FILTROS
sorted_lead_values = sorted(df_meta_ads['LEADS'].unique())
sorted_valor_usado_values = sorted(df_meta_ads['VALOR USADO'].unique())
leads_min, leads_max = st.sidebar.select_slider('Leads', options=sorted_lead_values, value=(sorted_lead_values[0], sorted_lead_values[-1]))
valor_usado_min, valor_usado_max = st.sidebar.select_slider('Valor usado', options=sorted_valor_usado_values, value=(sorted_valor_usado_values[0], sorted_valor_usado_values[-1]))

# FILTRA
df_meta_ads = df_meta_ads[(df_meta_ads['LEADS'] > leads_min) & (df_meta_ads['LEADS'] < leads_max) & (df_meta_ads['VALOR USADO'] > valor_usado_min)]


st.markdown('#')
st.dataframe(df_meta_ads.sort_values('CTR', ascending=False), column_config=COLUMNS_CFG_PERFORMANCE, use_container_width=True, hide_index=True)