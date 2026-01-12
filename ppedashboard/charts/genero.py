import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_grafico_sexo_lote(df):
    st.markdown("---")
    st.subheader("📊 Distribuição Percentual de Genero por Lote")

    if df.empty:
        st.warning("Dados insuficientes para gerar o gráfico de gênero.")
        return

    # 1. Agrupamento e Cálculo de Percentual
    # Contamos quantos registros existem por Lote e por Sexo
    df_sexo = df.groupby(['ConvenioNome', 'Sexo']).size().reset_index(name='contagem')

    # Calculamos o total por lote para descobrir o %
    df_sexo['total_lote'] = df_sexo.groupby('ConvenioNome')['contagem'].transform('sum')
    df_sexo['porcentagem'] = (df_sexo['contagem'] / df_sexo['total_lote']) * 100

    # 2. Criação do Gráfico de Barras Agrupadas
    fig = px.bar(
        df_sexo,
        x="ConvenioNome",
        y="porcentagem",
        color="Sexo",
        barmode="group",
        text=df_sexo['porcentagem'].apply(lambda x: f'{x:.1f}%'),
        labels={'porcentagem': 'Porcentagem (%)', 'ConvenioNome': 'Lote', 'Sexo': 'Gênero'},
        color_discrete_map={'F': '#FF3333', 'M': '#00BFFF'} # Cores aproximadas da sua imagem
    )

    # 3. Ajustes de Layout para ficar igual à imagem
    fig.update_layout(
        yaxis_ticksuffix="%",
        yaxis_range=[0, 100],
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='Gênero',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Lote",
        yaxis_title="Porcentagem (%)"
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    st.plotly_chart(fig, use_container_width=True)