import streamlit as st
import pandas as pd
from data.loader import carregar_resumo_ativo, carregar_resumo_geral, gerar_relatorio_lotes_2026_v2
from charts.ativos import mostrar_grafico_ativos
from charts.lotes import mostrar_grafico_contratacoes_ano
from charts.genero import mostrar_grafico_sexo_lote

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

    if not df_ativos.empty:
        mostrar_grafico_ativos(df_ativos)

    mostrar_grafico_contratacoes_ano(df_geral)
    mostrar_grafico_sexo_lote(df_geral)
    # Teste de conferência rápida
df_2026 = df_geral[(df_geral['ConvenioNome'] == "Fesfsus Lote 01") & 
                   (df_geral['DataAdmissao'].dt.year == 2026)]

# st.header("📊 Relatório de Movimentação - 2026")
# st.write("Período: Janeiro/2026 a Dezembro/2026")

# st.header("📊 Relatório Consolidado por Lote")
# st.info("📌 **Ativos e Desligados:** Filtrados por Admissão em 2026 | **Afastados:** Total acumulado (todos os anos).")

# df_rel = gerar_relatorio_lotes_2026_v2()

# if not df_rel.empty:
#     # Exibe a tabela
#     st.dataframe(
#         df_rel,
#         use_container_width=True,
#         column_config={
#             "Ativos (2026)": st.column_config.NumberColumn("Ativos (2026)", help="Apenas admitidos em 2026"),
#             "Afastados (Total)": st.column_config.NumberColumn("Afastados (Total)", help="Total geral de afastados hoje"),
#             "Desligados (2026)": st.column_config.NumberColumn("Desligados (2026)", help="Desligamentos ocorridos em 2026")
#         }
#     )

#     # Métricas de Rodapé para o Dashboard
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Soma Ativos (2026)", df_rel["Ativos (2026)"].sum())
#     c2.metric("Total Afastados (Geral)", df_rel["Afastados (Total)"].sum(), delta_color="inverse")
#     c3.metric("Soma Desligados (2026)", df_rel["Desligados (2026)"].sum())
# else:
#     st.warning("Nenhum dado encontrado para gerar o relatório.")