import streamlit as st
import pandas as pd
import plotly.express as px
from services.api import get_convenios

st.set_page_config(page_title="Dashboard Convênios", layout="wide")

st.title("📊 Dashboard - Evolução por Lote ao Longo dos Anos")

token = st.text_input("Token JWT (caso necessário)", type="password")

if st.button("Carregar Dados"):
    try:
        dados = get_convenios(token)
        df = pd.DataFrame(dados)

        # --- Converter datas ---
        df["dataAdmissao"] = pd.to_datetime(df["dataAdmissao"], errors="coerce")

        # --- Criar coluna com o ano ---
        df["Ano"] = df["dataAdmissao"].dt.year

        # --- Identificar todos os Lotes (ConvenioNome) ---
        lotes = sorted(df["convenioNome"].unique())

        st.subheader("Gráficos por Lote")

        # Criar um gráfico para cada lote
        for lote in lotes:
            df_lote = df[df["convenioNome"] == lote]

            # Agrupar por ano
            agrupado = (
                df_lote.groupby("Ano")
                .size()
                .reset_index(name="Quantidade")
                .sort_values(by="Ano")
            )

            st.markdown(f"### 📦 {lote}")

            fig = px.bar(
                agrupado,
                x="Ano",
                y="Quantidade",
                title=f"Evolução do {lote} por Ano",
                text="Quantidade",
            )
            fig.update_traces(textposition="outside")

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
