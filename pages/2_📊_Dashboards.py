import streamlit as st
import pandas as pd

from libs.utils import safe_divide


df_por_linha = st.session_state['df_meta_ads'].copy()
df_pesquisa = st.session_state['df_pesquisa'].copy()

# Tratar o df_Pesquisa pra adicionar uma coluna 'Linha' Baseado no UTM_CAMPAIGN
def extrair_linha(texto):
    if texto.endswith('-L1'):
        return '1'
    elif texto.endswith('-L2'):
        return '2'
    elif texto.endswith('-L3'):
        return '3'
    else:
        return 'Sem linha' 
    
 # Aplicar a função para criar a coluna 'LINHA'
df_pesquisa['LINHA'] = (df_pesquisa['UTM_CAMPAIGN']).apply(extrair_linha)    
#display(df_pesquisa)    

 # Tratar o df_por_linha pra adicionar uma colinha 'Linha' Baseado no Nome da campanha
df_por_linha['LINHA'] = df_por_linha['CAMPANHA: NOME'].str.extract(r'\[LINHA(\d+)\]')


df_por_linha = df_por_linha.reset_index()

##CRIANDO CROSSTABS
patrimonio_relativo_line = pd.crosstab(df_pesquisa['LINHA'], df_pesquisa['PATRIMÔNIO'], normalize="index")
patrimonio_absoluto_line = pd.crosstab(df_pesquisa['LINHA'], df_pesquisa['PATRIMÔNIO'])
patrimonio_absoluto_line['PESQUISAS'] = patrimonio_absoluto_line.sum(axis=1)
  
df_por_linha['TOTAL DE PESQUISA'] = patrimonio_absoluto_line['PESQUISAS']



#CRIANDO DF FINAL
df_por_linha = df_por_linha.groupby('LINHA').agg({
    'LEADS': 'sum',
    'VALOR USADO': 'sum',
    'CPM': 'mean',
    'IMPRESSÕES': 'sum',
    'CLICKS': 'sum',
    'CLICKS NO LINK': 'sum',
    'PAGEVIEWS': 'sum',
}) 


df_por_linha = df_por_linha.merge(patrimonio_relativo_line, left_on='LINHA', right_on='LINHA')
df_por_linha = df_por_linha.merge(patrimonio_absoluto_line['PESQUISAS'], left_on='LINHA', right_on='LINHA')
df_por_linha['PREÇO ATUAL CUSTO POR LEAD'] = safe_divide(df_por_linha['VALOR USADO'], df_por_linha['LEADS']).fillna(0)
#df_por_linha['PREÇO MÁXIMO'] = formula
df_por_linha['CONNECT RATE'] = safe_divide(df_por_linha['PAGEVIEWS'], df_por_linha['CLICKS NO LINK']).fillna(0) * 100
df_por_linha['CTR'] = safe_divide(df_por_linha['CLICKS'], df_por_linha['IMPRESSÕES']).fillna(0) * 100
df_por_linha['CONVERSÃO DA PÁGINA'] = safe_divide(df_por_linha['LEADS'], df_por_linha['PAGEVIEWS']).fillna(0) * 100
df_por_linha['TAXA DE RESPOSTA'] = safe_divide(df_por_linha['PESQUISAS'], df_por_linha['LEADS']).fillna(0) * 100

#STREAMLIT

colcfg_por_linha = {
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
st.dataframe(df_por_linha, column_config=colcfg_por_linha, use_container_width=True)


