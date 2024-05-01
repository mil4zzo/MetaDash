
import streamlit as st

def load_css():
    with open('style.css') as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

## ORDEM DAS COLUNAS
COLUMNS_ORDER_PERFORMANCE = [
    "LEADS",
    "PESQUISAS",
    "CPL",
    "VALOR USADO",
    "CTR",
    "CONNECT RATE",
    "CONVERSÃO DA PÁGINA",
    "FREQUÊNCIA",
    "CPM",
    "IMPRESSÕES",
    "CLICKS",
    "CLICKS NO LINK",
    "PAGEVIEWS"
]

## CONFIGURAÇÕES DAS COLUNAS
COLUMNS_CFG_PERFORMANCE = {
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
    ),
    "DISTRIBUIÇÃO": st.column_config.AreaChartColumn(
        "PATRIMÔNIO",
        help="Taxa de conversão da página de captura",
        width="medium",
        y_min=0.0,
        y_max=100.0,
    )
}