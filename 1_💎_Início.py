import streamlit as st
from libs.dataloader import TICKET_BRUTO, TICKET_LIQUIDO, TX_CONVERSAO, load_meta_ads, load_pesquisa, load_uploaded_ads

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Início",
    page_icon="💎"
)

df_pesquisa = st.session_state.get('df_pesquisa', load_pesquisa())
df_meta = st.session_state.get('df_meta_ads', load_meta_ads())
df_uploaded_ads = st.session_state.get('df_uploaded_ads', load_uploaded_ads())

# Streamlit app
st.title('💎 Início')

st.markdown("## DADOS PESQUISA")
st.dataframe(df_pesquisa, use_container_width=True)

st.markdown("## META ADS")
st.dataframe(df_meta, use_container_width=True)

st.markdown("## ANUNCIOS SUBIDOS")
st.dataframe(df_uploaded_ads, use_container_width=True)

st.sidebar.write(f"Ticket bruto: {TICKET_BRUTO}")
st.sidebar.write(f"Ticket liquido: {TICKET_LIQUIDO}")
#st.sidebar.table(pd.DataFrame(TX_CONVERSAO[0]['conversoes']).style.format({"taxa": "{:.2%}"}))