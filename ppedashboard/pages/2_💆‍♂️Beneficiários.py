import streamlit as st
import pandas as pd
from data.loader import carregar_resumo_ativo, carregar_resumo_geral
from charts.ativos import mostrar_grafico_ativos
from charts.lotes import mostrar_grafico_contratacoes_ano

# Configuração da página para aproveitar o espaço lateral
st.set_page_config(page_title="Painel de Beneficiários", layout="wide")

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

    # --- SEÇÃO 1: RESUMO ATUAL ---
    # Exibe o gráfico de barras azul claro (apenas ativos)
    if not df_ativos.empty:
        mostrar_grafico_ativos(df_ativos)

    # --- SEÇÃO 2: HISTÓRICO DE CONTRATAÇÕES ---
    # Exibe o gráfico de barras azul escuro (histórico completo - bate com a API)
    mostrar_grafico_contratacoes_ano(df_geral)

    # --- SEÇÃO 3: TABELA DE AUDITORIA ---
    st.markdown("---")
    with st.expander("🔍 Detalhamento e Auditoria de Registros", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            # Lista de lotes limpa e ordenada (evita o erro de float vs str)
            lotes_disponiveis = sorted([l for l in df_geral['ConvenioNome'].unique() if l != 'nan'])
            lote_sel = st.selectbox("Filtrar Lote", lotes_disponiveis)
            
        with col2:
            # Lista de anos baseada nas admissões encontradas
            anos_disponiveis = sorted(df_geral['ano_admissao'].dropna().unique().astype(int))
            ano_sel = st.selectbox("Filtrar Ano", anos_disponiveis, 
                                   index=anos_disponiveis.index(2016) if 2016 in anos_disponiveis else 0)

        # Filtro dinâmico para visualização da tabela
        df_tabela = df_geral[
            (df_geral['ConvenioNome'] == lote_sel) & 
            (df_geral['ano_admissao'] == ano_sel)
        ]

        st.write(f"Exibindo **{len(df_tabela)}** registros para o lote e ano selecionados.")
        
        # Exibição da tabela com colunas essenciais
        st.dataframe(
            df_tabela[['Id', 'Nome', 'DataAdmissao', 'Situacao', 'PostoTrabalho']], 
            use_container_width=True,
            hide_index=True
        )

else:
    st.error("Não foi possível carregar o arquivo de beneficiários.")