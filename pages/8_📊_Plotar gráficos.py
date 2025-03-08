import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregar os dados das planilhas
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Filtrar os dados apenas para a classe CT e DT
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Calcular média e erro padrão da pesagem para CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])

    # Calcular média e erro padrão da pesagem para DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    # Filtrar as caixas CT e DT para consumo de ração
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Forçar as colunas de consumo a serem numéricas, ignorando valores não numéricos
    df_racao_ct.iloc[:, 1:] = df_racao_ct.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    df_racao_dt.iloc[:, 1:] = df_racao_dt.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    # Calcular média do consumo de ração para CT
    medias_racao_ct = df_racao_ct.iloc[:, 1:].mean(axis=0)

    # Calcular média do consumo de ração para DT
    medias_racao_dt = df_racao_dt.iloc[:, 1:].mean(axis=0)

    # Retornar os valores em um dicionário
    return {
        "medias_peso_ct": medias_peso_ct, "erro_padrao_peso_ct": erro_padrao_peso_ct, "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt, "erro_padrao_peso_dt": erro_padrao_peso_dt, "df_dt": df_dt,
        "medias_racao_ct": medias_racao_ct,
        "medias_racao_dt": medias_racao_dt,
        "df_racao_ct": df_racao_ct, "df_racao_dt": df_racao_dt
    }

def plotar_pesagem(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, 18)  # Eixo X numerado de 1 a 17

    fig = go.Figure()

    # Pesagem da classe CT
    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_ct.values[:17],
        mode='lines+markers',
        name="Peso Médio CT",
        error_y=dict(type='data', array=erro_padrao_peso_ct.values[:17], visible=True),
        line=dict(color='blue')
    ))

    # Pesagem da classe DT
    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_dt.values[:17],
        mode='lines+markers',
        name="Peso Médio DT",
        error_y=dict(type='data', array=erro_padrao_peso_dt.values[:17], visible=True),
        line=dict(color='red')
    ))

    fig.update_layout(
         title="Consumo Médio de Ração",
        xaxis=dict(title="Dias", tickmode="array", tickvals=np.arange(1, len(medias_racao_ct) + 1)),
        yaxis_title="Consumo (g)"
    )

    st.plotly_chart(fig)
    
# Função para plotar o gráfico de consumo de ração
def plotar_consumo_racao(medias_racao_ct, medias_racao_dt):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=np.arange(1, len(medias_racao_ct) + 1),
        y=medias_racao_ct.values,
        mode='lines+markers',
        name="Caixa CT",
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatter(
        x=np.arange(1, len(medias_racao_dt) + 1),
        y=medias_racao_dt.values,
        mode='lines+markers',
        name="Caixa DT",
        line=dict(color='red')
    ))

    fig.update_layout(
        title="Consumo médio de ração", 
        xaxis_title="Dias", 
        yaxis_title="Consumo (g)")
        xaxis=dict(title="Dias", tickmode="array", tickvals=np.arange(1, len(medias_racao_ct) + 1)),
        yaxis_title="Consumo (g)"
    )

    st.plotly_chart(fig)

# Streamlit App
st.title("Análise de Pesagem e Consumo de Ração dos Animais")

uploaded_file = st.file_uploader("Carregar o arquivo Excel com os dados de pesagem", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)

    # Plota o gráfico de pesagem para CT e DT
    plotar_pesagem(
        dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
        dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
    )

    # Plota o gráfico de consumo de ração para CT e DT
    plotar_consumo_racao(
        dados["medias_racao_ct"],
        dados["medias_racao_dt"],
    )

    # Exibe as tabelas
    st.subheader("Tabela de Pesagem para Animais da Classe CT e DT")
    st.write(pd.concat([dados["df_ct"], dados["df_dt"]]))

    st.subheader("Tabela de Consumo de Ração para Caixas CT e DT")
    st.write(pd.concat([dados["df_racao_ct"], dados["df_racao_dt"]]))
