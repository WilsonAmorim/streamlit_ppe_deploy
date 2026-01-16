import streamlit as st
import pandas as pd
from data.loader import carregar_resumo_ativo, carregar_resumo_geral
from charts.ativos import mostrar_grafico_ativos
from charts.lotes import mostrar_grafico_contratacoes_ano
from charts.genero import mostrar_grafico_sexo_lote

# Configuração da página para aproveitar o espaço lateral
st.set_page_config(page_title="Painel de Beneficiários", layout="wide")

# Injeção de CSS para esconder o menu, o cabeçalho e o rodapé
st.markdown("""
    <style>
    /* Esconde o menu (os três pontos no canto superior direito) */
    #MainMenu {visibility: hidden;}
    
    /* Esconde o cabeçalho inteiro (onde ficam os botões Share, Star, etc.) */
    header {visibility: hidden;}
    
    /* Esconde o rodapé "Made with Streamlit" (opcional) */
    footer {visibility: hidden;}
    
    /* Ajusta o espaçamento superior após esconder o header */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Beneficiários")

# 1. CARREGAMENTO DOS DADOS
# df_geral: Histórico completo (usado para o gráfico de contratações e conferência)
df_geral = carregar_resumo_geral()

# df_ativos: Apenas quem está na ativa hoje (usado para o gráfico de situação atual)
df_ativos = carregar_resumo_ativo()

if not df_geral.empty:
    # --- TRATAMENTO DOS DADOS GERAIS ---
    # Garante que datas sejam interpretadas corretamente (suporta formatos ISO e BR)
    df_geral['DataAdmissao'] = pd.to_datetime(df_geral['DataAdmissao'], errors='coerce')
    df_geral['ano_admissao'] = df_geral['DataAdmissao'].dt.year

    if not df_ativos.empty:
        mostrar_grafico_ativos(df_ativos)

    mostrar_grafico_contratacoes_ano(df_geral)
    mostrar_grafico_sexo_lote(df_geral)
    # Teste de conferência rápida
df_2025 = df_geral[(df_geral['ConvenioNome'] == "Fesfsus Lote 01") & 
                   (df_geral['DataAdmissao'].dt.year == 2025)]

