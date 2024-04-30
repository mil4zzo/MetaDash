import streamlit as st
import pandas as pd
from libs.dataloader import load_meta_ads, load_pesquisa, load_uploaded_ads
from libs.swag import COLUMNS_CFG_PERFORMANCE, COLUMNS_ORDER_PERFORMANCE
from libs.utils import safe_divide

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Conjuntos",
    page_icon="🗂️"
)

df_pesquisa = (st.session_state.get('df_pesquisa', load_pesquisa())).copy()
df_meta_conjunto = (st.session_state.get('df_meta_ads', load_meta_ads())).copy()
df_uploaded_ads = (st.session_state.get('df_uploaded_ads', load_uploaded_ads())).copy()

df_meta_conjunto = df_meta_conjunto.groupby("CONJUNTO: NOME").agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum',
    'ALCANCE': 'sum',
})

df_meta_conjunto['CPL'] = safe_divide(df_meta_conjunto['VALOR USADO'], df_meta_conjunto['LEADS']).fillna(0)
df_meta_conjunto['CTR'] = safe_divide(df_meta_conjunto['CLICKS'], df_meta_conjunto['IMPRESSÕES']).fillna(0) * 100
df_meta_conjunto['CONNECT RATE'] = safe_divide(df_meta_conjunto['PAGEVIEWS'], df_meta_conjunto['CLICKS NO LINK']).fillna(0) * 100
df_meta_conjunto['CONVERSÃO DA PÁGINA'] = safe_divide(df_meta_conjunto['LEADS'], df_meta_conjunto['PAGEVIEWS']).fillna(0) * 100
df_meta_conjunto['FREQUÊNCIA'] = safe_divide(df_meta_conjunto['IMPRESSÕES'], df_meta_conjunto['ALCANCE']).fillna(0)

## FILTROS
df_meta_conjunto = df_meta_conjunto[(df_meta_conjunto['LEADS'] > 0)]

## CROSSTABS
patrimonio_relativo = pd.crosstab(df_pesquisa['UTM_ADSET'], df_pesquisa['PATRIMÔNIO'], normalize="index")
patrimonio_absoluto = pd.crosstab(df_pesquisa['UTM_ADSET'], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto['PESQUISAS'] = patrimonio_absoluto.sum(axis=1)

## MERGE DE %
df_meta_conjunto = df_meta_conjunto.merge(patrimonio_absoluto[['PESQUISAS']], left_on="CONJUNTO: NOME", right_index=True)
df_meta_conjunto = df_meta_conjunto[COLUMNS_ORDER_PERFORMANCE]
df_meta_conjunto = df_meta_conjunto.merge(patrimonio_relativo, left_on="CONJUNTO: NOME", right_index=True).reset_index()

# Streamlit app
st.title('📊 Dashboard')

st.markdown("## POR CONJUNTO")
st.dataframe(df_meta_conjunto, column_config=COLUMNS_CFG_PERFORMANCE, use_container_width=True, hide_index=True)