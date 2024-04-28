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

df_por_anuncio['CPL'] = safe_divide(df_por_anuncio['VALOR USADO'], df_por_anuncio['LEADS']).fillna(0)
df_por_anuncio['CTR'] = safe_divide(df_por_anuncio['CLICKS'], df_por_anuncio['IMPRESSÕES']).fillna(0) * 100
df_por_anuncio['CONNECT RATE'] = safe_divide(df_por_anuncio['PAGEVIEWS'], df_por_anuncio['CLICKS NO LINK']).fillna(0) * 100
df_por_anuncio['CONVERSÃO DA PÁGINA'] = safe_divide(df_por_anuncio['LEADS'], df_por_anuncio['PAGEVIEWS']).fillna(0) * 100

## FILTROS
df_por_anuncio = df_por_anuncio[(df_por_anuncio['LEADS'] > 0)]

## CROSSTABS
patrimonio_relativo = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'], normalize="index")
patrimonio_absoluto = pd.crosstab(df_pesquisa['UTM_TERM'], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto['PESQUISAS'] = patrimonio_absoluto.sum(axis=1)

## ORDEM DAS COLUNAS
col_orders_por_anuncio = [
    "LEADS",
    "PESQUISAS",
    "CPL",
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

## MERGE DE %
df_por_anuncio = df_por_anuncio.merge(patrimonio_absoluto[['PESQUISAS']], left_on="ANÚNCIO: NOME", right_index=True)
df_por_anuncio = df_por_anuncio[col_orders_por_anuncio]
df_por_anuncio = df_por_anuncio.merge(patrimonio_relativo, left_on="ANÚNCIO: NOME", right_index=True).reset_index()

headers = {
    'selector': 'th',
    'props': 'background-color: red; color: white;'
}

colcfg_por_anuncio = {
        "CPL": st.column_config.NumberColumn(
            "💲 CPL",
            help="Total investido em tráfego",
            format="R$ %.2f",
        ),
        "VALOR USADO": st.column_config.NumberColumn(
            "💲 VALOR USADO",
            help="Total investido em tráfego",
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
            help="% que chega à página após clicar no link do anúncio",
            format="%.2f %%",
        ),
        "CPM": st.column_config.NumberColumn(
            "💲 CPM",
            help="Custo médio por 1000 impressões",
            format="R$ %.2f",
        ),
        "Acima de R$1 milhão": st.column_config.NumberColumn(
            "⭐ +1MM",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Entre R$500 mil e R$1 milhão": st.column_config.NumberColumn(
            "⭐ 500k - 1MM",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Entre R$250 mil e R$500 mil": st.column_config.NumberColumn(
            "⭐ 250k - 500k",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Entre R$100 mil e R$250 mil": st.column_config.NumberColumn(
            "⭐ 100k - 250k",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Entre R$20 mil e R$100 mil": st.column_config.NumberColumn(
            "⭐ 20k - 100k",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Entre R$5 mil e R$20 mil": st.column_config.NumberColumn(
            "⭐ 5k - 20k",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        ),
        "Menos de R$5 mil": st.column_config.NumberColumn(
            "⭐ 0 - 5k",
            help="Taxa de conversão da página de captura",
            format="%.2f %%",
            width="small"
        )
    }

# Streamlit app
st.title('📊 Dashboard')

st.markdown("## POR ANÚNCIO")
st.dataframe(df_por_anuncio, column_config=colcfg_por_anuncio, use_container_width=True)