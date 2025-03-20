import streamlit as st
import altair as alt
import pandas as pd

# Criando um DataFrame com valores de média e erro padrão
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],       # Eixo X (por exemplo, tempo ou categorias)
    'mean': [10, 20, 15, 25, 30],  # Média dos valores
    'std_err': [1, 2, 1.5, 2, 1]  # Erro padrão (desvio padrão)
})

# Criando o gráfico de barras de erro
error_bars = alt.Chart(data).mark_errorbar().encode(
    x=alt.X('x:Q').scale(zero=False),
    y=alt.Y('mean:Q'),
    y2='mean + std_err'  # Define o intervalo de erro
)

# Adicionando os pontos representando a média
points = alt.Chart(data).mark_point(
    filled=True,
    color="black",
).encode(
    x='x:Q',
    y='mean:Q'
)

# Combinando as barras de erro e os pontos
chart = error_bars + points

# Exibindo o gráfico no Streamlit
st.title('Gráfico de Linha com Barras de Erro')
st.altair_chart(chart, use_container_width=True)
