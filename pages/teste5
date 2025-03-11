import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# Função para carregar o arquivo e processar as tabelas (somente consumo de ração)
def carregar_e_processar_racao(uploaded_file):
    # Carregar o arquivo Excel
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Filtrar as caixas CT e DT para consumo de ração
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Forçar as colunas de consumo a serem numéricas, ignorando valores não numéricos (convertendo-os para NaN)
    df_racao_ct.iloc[:, 1:] = df_racao_ct.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    df_racao_dt.iloc[:, 1:] = df_racao_dt.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    # Calcular a média e erro padrão para o consumo de ração por dia para cada caixa
    medias_racao_ct = df_racao_ct.iloc[:, 1:].mean(axis=0)  # Média por dia para a caixa CT
    erro_padrao_racao_ct = df_racao_ct.iloc[:, 1:].std(axis=0) / np.sqrt(df_racao_ct.shape[0])  # Erro padrão por dia

    medias_racao_dt = df_racao_dt.iloc[:, 1:].mean(axis=0)  # Média por dia para a caixa DT
    erro_padrao_racao_dt = df_racao_dt.iloc[:, 1:].std(axis=0) / np.sqrt(df_racao_dt.shape[0])  # Erro padrão por dia

    # Retornar todas as variáveis necessárias
    return medias_racao_ct, medias_racao_dt, erro_padrao_racao_ct, erro_padrao_racao_dt, df_racao_ct, df_racao_dt

# Página Streamlit dedicada ao gráfico de consumo de ração
st.title("Análise de Consumo de Ração por Caixa (CT e DT)")

# Widget para o upload do arquivo Excel
uploaded_file = st.file_uploader("Carregar o arquivo Excel com os dados de consumo de ração", type=["xlsx"])

if uploaded_file is not None:
    # Processar o arquivo e calcular as médias e erro padrão para o consumo de ração
    medias_racao_ct, medias_racao_dt, erro_padrao_racao_ct, erro_padrao_racao_dt, df_racao_ct, df_racao_dt = carregar_e_processar_racao(uploaded_file)

    # Plotar gráfico de consumo de ração com erro padrão
    fig_racao, ax_racao = plt.subplots(figsize=(10, 6))

    # Plotar Caixa CT
    ax_racao.errorbar(np.arange(1, len(medias_racao_ct) + 1), medias_racao_ct.values, yerr=erro_padrao_racao_ct.values, fmt='o-', label="Caixa CT", color='g', capsize=5)
    
    # Plotar Caixa DT
    ax_racao.errorbar(np.arange(1, len(medias_racao_dt) + 1), medias_racao_dt.values, yerr=erro_padrao_racao_dt.values, fmt='o-', label="Caixa DT", color='r', capsize=5)

    # Ajustando o eixo x para dias numerados de 1 a N
    dias = np.arange(1, len(medias_racao_ct) + 1)
    ax_racao.set_xticks(dias)
    ax_racao.set_xticklabels(dias)  # Marcar os dias como números inteiros
    ax_racao.set_xlabel("Dias de Consumo de Ração")
    ax_racao.set_ylabel("Consumo Médio de Ração (g)")
    ax_racao.set_title("Consumo Médio de Ração por Caixa com Erro Padrão")
    ax_racao.legend()

    # Exibir o gráfico de consumo de ração
    st.pyplot(fig_racao)

    # Exibir as tabelas de dados para referência
    st.subheader("Tabela de Consumo de Ração para Caixas CT e DT")
    st.write(pd.concat([df_racao_ct, df_racao_dt]))
