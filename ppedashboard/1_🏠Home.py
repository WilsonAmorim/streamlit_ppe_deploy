import streamlit as st
from datetime import datetime
import pandas as pd
import os
import data.loader as loader

st.set_page_config(
    page_title="Dashboard PPE",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
    <style>
    /* Esconde apenas os botões da direita (Share, Star, GitHub, etc.) */
    [data-testid="stToolbar"] {
        visibility: hidden;
        display: none;
    }

    /* Esconde especificamente o menu de 3 pontos (MainMenu) */
    #MainMenu {
        visibility: hidden;
    }

    /* Opcional: Remove o espaço vazio que fica no topo */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    /* Garante que o botão da barra lateral continue visível e funcional */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible;
    }
    </style>
""", unsafe_allow_html=True)

def formatar_moeda_br(val):
            try:
                return f" {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return " 0,00"
            
def formatar_inteiros(val):
    try:
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0"
            
# --- CONFIGURAÇÃO DO LOGO NO TOPO DO MENU ---
# O st.logo coloca a imagem automaticamente acima da lista de páginas
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_atual, "imagens", "logo.png",)
caminho_logo2 = os.path.join(diretorio_atual, "imagens", "logogov.png")

if os.path.exists(caminho_logo):
    st.logo(caminho_logo, icon_image=caminho_logo)
else:
    st.sidebar.warning("Logo não encontrado em: imagens/logo.png")

st.sidebar.image(caminho_logo2, width=400)
# --- CONTEÚDO DA BARRA LATERAL ---
col_esq, col_meio, col_dir = st.columns([1, 2, 1])

with col_meio:
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, width=100)
    else:
        st.error("Logo não encontrado.")
st.title("Dashboard PPE - Projeto Primeiro Emprego")

st.markdown(
    """
    O Aplicativo de Dashboard PPE visa fornecer insights valiosos sobre os convênios
    firmados pelo PPE ao longo dos anos. Com uma interface interativa e visualizações
    dinâmicas, este dashboard permite aos usuários explorar dados detalhados sobre os
    convênios, facilitando a análise de tendências, desempenho e impacto dessas parcerias.
    """
)

st.metric("Contratações no Período de 2016 até Março  2026",  "Beneficários", border=True)

a, b, c, d = st.columns(4)

with a:
    with st.container(border=True):
        st.metric("Total Geral Ativos", value=formatar_inteiros(loader.obter_total_ativos())+" =")
        st.page_link("pages/2_💆‍♂️Beneficiários.py", label="Ver Detalhes", icon="➡️")

b.metric("Secretaria da Saúde Ativos",  value=formatar_inteiros(loader.carregar_fesfsus_ativo())+" +", border=True)
c.metric("Total Secretaria da Educação Ativos", value=formatar_inteiros(loader.carregar_flem2_ativo())+" +", border=True)
d.metric("Total Demais Órgãos e Entidades Ativos",  value=formatar_inteiros(loader.carregar_flem3_ativo()), border=True)

a2, b2, c2, d2 = st.columns(4)
contratados = loader.obter_total_ativos() + loader.carregar_finalizados() + loader.carregar_afastados() + 61
a2.metric("Contratados até Março  de 2026", value=formatar_inteiros(contratados)+" =", border=True)
b2.metric("Total Geral Ativos", value=formatar_inteiros(loader.obter_total_ativos())+" +", border=True)
c2.metric("Contratos de Trabalho Finalizados", value=formatar_inteiros(loader.carregar_finalizados() + 61)+" +", border=True)
d2.metric("Afastados pelo INSS", value=formatar_inteiros(loader.carregar_afastados()), border=True)

a3, b3, c3, d3 = st.columns(4)
estagios = 6174
privados = 1127
geral = contratados + estagios + privados
a3.metric("Total Geral", value=formatar_inteiros(geral)+" =", border=True)
b3.metric("Contratados até Março  de 2026", value=formatar_inteiros(contratados)+" +", border=True)
c3.metric("Estágio e Aprendizagem no Espaço Público", value=formatar_inteiros(estagios)+" +", border=True)
d3.metric("Ocupação Formal, Estágio e\n Aprendizagem no Espaço Privado", value=formatar_inteiros(privados), border=True)

st.metric("Repasses Financeiros por Lote e Competência",  "Repasses", border=True)
a4, b4, c4, d4 = st.columns(4)

RepassesFesfsus = 110210584.86
RepassesFlem2 = 59279273.65
RepassesFlem3 = 96446392.70
totalRepasses = RepassesFesfsus + RepassesFlem2 + RepassesFlem3
with a4:
    with st.container(border=True):
        st.metric("Total de Repasses", value=formatar_moeda_br(totalRepasses)+" =")
        st.page_link("pages/3_💰Finanças - Repasses", label="Ver Detalhes", icon="➡️")

b4.metric("Repasse Fesfsus Lote 01", value=formatar_moeda_br(RepassesFesfsus)+" +", border=True)
c4.metric("Repasse Flem Lote 02", value=formatar_moeda_br(RepassesFlem2)+" +", border=True)
d4.metric("Repasse Flem Lote 03 ", value=formatar_moeda_br(RepassesFlem3), border=True)

st.sidebar.markdown("\n**SAEB/DG/PPE**")

# --- CONTEÚDO DA PÁGINA PRINCIPAL ---
