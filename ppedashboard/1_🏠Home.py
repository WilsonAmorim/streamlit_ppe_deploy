import streamlit as st
from datetime import datetime
import pandas as pd



st.set_page_config(
    page_title="Dashboard PPE",
    layout="wide",
    page_icon="📊"
)


st.sidebar.markdown("Desenvolvido por Wilson Amorim  SAEB/SGI/PPE")

st.markdown(
    """
    O Aplicatico de Dashboard PPE visa fornecer insights valiosos sobre os convênios
    firmados pelo PPE ao longo dos anos. Com uma interface interativa e visualizações
    dinâmicas, este dashboard permite aos usuários explorar dados detalhados sobre os
    convênios, facilitando a análise de tendências, desempenho e impacto dessas parcerias.
    
"""
)