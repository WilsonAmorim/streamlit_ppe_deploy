import streamlit as st
import plotly.express as px

def mostrar_grafico_sexo(df):
    st.markdown("---")
    st.subheader("📊 Distribuição Percentual de Sexo por Lote")

    col_lote = "lote" if "lote" in df.columns else "convenionome"
    
    if col_lote in df.columns and "sexo" in df.columns:
        # 1. Agrupar e somar as quantidades
        df_plot = df.groupby([col_lote, "sexo"])["quantidade"].sum().reset_index()

        # 2. Calcular o percentual dentro de cada lote
        df_plot['percentual'] = df_plot.groupby(col_lote)['quantidade'].transform(
            lambda x: (x / x.sum() * 100).round(1)
        )

        # 3. Criar o gráfico
        # Usamos 'text' para exibir o símbolo de % e o valor
        df_plot['texto_label'] = df_plot['percentual'].astype(str) + '%'

        fig = px.bar(
            df_plot, 
            x=col_lote, 
            y="percentual", # Mudamos o eixo Y para o percentual
            color="sexo",
            barmode="group", 
            text="texto_label",
            labels={"percentual": "Porcentagem (%)", "lote": "Lote", "sexo": "Gênero"},
            color_discrete_map={'F': '#FF3131', 'M': '#00BFFF', 'N/I': '#CCCCCC'}
        )

        # Ajustes de layout
        fig.update_traces(textposition="outside")
        fig.update_layout(
            yaxis_range=[0, 110], # Espaço para o texto não cortar
            yaxis_ticksuffix="%",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Colunas 'sexo' ou 'lote' não encontradas para calcular percentual.")