import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

# Função para plotar o gráfico de linhas com erro padrão usando plotly
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
        yaxis_title="Peso (g)",
        #legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center")
        #margin=dict(l=0, r=150, t=50, b=50),
        #legend_title="Classes"
    )
    
    st.plotly_chart(fig)

# Função para plotar o gráfico de área sombreada usando plotly
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
        yaxis_title="Peso (g)",
        #legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center")
        #legend_title="Classes"
        #margin=dict(l=0, r=150, t=50, b=50),
    )

    st.plotly_chart(fig)

# Função para plotar o gráfico de consumo de ração usando plotly
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
        xaxis=dict(title="Dias"),
        yaxis_title="Consumo (g)",
        title_font_shadow="auto",
        #paper_bgcolor="#84998d",
        #plot_bgcolor="#ffffff",
        #legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center")
        #margin=dict(l=0, r=150, t=50, b=50),
        #xaxis=dict(title="Dias",scaleanchor="y", constrain="domain"),
    )

    st.plotly_chart(fig)
    
# Função para plotar o gráfico de linhas com erro padrão usando matplotlib
def plotar_pesagem_mat(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando os dados para Controle
    ax.errorbar(dias, medias_peso_ct.values, yerr=erro_padrao_peso_ct.values, fmt='-o', color='blue', label='Controle')

    # Plotando os dados para Deficiente em tiamina
    ax.errorbar(dias, medias_peso_dt.values, yerr=erro_padrao_peso_dt.values, fmt='-o', color='red', label='Deficiente em tiamina')

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Peso médio dos animais em 16 dias de experimento", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Peso (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)

# Função para plotar o gráfico de área sombreada usando matplotlib
def plotar_pesagem_area_mat(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Faixa sombreada para Controle (CT)
    ax.fill_between(dias, 
                    medias_peso_ct.values - erro_padrao_peso_ct.values, 
                    medias_peso_ct.values + erro_padrao_peso_ct.values, 
                    color='blue', alpha=0.2, label='Controle - Erro padrão')

    # Linha para Controle (CT)
    ax.plot(dias, medias_peso_ct.values, '-o', color='blue', label='Controle')

    # Faixa sombreada para Deficiente em tiamina (DT)
    ax.fill_between(dias, 
                    medias_peso_dt.values - erro_padrao_peso_dt.values, 
                    medias_peso_dt.values + erro_padrao_peso_dt.values, 
                    color='red', alpha=0.2, label='Deficiente em tiamina - Erro padrão')

    # Linha para Deficiente em tiamina (DT)
    ax.plot(dias, medias_peso_dt.values, '-o', color='red', label='Deficiente em tiamina')

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Peso médio dos animais em 16 dias de experimento - erro padrão sombreado", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Peso (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)
    
# Função para plotar o gráfico de consumo de ração usando matplotlib
def plotar_consumo_racao_mat(medias_racao_ct, medias_racao_dt):
    dias = np.arange(1, len(medias_racao_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando a linha para Ração CT
    ax.plot(dias, medias_racao_ct.values, '-o', color='blue', label='Ração CT')

    # Plotando a linha para Ração DT
    ax.plot(dias, medias_racao_dt.values, '-o', color='red', label='Ração DT')

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Consumo médio de ração em 16 dias de experimento", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Consumo (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)
    
# Função para plotar o gráfico de linhas com erro padrão usando seaborn
def plotar_pesagem_seaborn(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando as linhas e barras de erro para Controle (CT)
    ax.errorbar(dias, medias_peso_ct.values, yerr=erro_padrao_peso_ct.values, fmt='-o', color='blue', label='Controle', capsize=5)

    # Plotando as linhas e barras de erro para Deficiente em tiamina (DT)
    ax.errorbar(dias, medias_peso_dt.values, yerr=erro_padrao_peso_dt.values, fmt='-o', color='red', label='Deficiente em tiamina', capsize=5)

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Peso médio dos animais em 16 dias de experimento", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Peso (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)
    
# Função para plotar o gráfico de área sombreada usando seaborn
def plotar_pesagem_area_seaborn(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando a área sombreada para Controle (CT)
    ax.fill_between(dias, 
                    medias_peso_ct.values - erro_padrao_peso_ct.values, 
                    medias_peso_ct.values + erro_padrao_peso_ct.values, 
                    color='blue', alpha=0.2, label='Controle - Erro padrão')

    # Plotando a linha para Controle (CT) usando seaborn
    sns.lineplot(x=dias, y=medias_peso_ct.values, ax=ax, color='blue', label='Controle', marker='o')

    # Plotando a área sombreada para Deficiente em tiamina (DT)
    ax.fill_between(dias, 
                    medias_peso_dt.values - erro_padrao_peso_dt.values, 
                    medias_peso_dt.values + erro_padrao_peso_dt.values, 
                    color='red', alpha=0.2, label='Deficiente em tiamina - Erro padrão')

    # Plotando a linha para Deficiente em tiamina (DT) usando seaborn
    sns.lineplot(x=dias, y=medias_peso_dt.values, ax=ax, color='red', label='Deficiente em tiamina', marker='o')

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Peso médio dos animais em 16 dias de experimento - erro padrão sombreado", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Peso (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)

# Função para plotar o gráfico de consumo de ração usando matplotlib
def plotar_consumo_racao_seaborn(medias_racao_ct, medias_racao_dt):
    dias = np.arange(1, len(medias_racao_ct) + 1)

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando a linha para Ração CT com Seaborn
    sns.lineplot(x=dias, y=medias_racao_ct.values, ax=ax, color='blue', label='Ração CT', marker='o')

    # Plotando a linha para Ração DT com Seaborn
    sns.lineplot(x=dias, y=medias_racao_dt.values, ax=ax, color='red', label='Ração DT', marker='o')

    # Definindo o título e os rótulos dos eixos
    ax.set_title("Consumo médio de ração em 16 dias de experimento", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Consumo (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)

# Streamlit App
st.title("Análise do peso e consumo de ração")

uploaded_file = st.file_uploader("Carregar o arquivo excel com os dados", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)

    # Cria as abas usando st.radio
    aba_selecionada = st.radio(
        "Escolha o tipo de gráfico",
        ("Plotly", "Matplotlib", "Seaborn")
    )

    if aba_selecionada == "Plotly":
        st.subheader("Gráficos com Plotly")
        # Plota todos os gráficos relacionados ao Plotly
        plotar_pesagem(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_pesagem_area(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_consumo_racao(
            dados["medias_racao_ct"],
            dados["medias_racao_dt"],
        )

    elif aba_selecionada == "Matplotlib":
        st.subheader("Gráficos com Matplotlib")
        # Plota todos os gráficos relacionados ao Matplotlib
        plotar_pesagem_mat(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_pesagem_area_mat(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_consumo_racao_mat(
            dados["medias_racao_ct"],
            dados["medias_racao_dt"],
        )

    elif aba_selecionada == "Seaborn":
        st.subheader("Gráficos com Seaborn")
        # Plota todos os gráficos relacionados ao Seaborn
        plotar_pesagem_seaborn(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_pesagem_area_seaborn(
            dados["medias_peso_ct"], dados["erro_padrao_peso_ct"],
            dados["medias_peso_dt"], dados["erro_padrao_peso_dt"]
        )
        plotar_consumo_racao_seaborn(
            dados["medias_racao_ct"],
            dados["medias_racao_dt"],
        )

    # Exibe as tabelas abaixo das abas
    st.subheader("Tabela de peso dos animais CT e DT")
    st.write(pd.concat([dados["df_ct"], dados["df_dt"]]))

    st.subheader("Tabela de consumo de ração das caixas CT e DT")
    st.write(pd.concat([dados["df_racao_ct"], dados["df_racao_dt"]]))
