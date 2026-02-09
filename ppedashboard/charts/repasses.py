import streamlit as st
import os

def exibir_repasses_por_imagem():
    st.markdown("---")
    st.subheader("📋 Resumo de Repasses por Lote")

    # Define o diretório onde as imagens estão guardadas
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_imagens = os.path.join(diretorio_atual, "..", "data", "repasses")

    # Lista de lotes e seus respectivos arquivos de imagem
    # Você pode automatizar isso ou deixar fixo se os nomes não mudarem
    lotes = {
        "Lote 01": "repasse_lote01.png",
        "Lote 02": "repasse_lote02.png",
        "Lote 03": "repasse_lote0.png"
    }

    for nome_lote, arquivo in lotes.items():
        caminho_imagem = os.path.join(pasta_imagens, arquivo)
        
        with st.expander(f"📦 {nome_lote.upper()}", expanded=False):
            if os.path.exists(caminho_imagem):
                # Exibe a imagem do resumo (como a que você anexou)
                st.image(
                    caminho_imagem, 
                    caption=f"Detalhamento Financeiro - {nome_lote}",
                    use_container_width=True
                )
                
                # Opcional: Adicionar um botão de download para o PDF desse lote
                # if os.path.exists(caminho_imagem.replace(".png", ".pdf")):
                #     with open(caminho_imagem.replace(".png", ".pdf"), "rb") as f:
                #         st.download_button(
                #             label=f"📥 Baixar PDF {nome_lote}",
                #             data=f,
                #             file_name=f"Repasses_{nome_lote}.pdf",
                #             mime="application/pdf"
                #         )
            else:
                st.warning(f"⚠️ Imagem não encontrada para o {nome_lote}")