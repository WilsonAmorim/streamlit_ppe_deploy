import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from services.api import get_convenios

API_URL = "http://ppeprojeto.saeb:5000/api/convenios"

# --------------------------------------------------------
# CARREGAR DADOS DA API
# --------------------------------------------------------
@st.cache_data
def carregar_dados():
    response = requests.get(API_URL)
    json_data = response.json()

    # Detecta automaticamente o formato retornado
    if isinstance(json_data, list):
        data = json_data
    elif isinstance(json_data, dict):
        if "conveiosCadastrados" in json_data:
            data = json_data["conveiosCadastrados"]
        elif "convenios" in json_data:
            data = json_data["convenios"]
        else:
            data = next((v for v in json_data.values() if isinstance(v, list)), [])
    else:
        data = []

    df = pd.DataFrame(data)
    df.columns = df.columns.str.lower()  # normaliza nomes

    # Criar coluna Ano com segurança
    if "dataadmissao" in df.columns:
        df["dataadmissao"] = pd.to_datetime(df["dataadmissao"], errors="coerce")
        df["ano"] = df["dataadmissao"].dt.year
    else:
        st.error("❌ Coluna 'dataAdmissao' não encontrada no JSON.")
        st.stop()

    return df


# --------------------------------------------------------
# CARREGAR DATAFRAME
# --------------------------------------------------------
df = carregar_dados()

st.title("Dashboard de Convênios por Setor e Lote")

# ---------------- MENU LATERAL --------------------------
setor = st.sidebar.selectbox(
    "Selecione o Setor",
    ["Setor 1", "Setor 2", "Setor 3", "Setor 4", "Setor 5"]
)

# --------------------------------------------------------
# SETOR 1 – POSSUI GRÁFICOS
# --------------------------------------------------------
if setor == "Setor 1":
    st.header("📊 Gráficos por Lote – Setor 1")

    # Identificar lotes
    if "convenionome" not in df.columns:
        st.error("Coluna 'convenioNome' não encontrada.")
        st.stop()

    lotes = df["convenionome"].dropna().unique().tolist()

    if not lotes:
        st.warning("Nenhum lote encontrado.")
        st.stop()

    # Criar abas por lote
    abas = st.tabs(lotes)

    for tab, lote in zip(abas, lotes):
        with tab:
            df_lote = df[df["convenionome"] == lote]

            if df_lote.empty:
                st.write("Sem dados para este lote.")
                continue

            # Agrupar por ano
            contagem = df_lote.groupby("ano").size().reset_index(name="quantidade")

            # Gráfico de barras
            fig = px.bar(
                contagem,
                x="ano",
                y="quantidade",
                title=f"Quantidade por Ano – {lote}",
                text="quantidade"
            )

            fig.update_layout(xaxis_title="Ano", yaxis_title="Quantidade")
            fig.update_traces(textposition="outside")

            st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# OUTROS SETORES – AINDA NÃO TEM GRÁFICOS
# --------------------------------------------------------
else:
    st.header(f"{setor}")
    st.info("📌 Este setor ainda não possui gráficos implementados.")
