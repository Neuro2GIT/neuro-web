import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Função para carregar o arquivo e processar as tabelas
def carregar_e_processar_excel(uploaded_file):
    # Carregar o arquivo Excel
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Filtrar os dados apenas para a classe CT
    df_ct = df[df['Classe do Animal'] == 'CT']

    # Calcular a média e erro padrão para cada dia de pesagem
    medias_peso = df_ct.iloc[:, 2:].mean()  # Ignorar as duas primeiras colunas (ID e Classe do Animal)
    erro_padrao_peso = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])  # Erro padrão

    # Filtrar as caixas CT e DT para consumo de ração
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Calcular a média e erro padrão de consumo de ração para cada dia
    medias_racao_ct = df_racao_ct.iloc[:, 2:].mean()
    erro_padrao_racao_ct = df_racao_ct.iloc[:, 2:].std() / np.sqrt(df_racao_ct.shape[0])

    medias_racao_dt = df_racao_dt.iloc[:, 2:].mean()
    erro_padrao_racao_dt = df_racao_dt.iloc[:, 2:].std() / np.sqrt(df_racao_dt.shape[0])

    # Retornar todas as variáveis necessárias
    return medias_peso, erro_padrao_peso, df_ct, medias_racao_ct, medias_racao_dt, erro_padrao_racao_ct, erro_padrao_racao_dt, df_racao_ct, df_racao_dt

# Página Streamlit
st.title("Análise de Pesagem e Consumo de Ração dos Animais")

# Widget para o upload do arquivo Excel
uploaded_file = st.file_uploader("Carregar o arquivo Excel com os dados de pesagem", type=["xlsx"])

if uploaded_file is not None:
    # Processar o arquivo e calcular as médias e erro padrão
    medias_peso, erro_padrao_peso, df_ct, medias_racao_ct, medias_racao_dt, erro_padrao_racao_ct, erro_padrao_racao_dt, df_racao_ct, df_racao_dt = carregar_e_processar_excel(uploaded_file)

    # Plotar gráfico de pesagem dos animais da classe CT
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(medias_peso.index, medias_peso.values, yerr=erro_padrao_peso.values, fmt='o-', label="Média de Peso (g)", color='b', capsize=5)
    ax.set_xticks(range(1, len(medias_peso) + 1))  # Ajustar os dias para números inteiros
    ax.set_xticklabels(range(1, len(medias_peso) + 1))  # Mostrar apenas os números dos dias
    ax.set_xlabel("Dias de Pesagem")
    ax.set_ylabel("Peso Médio (g)")
    ax.set_title("Média de Peso dos Animais da Caixa CT com Erro Padrão")
    ax.legend()

    # Exibir o gráfico de pesagem
    st.pyplot(fig)

    # Plotar gráfico de consumo de ração com erro padrão
    fig_racao, ax_racao = plt.subplots(figsize=(10, 6))

    # Plotar Caixa CT
    ax_racao.errorbar(medias_racao_ct.index, medias_racao_ct.values, yerr=erro_padrao_racao_ct.values, fmt='o-', label="Caixa CT", color='g', capsize=5)
    
    # Plotar Caixa DT
    ax_racao.errorbar(medias_racao_dt.index, medias_racao_dt.values, yerr=erro_padrao_racao_dt.values, fmt='o-', label="Caixa DT", color='r', capsize=5)

    ax_racao.set_xticks(range(1, len(medias_racao_ct) + 1))  # Ajustar os dias para números inteiros
    ax_racao.set_xticklabels(range(1, len(medias_racao_ct) + 1))  # Mostrar apenas os números dos dias
    ax_racao.set_xlabel("Dias de Consumo de Ração")
    ax_racao.set_ylabel("Consumo Médio de Ração (g)")
    ax_racao.set_title("Consumo Médio de Ração por Caixa com Erro Padrão")
    ax_racao.legend()

    # Exibir o gráfico de consumo de ração
    st.pyplot(fig_racao)

    # Exibir as tabelas de dados para referência
    st.subheader("Tabela de Pesagem para Animais da Classe CT")
    st.write(df_ct)

    st.subheader("Tabela de Consumo de Ração para Caixas CT e DT")
    st.write(pd.concat([df_racao_ct, df_racao_dt]))
