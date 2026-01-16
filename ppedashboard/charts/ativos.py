import streamlit as st
import plotly.express as px


def mostrar_grafico_ativos(df):
    st.markdown("### 🟢 Beneficiários Ativos por Lote")
    
    if df.empty:
        st.warning("Nenhum dado encontrado no CSV.")
        return

    # 1. Filtrar as situações desejadas (igual ao seu código C#)
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    df_filtrado = df[df['Situacao'].isin(situacoes_ativas)].copy()

    if df_filtrado.empty:
        st.info("Nenhum beneficiário com situação 'Ativa' encontrado.")
        return

    # 2. Agrupar por Lote (ConvenioNome)
    # Criamos uma contagem de IDs para cada Lote
    df_agrupado = df_filtrado.groupby('ConvenioNome').size().reset_index(name='Total')
    
    # 3. Criar o gráfico
    fig = px.bar(
        df_agrupado,
        x='ConvenioNome',
        y='Total',
        text='Total',
        labels={'ConvenioNome': 'Lote/Convênio', 'Total': 'Total de Ativos'},
        color_discrete_sequence=['#0066cc'] # Azul da sua imagem
    )

    # Ajustes estéticos
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        yaxis_title="Total de Ativos",
        xaxis_title="Lote/Convênio"
    )

    st.plotly_chart(fig, use_container_width=True)