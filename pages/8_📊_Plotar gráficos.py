import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregar os dados das planilhas
    df_peso = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Garantir que as colunas de classe não tenham espaços extras
    df_peso["Classe do Animal"] = df_peso["Classe do Animal"].astype(str).str.strip()
    df_racao["Classe da Caixa"] = df_racao["Classe da Caixa"].astype(str).str.strip()

    # Criar dicionários para armazenar médias e erros padrão por classe
    medias_peso = {}
    erro_padrao_peso = {}

    # Definir corretamente os dias com base nas colunas da pesagem (excluindo ID e Classe)
    dias_peso = df_peso.columns[2:]

    # Processar todas as classes presentes nos dados de pesagem
    for classe in df_peso["Classe do Animal"].unique():
        df_classe = df_peso[df_peso["Classe do Animal"] == classe]
        medias_peso[classe] = df_classe[dias_peso].mean()
        erro_padrao_peso[classe] = df_classe[dias_peso].std() / np.sqrt(df_classe.shape[0])

    # Converter colunas de consumo para numérico
    df_racao.iloc[:, 2:] = df_racao.iloc[:, 2:].apply(pd.to_numeric, errors="coerce")

    # Criar dicionário para médias de consumo de ração por classe de caixa
    medias_racao = {}
    dias_racao = df_racao.columns[2:]

    for classe in df_racao["Classe da Caixa"].unique():
        medias_racao[classe] = df_racao[df_racao["Classe da Caixa"] == classe][dias_racao].mean()

    return {
        "medias_peso": medias_peso, 
        "erro_padrao_peso": erro_padrao_peso, 
        "df_peso": df_peso,
        "dias_peso": dias_peso,
        "medias_racao": medias_racao,
        "df_racao": df_racao,
        "dias_racao": dias_racao
    }

# Função para plotar a pesagem
def plotar_pesagem(medias_peso, erro_padrao_peso, dias_peso):
    fig = go.Figure()

    # Adicionar uma linha para cada classe encontrada nos dados
    cores = ["blue", "red", "green", "purple", "orange"]  # Lista de cores para diferentes classes
    for i, (classe, medias) in enumerate(medias_peso.items()):
        fig.add_trace(go.Scatter(
            x=dias_peso,
            y=medias.values,
            mode="lines+markers",
            name=f"Peso Médio {classe}",
            error_y=dict(type="data", array=erro_padrao_peso[classe].values, visible=True),
            line=dict(color=cores[i % len(cores)])  # Alterna as cores automaticamente
        ))

    fig.update_layout(
        title="Média de Peso dos Animais por Classe",
        xaxis_title="Dias",
        yaxis_title="Peso (g)",
        xaxis=dict(tickmode="array", tickvals=dias_peso),
        legend_title="Classes"
    )
    st.plotly_chart(fig)

# Função para plotar o consumo de ração
def plotar_consumo_racao(medias_racao, dias_racao):
    fig = go.Figure()

    # Adicionar uma linha para cada classe encontrada nos dados
    cores = ["green", "red", "blue", "purple", "orange"]
    for i, (classe, medias) in enumerate(medias_racao.items()):
        fig.add_trace(go.Scatter(
            x=dias_racao,
            y=medias.values,
            mode="lines+markers",
            name=f"Consumo {classe}",
            line=dict(color=cores[i % len(cores)])
        ))

    fig.update_layout(
        title="Consumo Médio de Ração por Classe",
        xaxis_title="Dias",
        yaxis_title="Consumo (g)",
        xaxis=dict(tickmode="array", tickvals=dias_racao),
        legend_title="Classes"
    )
    st.plotly_chart(fig)

# Streamlit App
st.title("Análise de Pesagem e Consumo de Ração dos Animais")

uploaded_file = st.file_uploader("Carregar o arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)

    # Plota o gráfico de pesagem para todas as classes
    plotar_pesagem(dados["medias_peso"], dados["erro_padrao_peso"], dados["dias_peso"])

    # Plota o gráfico de consumo de ração para todas as classes
    plotar_consumo_racao(dados["medias_racao"], dados["dias_racao"])

    # Exibe as tabelas
    st.subheader("Tabela de Pesagem para Todas as Classes")
    st.write(dados["df_peso"])

    st.subheader("Tabela de Consumo de Ração para Todas as Classes")
    st.write(dados["df_racao"])

