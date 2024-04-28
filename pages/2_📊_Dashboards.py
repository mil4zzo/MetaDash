import streamlit as st
import pandas as pd

from libs.utils import safe_divide

df_por_anuncio = st.session_state['df_meta_ads']
df_pesquisa = st.session_state['df_pesquisa']

df_por_anuncio = df_por_anuncio.groupby("ANÚNCIO: NOME").agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum'
})

df_por_anuncio['CTR'] = safe_divide(df_por_anuncio['CLICKS'], df_por_anuncio['IMPRESSÕES']) * 100
df_por_anuncio['CONNECT RATE'] = safe_divide(df_por_anuncio['PAGEVIEWS'], df_por_anuncio['CLICKS NO LINK']) * 100
df_por_anuncio['CONVERSÃO DA PÁGINA'] = safe_divide(df_por_anuncio['LEADS'], df_por_anuncio['PAGEVIEWS']) * 100

col_orders_por_anuncio = [
    "LEADS",
    "VALOR USADO",
    "CTR",
    "CONNECT RATE",
    "CONVERSÃO DA PÁGINA",
    "CPM",
    "IMPRESSÕES",
    "CLICKS",
    "CLICKS NO LINK",
    "PAGEVIEWS"
]

df_por_anuncio = df_por_anuncio[col_orders_por_anuncio].reset_index()

patrimonio_absoluto = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'])
patrimonio_relativo = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'], normalize="index")

df_meta_ads = df_por_anuncio.merge(patrimonio_relativo, left_on="ANÚNCIO: NOME", right_on="UTM_TERM" )

colcfg_por_anuncio = {
        "VALOR USADO": st.column_config.NumberColumn(
            "💲 VALOR USADO",
            help="Total investido em tráfego",
            format="R$ %.2f",
        ),
        "CPM": st.column_config.NumberColumn(
            "💲 CPM",
            help="Custo médio por 1000 impressões",
            format="R$ %.2f",
        ),
        "CTR": st.column_config.NumberColumn(
            "➡️ CTR",
            help="Click rate",
            format="%.2f %%",
        ),
        "CONNECT RATE": st.column_config.NumberColumn(
            "➡️ CONNECT RATE",
            help="% que chega à página após clicar no link do anúncio",
            format="%.2f %%",
        ),
        "CONVERSÃO DA PÁGINA": st.column_config.NumberColumn(
            "➡️ CONVERSÃO DA PÁGINA",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
        )
    }

# Streamlit app
st.title('📊 Dashboard')

st.markdown("## POR ANÚNCIO")
st.dataframe(df_meta_ads, column_config=colcfg_por_anuncio, use_container_width=True)

