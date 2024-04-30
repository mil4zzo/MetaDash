import streamlit as st
import pandas as pd
from libs.utils import safe_divide

df_por_campanha = st.session_state['df_meta_ads'].copy()
df_pesquisa = st.session_state['df_pesquisa'].copy()

df_por_campanha['CAMPANHA: NOME'] = df_por_campanha['CAMPANHA: NOME'].str.extract(r'(LINHA\s*[123])', expand=False)
df_por_campanha = df_por_campanha.groupby("CAMPANHA: NOME").agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum'
})

df_por_campanha['CPL'] = safe_divide(df_por_campanha['VALOR USADO'], df_por_campanha['LEADS']).fillna(0)
df_por_campanha['CTR'] = safe_divide(df_por_campanha['CLICKS'], df_por_campanha['IMPRESSÕES']).fillna(0) * 100
df_por_campanha['CONNECT RATE'] = safe_divide(df_por_campanha['PAGEVIEWS'], df_por_campanha['CLICKS NO LINK']).fillna(0) * 100
df_por_campanha['CONVERSÃO DA PÁGINA'] = safe_divide(df_por_campanha['LEADS'], df_por_campanha['PAGEVIEWS']).fillna(0) * 100

## FILTROS
df_por_campanha = df_por_campanha[(df_por_campanha['LEADS'] > 0)]

## CROSSTABS
patrimonio_relativo = pd.crosstab(df_pesquisa['UTM_CAMPAIGN'], df_pesquisa['PATRIMÔNIO'], normalize="index")
patrimonio_absoluto = pd.crosstab(df_pesquisa['UTM_CAMPAIGN'], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto['PESQUISAS'] = patrimonio_absoluto.sum(axis=1)

## TRATA CAMPANHAS
index_rename_campaigns = {
    'EI.17_Captacao-L1': 'LINHA1',
    'EI.17_Captacao-L2': 'LINHA2',
    'EI.17_Captacao-L3': 'LINHA3',
}
patrimonio_relativo.rename(index_rename_campaigns, inplace=True)
patrimonio_absoluto.rename(index_rename_campaigns, inplace=True)    

## DEFINE A ORDEM DAS PRIMEIRAS COLUNAS
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

## ADD FAIXAS PATRIMÔNIAIS
df_por_campanha = df_por_campanha.merge(patrimonio_absoluto[['PESQUISAS']], left_index=True, right_index=True, how='inner')
## ORDENA COLUNAS
df_por_campanha = df_por_campanha[col_orders_por_anuncio]
## ADD RESPOSTAS DE PESQUISA
df_por_campanha = df_por_campanha.merge(patrimonio_relativo, left_index=True, right_index=True, how='inner')

columns_cfg = {
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

st.markdown("## POR CAMPANHA")
st.dataframe(df_por_campanha, column_config=columns_cfg, use_container_width=True)