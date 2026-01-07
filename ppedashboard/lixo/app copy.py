import streamlit as st
import pandas as pd
from services.api import get_convenios

st.set_page_config(page_title="Dashboard de Convênios", layout="wide")

st.title("📄 Lista de Convênios (API .NET)")

token = st.text_input("Token JWT (opcional)", type="password")

if st.button("Carregar Convênios"):
    try:
        convenios = get_convenios(token)

        df = pd.DataFrame(convenios)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
