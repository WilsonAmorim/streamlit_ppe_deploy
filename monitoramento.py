import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Painel de Zeladoria Urbana", layout="wide")

st.title("🏙️ Dashboard de Incidentes Urbanos - Salvador")
st.markdown("Monitoramento de chamados via CPF em tempo real.")

# 1. Simulação de Dados (Mock Data)
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'categoria': ['Buraco', 'Semáforo', 'Lixo', 'Segurança', 'Tráfego', 'Iluminação'] * 5,
        'lat': np.random.uniform(low=-13.01, high=-12.85, size=30),
        'lon': np.random.uniform(low=-38.52, high=-38.35, size=30),
        'prioridade': ['Alta', 'Crítica', 'Baixa', 'Média', 'Alta', 'Média'] * 5,
        'status': ['Aberto', 'Em Análise', 'Concluído'] * 10
    })
    return data

df = load_data()

# 2. Filtros na Barra Lateral
st.sidebar.header("Filtros de Gestão")
categoria_selecionada = st.sidebar.multiselect(
    "Filtrar por Categoria:", 
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

status_selecionado = st.sidebar.selectbox("Status do Chamado:", ['Todos', 'Aberto', 'Em Análise', 'Concluído'])

# Filtrando o DataFrame
df_filtrado = df[df['categoria'].isin(categoria_selecionada)]
if status_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['status'] == status_selecionado]

# 3. Layout Principal (Métricas)
col1, col2, col3 = st.columns(3)
col1.metric("Total de Chamados", len(df_filtrado))
col2.metric("Pendentes (Aberto)", len(df_filtrado[df_filtrado['status'] == 'Aberto']))
col3.metric("Críticos", len(df_filtrado[df_filtrado['prioridade'] == 'Crítica']))

# 4. Mapa Interativo
st.subheader("📍 Localização dos Incidentes")
st.map(df_filtrado)

# 5. Tabela de Detalhes
st.subheader("📋 Lista de Ocorrências")
st.dataframe(df_filtrado, use_container_width=True)