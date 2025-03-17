import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Gerando os dados de amostra
np.random.seed(42)

# Dados para a primeira gaussiana
x1 = np.random.normal(loc=0, scale=1, size=500)

# Dados para a segunda gaussiana
x2 = np.random.normal(loc=5, scale=1.5, size=500)

# Criando um DataFrame
df = pd.DataFrame({
    'x': np.concatenate([x1, x2]),
    'categoria': ['Gaussiana 1']*500 + ['Gaussiana 2']*500
})

# Criando o gráfico com Altair
chart = alt.Chart(df).mark_point().encode(
    x='x',
    color='categoria',
    tooltip=['x', 'categoria']
).interactive()

# Exibindo a visualização no Streamlit
st.title("Visualização de Distribuições Gaussianas")
st.write("Gráfico interativo mostrando duas distribuições gaussianas.")
st.altair_chart(chart, use_container_width=True)
