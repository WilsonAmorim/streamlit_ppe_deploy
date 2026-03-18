import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Zeladoria Digital v1.0",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SIMULAÇÃO DE BANCO DE DADOS (MOCK DATA) ---
@st.cache_data
def gerar_dados_ficticios():
    np.random.seed(42)
    categorias = {
        'Buraco': 'Prefeitura',
        'Lixo Acumulado': 'Prefeitura',
        'Semáforo': 'Prefeitura',
        'Falta de Energia': 'Coelba',
        'Poste Danificado': 'Coelba',
        'Vazamento de Água': 'Embasa',
        'Esgoto a Céu Aberto': 'Embasa',
        'Atividade Suspeita': 'Polícia',
        'Vandalismo': 'Polícia'
    }
    
    lista_cats = list(categorias.keys())
    n_linhas = 100
    
    data = pd.DataFrame({
        'id': range(1000, 1000 + n_linhas),
        'categoria': [np.random.choice(lista_cats) for _ in range(n_linhas)],
        'status': [np.random.choice(['Aberto', 'Em Análise', 'Concluído'], p=[0.5, 0.3, 0.2]) for _ in range(n_linhas)],
        'prioridade': [np.random.choice(['Baixa', 'Média', 'Alta', 'Crítica']) for _ in range(n_linhas)],
        'data_abertura': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(n_linhas)],
        # Coordenadas aproximadas de Salvador-BA
        'lat': np.random.uniform(low=-13.01, high=-12.88, size=n_linhas),
        'lon': np.random.uniform(low=-38.52, high=-38.40, size=n_linhas),
    })
    
    # Mapeia o órgão responsável baseado na categoria
    data['orgao'] = data['categoria'].map(categorias)
    return data

df = gerar_dados_ficticios()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1255/1255260.png", width=100)
st.sidebar.title("Filtros de Gestão")

filtro_orgao = st.sidebar.multiselect(
    "Selecione o Órgão:",
    options=df['orgao'].unique(),
    default=df['orgao'].unique()
)

filtro_status = st.sidebar.multiselect(
    "Status do Chamado:",
    options=df['status'].unique(),
    default=['Aberto', 'Em Análise']
)

# Aplicando filtros
df_filtrado = df[(df['orgao'].isin(filtro_orgao)) & (df['status'].isin(filtro_status))]

# --- ÁREA PRINCIPAL ---
st.title("🏙️ Sistema Integrado de Zeladoria Urbana")
st.markdown(f"Exibindo **{len(df_filtrado)}** incidentes ativos para os órgãos selecionados.")

# Métrica de Resumo
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Filtrado", len(df_filtrado))
col2.metric("Críticos (Urgente)", len(df_filtrado[df_filtrado['prioridade'] == 'Crítica']))
col3.metric("Aguardando Triagem", len(df_filtrado[df_filtrado['status'] == 'Aberto']))
col4.metric("Órgãos Ativos", len(filtro_orgao))

st.divider()

# --- MAPA E GRÁFICOS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📍 Mapa de Incidentes (Geolocalização)")
    # Cores no mapa baseadas na prioridade (opcional usando plotly para mais detalhes)
    st.map(df_filtrado, latitude='lat', longitude='lon', color='#ff4b4b' if 'Crítica' in df_filtrado['prioridade'].values else '#0000ff')

with c2:
    st.subheader("📊 Distribuição por Órgão")
    fig_pizza = px.pie(df_filtrado, names='orgao', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pizza, use_container_width=True)

st.divider()

# --- TABELA DE DADOS E DETALHES ---
st.subheader("📋 Detalhamento dos Chamados")
st.dataframe(
    df_filtrado[['id', 'data_abertura', 'orgao', 'categoria', 'prioridade', 'status']].sort_values(by='data_abertura', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Rodapé formatado
st.sidebar.info(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")