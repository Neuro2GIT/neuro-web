import streamlit as st
import altair as alt
import pandas as pd

# Criando um DataFrame com valores de média e erro padrão
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],       # Eixo X (por exemplo, tempo ou categorias)
    'mean': [10, 20, 15, 25, 30],  # Média dos valores
    'std_err': [1, 2, 1.5, 2, 1]  # Erro padrão (desvio padrão)
})

# Criando o gráfico de linha com erro padrão
chart = alt.Chart(data).mark_line(color='blue').encode(
    x='x',
    y='mean'
) + alt.Chart(data).mark_errorband(extent='stderr').encode(
    x='x',
    y='mean',
    y2='mean + std_err'  # Define o intervalo de erro
)

# Exibindo o gráfico no Streamlit
st.title('Gráfico de Linha com Erro Padrão')
st.altair_chart(chart, use_container_width=True)
