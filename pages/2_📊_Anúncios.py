import streamlit as st
import pandas as pd
from libs.dataloader import load_meta_ads, load_pesquisa, load_uploaded_ads
from libs.swag import COLUMNS_CFG_PERFORMANCE, COLUMNS_ORDER_PERFORMANCE
from libs.utils import safe_divide

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Anúncios",
    page_icon="📊"
)

df_pesquisa = (st.session_state.get('df_pesquisa', load_pesquisa())).copy()
df_meta_anuncio = (st.session_state.get('df_meta_ads', load_meta_ads())).copy()
df_uploaded_ads = (st.session_state.get('df_uploaded_ads', load_uploaded_ads())).copy()

df_meta_anuncio = df_meta_anuncio.groupby("ANÚNCIO: NOME").agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum',
    'ALCANCE': 'sum',
})

df_meta_anuncio['CPL'] = safe_divide(df_meta_anuncio['VALOR USADO'], df_meta_anuncio['LEADS']).fillna(0)
df_meta_anuncio['CTR'] = safe_divide(df_meta_anuncio['CLICKS'], df_meta_anuncio['IMPRESSÕES']).fillna(0) * 100
df_meta_anuncio['CONNECT RATE'] = safe_divide(df_meta_anuncio['PAGEVIEWS'], df_meta_anuncio['CLICKS NO LINK']).fillna(0) * 100
df_meta_anuncio['CONVERSÃO DA PÁGINA'] = safe_divide(df_meta_anuncio['LEADS'], df_meta_anuncio['PAGEVIEWS']).fillna(0) * 100
df_meta_anuncio['FREQUÊNCIA'] = safe_divide(df_meta_anuncio['IMPRESSÕES'], df_meta_anuncio['ALCANCE']).fillna(0)

## FILTROS
df_meta_anuncio = df_meta_anuncio[(df_meta_anuncio['LEADS'] > 0)]

## CROSSTABS
patrimonio_relativo = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'], normalize="index")
patrimonio_absoluto = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto['PESQUISAS'] = patrimonio_absoluto.sum(axis=1)

## MERGE DE %
df_meta_anuncio = df_meta_anuncio.merge(patrimonio_absoluto[['PESQUISAS']], left_on="ANÚNCIO: NOME", right_index=True)
df_meta_anuncio = df_meta_anuncio[COLUMNS_ORDER_PERFORMANCE]
df_meta_anuncio = df_meta_anuncio.merge(patrimonio_relativo, left_on="ANÚNCIO: NOME", right_index=True).reset_index()

# Streamlit app
st.title('📊 Anúncios')

st.markdown("## POR ANÚNCIO")
st.dataframe(df_meta_anuncio, column_config=COLUMNS_CFG_PERFORMANCE, use_container_width=True, hide_index=True)