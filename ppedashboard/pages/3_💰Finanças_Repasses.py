import streamlit as st
import os
from pathlib import Path

# Título da página
st.set_page_config(page_title="Detalhamento de Repasses", layout="wide")


ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "imagens" / "logogov.png"
st.sidebar.image(IMG, width=400)

st.title("💰 Painel de Repasses")


# Função para exibir as imagens (baseada no que conversamos antes)
def exibir_repasses_por_imagem():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Ajuste o caminho para onde suas imagens estão guardadas
    pasta_imagens = os.path.join(diretorio_atual, "..", "data", "repasses")

    lotes = {
        
        "Lote 01 - FESFSUS - SECRETARIA DA SAÚDE": "repasse_lote01.png",
        "Lote 02 - FLEM - SECRETARIA DA EDUCAÇÃO": "repasse_lote02.png",
        "Lote 03 - FLEM - DEMIAS ÓRGÃOS E ENTIDADES": "repasse_lote03.png",
        "Lote  - FLEM -Lotes 02 e 03": "repasse_lote04.png",
        "Todo os Lotes - FESFSUS - SECRETARIA DA SAÚDE, FLEM - SECRETARIA DA EDUCAÇÃO, DEMIAS ÓRGÃOS E ENTIDADES": "repasse_lote05.png",
        "Investimento no Projeto Primeiro Emprego": "investimento.png"
    }

    for nome_lote, arquivo in lotes.items():
        caminho_imagem = os.path.join(pasta_imagens, arquivo)
        
        with st.expander(f"📦 {nome_lote.upper()}", expanded=(nome_lote == "Fesfsus Lote 01")):
            if os.path.exists(caminho_imagem):
                st.image(caminho_imagem, use_container_width=True)
            else:
                st.warning(f"Arquivo {arquivo} não encontrado em {pasta_imagens}")

# Chama a função
exibir_repasses_por_imagem()
st.sidebar.markdown("\n**SAEB/DG/PPE**")