import streamlit as st
from data.loader import carregar_repasses
from charts.repasses import exibir_tabelas_por_lote

st.set_page_config(
    page_title="Dashboard PPE",
    layout="wide",
    page_icon="📊"
)
col1, col2 = st.columns([1, 4])  # 1 parte imagem / 4 partes título

with col1:
    st.image("imagens/logo.png", width=80)

with col2:
    st.markdown(
        "<h1 style='margin-top: 10px;'>PPE – BI Finaças</h1>",
        unsafe_allow_html=True
    )

# 1. Carrega os dados de repasse
df_repasses = carregar_repasses()

# 2. Exibe os expanders agrupados
if not df_repasses.empty:
    exibir_tabelas_por_lote(df_repasses)
else:
    st.info("ℹ️ Informações de repasses não encontradas para o Finanças.")