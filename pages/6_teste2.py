import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Função para carregar o arquivo e calcular a média do peso e erro padrão
def carregar_e_processar_excel(uploaded_file):
    # Carregar o arquivo Excel
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")

    # Filtrar os dados apenas para a classe CT
    df_ct = df[df['Classe do Animal'] == 'CT']

    # Calcular a média e erro padrão para cada dia
    medias = df_ct.iloc[:, 2:].mean()  # Ignorar as duas primeiras colunas (ID e Classe do Animal)
    erro_padrao = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])  # Erro padrão

    return medias, erro_padrao, df_ct

# Página Streamlit
st.title("Análise de Pesagem dos Animais da Classe CT")

# Widget para o upload do arquivo Excel
uploaded_file = st.file_uploader("Carregar o arquivo Excel com os dados de pesagem", type=["xlsx"])

if uploaded_file is not None:
    # Processar o arquivo e calcular as médias e erro padrão
    medias, erro_padrao, df_ct = carregar_e_processar_excel(uploaded_file)

    # Exibir o gráfico da média e erro padrão
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(medias.index, medias.values, yerr=erro_padrao.values, fmt='o-', label="Média de Peso (g)", color='b', capsize=5)

    ax.set_xlabel("Dias de Pesagem")
    ax.set_ylabel("Peso Médio (g)")
    ax.set_title("Média de Peso dos Animais da Caixa CT com Erro Padrão")
    ax.legend()
    
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    # Exibir a tabela de dados de CT para referência
    st.subheader("Tabela de Pesagem para Animais da Classe CT")
    st.write(df_ct)
