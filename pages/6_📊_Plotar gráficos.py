import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Separar dados de consumo por classe
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Calculo da média do peso e erro padrão para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])

    # Calculo da média do peso e erro padrão para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    # Calculo da média do consumo de ração CT e DT
    medias_racao_ct = df_racao_ct.iloc[:, 2:].mean()
    medias_racao_dt = df_racao_dt.iloc[:, 2:].mean()

    # Dicionário com o resultado dos dados processados
    return {
        "medias_peso_ct": medias_peso_ct, "erro_padrao_peso_ct": erro_padrao_peso_ct, "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt, "erro_padrao_peso_dt": erro_padrao_peso_dt, "df_dt": df_dt,
        "medias_racao_ct": medias_racao_ct,
        "medias_racao_dt": medias_racao_dt,
        "df_racao_ct": df_racao_ct, "df_racao_dt": df_racao_dt
    }

# Função para plotar o gráfico de linhas com erro padrão
def plotar_pesagem(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_ct.values,
        mode='lines+markers',
        name="Controle",
        error_y=dict(type='data', array=erro_padrao_peso_ct.values, visible=True),
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_dt.values,
        mode='lines+markers',
        name="Deficiente em tiamina",
        error_y=dict(type='data', array=erro_padrao_peso_dt.values, visible=True),
        line=dict(color='red')
    ))

    fig.update_layout(
        title="Peso médio dos animais em 16 dias de experimento",
        xaxis=dict(title="Dias",scaleanchor="y"),
        yaxis_title="Peso (g)"
        #legend_title="Classes"
    )
    
    st.plotly_chart(fig)

# Função para plotar o gráfico de área sombreada
def plotar_pesagem_area(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    fig = go.Figure()

    # Faixa sombreada para CT
    fig.add_trace(go.Scatter(
        x=np.concatenate((dias, dias[::-1])),
        y=np.concatenate((medias_peso_ct.values + erro_padrao_peso_ct.values, 
                          (medias_peso_ct.values - erro_padrao_peso_ct.values)[::-1])),
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_ct.values,
        mode='lines+markers',
        name="Controle",
        line=dict(color='blue')
    ))

    # Faixa sombreada para DT
    fig.add_trace(go.Scatter(
        x=np.concatenate((dias, dias[::-1])),
        y=np.concatenate((medias_peso_dt.values + erro_padrao_peso_dt.values, 
                          (medias_peso_dt.values - erro_padrao_peso_dt.values)[::-1])),
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_peso_dt.values,
        mode='lines+markers',
        name="Deficiente em tiamina",
        line=dict(color='red')
    ))

    fig.update_layout(
        title="Peso médio dos animais em 16 dias de experimento - erro padrão sombreado",
        xaxis=dict(title="Dias"),
        yaxis_title="Peso (g)"
        #legend_title="Classes"
    )

    st.plotly_chart(fig)

# Função para plotar o gráfico de consumo de ração
def plotar_consumo_racao(medias_racao_ct, medias_racao_dt):
    dias = np.arange(1, len(medias_racao_ct) + 1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_racao_ct.values,
        mode='lines+markers',
        name="Ração CT",
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=dias,
        y=medias_racao_dt.values,
        mode='lines+markers',
        name="Ração DT",
        line=dict(color='red')
    ))

    fig.update_layout(
        title="Consumo médio de ração em 16 dias de experimento",
        width=800,  # Largura fixa
        height=500,  # Altura fixa
        xaxis=dict(title="Dias"),
        #xaxis=dict(title="Dias",scaleanchor="y", constrain="domain"),
        yaxis_title="Consumo (g)",
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center")
    )

    st.plotly_chart(fig)

# Streamlit App
st.title("Análise do peso e consumo de ração")

uploaded_file = st.file_uploader("Carregar o arquivo excel com os dados", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)

    # Plota o gráfico de pesagem (linha + barras de erro)
    plotar_pesagem(
        dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
        dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
    )

    # Plota o gráfico de pesagem com área sombreada
    plotar_pesagem_area(
        dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
        dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
    )

    # Plota o gráfico de consumo de ração
    plotar_consumo_racao(
        dados["medias_racao_ct"],
        dados["medias_racao_dt"],
    )

    # Exibe as tabelas
    st.subheader("Tabela de peso dos animais CT e DT")
    st.write(pd.concat([dados["df_ct"], dados["df_dt"]]))

    st.subheader("Tabela de consumo de ração das caixas CT e DT")
    st.write(pd.concat([dados["df_racao_ct"], dados["df_racao_dt"]]))
