import streamlit as st
import pandas as pd


df_meta_ads = st.session_state['df_meta_ads']
df_pesquisa = st.session_state['df_pesquisa']

ctab = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'], normalize="index")
st.dataframe(ctab)

df_meta_ads = df_meta_ads.groupby("ANÚNCIO: NOME").agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum'
})
df_meta_ads['CTR'] = df_meta_ads['CLICKS'] / df_meta_ads['IMPRESSÕES'] * 100
df_meta_ads['CONNECT RATE'] = df_meta_ads['PAGEVIEWS'] / df_meta_ads['CLICKS NO LINK'] * 100
df_meta_ads['CONVERSÃO DA PÁGINA'] = df_meta_ads['LEADS'] / df_meta_ads['PAGEVIEWS'] * 100

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

df_meta_ads = df_meta_ads[col_orders_por_anuncio]

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

