import streamlit as st
import pandas as pd
import numpy as np
import matplotlib  
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Análise de peso e ração",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={})
st.set_option('client.showErrorDetails', True)

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")

    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Separar dados de consumo por classe
    #df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    #df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Calculo da média do peso e erro padrão para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean() #numeric_only=True
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])

    # Calculo da média do peso e erro padrão para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    # Dicionário com o resultado dos dados processados
    return {
        "medias_peso_ct": medias_peso_ct, "erro_padrao_peso_ct": erro_padrao_peso_ct, "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt, "erro_padrao_peso_dt": erro_padrao_peso_dt, "df_dt": df_dt,
    }

    # Criar o DataFrame com as médias para cada dia em cada classe
    #df_resultado = pd.DataFrame({
        #"Média Peso CT": medias_peso_ct,
        #"Erro Padrão Peso CT": erro_padrao_peso_ct,
        #"Média Peso DT": medias_peso_dt,
        #"Erro Padrão Peso DT": erro_padrao_peso_dt
    #}).T

    # Criar DataFrame com as médias e erros padrões de peso
    #df_medias_e_erros = pd.DataFrame({
    #"Grupo": ["CT", "DT"],
    #"Média Peso": [
        #dados["medias_peso_ct"].mean(),  # Média do peso para CT
        #dados["medias_peso_dt"].mean()   # Média do peso para DT
    #],
    #"Erro Padrão Peso": [
        #dados["erro_padrao_peso_ct"],  # Erro padrão do peso para CT
        #dados["erro_padrao_peso_dt"]   # Erro padrão do peso para DT
    #]
    #})

def processar_consumo_racao(uploaded_file):
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")
    
    # Filtragem dos dados por classe de caixa
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Cálculo da média de consumo de ração CT e DT para cada dia
    medias_racao_ct = df_racao_ct.iloc[:, 2:].mean()
    medias_racao_dt = df_racao_dt.iloc[:, 2:].mean()

    # Cálculo da média geral de consumo para cada grupo
    media_geral_racao_ct = medias_racao_ct.mean()
    media_geral_racao_dt = medias_racao_dt.mean()

    # Dicionário com os resultados do consumo
    return {
        "medias_racao_ct": medias_racao_ct, 
        "medias_racao_dt": medias_racao_dt,
        "df_racao_dt": df_racao_dt,
        "df_racao_ct": df_racao_ct,
        "media_geral_racao_ct": media_geral_racao_ct,
        "media_geral_racao_dt": media_geral_racao_dt,
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

    # Atualizando o layout para ajustar a escala
    fig.update_layout(
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento",
        title_x=(0.5),
        title_xanchor=('center'),
        yaxis_title="Peso (g)",
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center"),
        xaxis=dict(title="Dias", tickmode="array", tickvals=dias),
        height=600,
        width=600
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
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento - erro padrão sombreado",
        title_x=(0.5),
        title_xanchor=('center'),
        yaxis_title="Peso (g)",
        xaxis=dict(title="Dias", tickmode="array", tickvals=dias),
        #xaxis=dict(title="Dias", range=[dias.min(), dias.max()], scaleanchor="y"),
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center"),
        height=600,
        width=600
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
        title=f"Consumo médio de ração em {dias.max() - dias.min() + 1} dias de experimento",
        yaxis_title="Consumo (g)",
        xaxis=dict(title="Dias", tickmode="array", tickvals=dias),
        title_font_shadow="auto",
        title_x=(0.5),
        title_xanchor=('center'),
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center"),
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
    ax.set_title(f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento", fontsize=16)
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
    ax.set_title(f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento - erro padrão sombreado", fontsize=16)
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
    ax.set_title(f"Consumo médio de ração em {dias.max() - dias.min() + 1} dias de experimento", fontsize=16)
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
    ax.set_title(f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento", fontsize=16)
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
    ax.set_title(f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento - erro padrão sombreado", fontsize=16)
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
    ax.set_title(f"Consumo médio de ração em {dias.max() - dias.min() + 1} dias de experimento", fontsize=16)
    ax.set_xlabel("Dias", fontsize=12)
    ax.set_ylabel("Consumo (g)", fontsize=12)

    # Adicionando a legenda
    ax.legend()

    # Exibindo o gráfico
    st.pyplot(fig)

def plotar_pesagem_altair(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    # Criando um DataFrame adequado para Altair
    df_plot = pd.DataFrame({
        "Dias": np.concatenate([np.arange(1, len(medias_peso_ct) + 1)] * 2),
        "Peso Médio": np.concatenate([medias_peso_ct.values, medias_peso_dt.values]),
        "Erro Inferior": np.concatenate([medias_peso_ct.values - erro_padrao_peso_ct.values, 
                                         medias_peso_dt.values - erro_padrao_peso_dt.values]),
        "Erro Superior": np.concatenate([medias_peso_ct.values + erro_padrao_peso_ct.values, 
                                         medias_peso_dt.values + erro_padrao_peso_dt.values]),
        "Grupo": ["Controle"] * len(medias_peso_ct) + ["Deficiente em tiamina"] * len(medias_peso_dt)
    })

    # Gráfico principal de linha com pontos
    base = alt.Chart(df_plot).mark_line(point=True).encode(
        x=alt.X("Dias:O", title="Dias"),
        y=alt.Y("Peso Médio:Q", title="Peso (g)"),
        color=alt.Color("Grupo:N", scale=alt.Scale(domain=["Controle", "Deficiente em tiamina"], 
                                                   range=["blue", "red"])),
        tooltip=["Dias", "Peso Médio", "Grupo"]
    )

    # Adicionando as barras de erro com `mark_rule`
    erro = alt.Chart(df_plot).mark_rule().encode(
        x="Dias:O",
        y="Erro Inferior:Q",
        y2="Erro Superior:Q",
        color=alt.Color("Grupo:N", scale=alt.Scale(domain=["Controle", "Deficiente em tiamina"], 
                                                   range=["blue", "red"]))
    )

    # Combinando os gráficos
    chart = (base + erro).properties(
        title="Peso médio dos animais ao longo dos dias",
        width=600,
        height=400
    )

    # Exibindo no Streamlit
    st.altair_chart(chart, use_container_width=True)

def plotar_pesagem_area_altair(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    # Criando DataFrame para o gráfico
    df_plot = pd.DataFrame({
        "Dias": np.concatenate([np.arange(1, len(medias_peso_ct) + 1)] * 2),
        "Peso Médio": np.concatenate([medias_peso_ct.values, medias_peso_dt.values]),
        "Erro Inferior": np.concatenate([medias_peso_ct.values - erro_padrao_peso_ct.values, 
                                         medias_peso_dt.values - erro_padrao_peso_dt.values]),
        "Erro Superior": np.concatenate([medias_peso_ct.values + erro_padrao_peso_ct.values, 
                                         medias_peso_dt.values + erro_padrao_peso_dt.values]),
        "Grupo": ["Controle"] * len(medias_peso_ct) + ["Deficiente em tiamina"] * len(medias_peso_dt)
    })

    # Gráfico de área preenchendo a região de erro
    area = alt.Chart(df_plot).mark_area(opacity=0.3).encode(
        x=alt.X("Dias:O", title="Dias"),
        y="Erro Inferior:Q",
        y2="Erro Superior:Q",
        color=alt.Color("Grupo:N", scale=alt.Scale(domain=["Controle", "Deficiente em tiamina"], 
                                                   range=["blue", "red"]))
    )

    # Gráfico de linha principal com pontos
    base = alt.Chart(df_plot).mark_line(point=True).encode(
        x=alt.X("Dias:O", title="Dias"),
        y=alt.Y("Peso Médio:Q", title="Peso (g)"),
        color=alt.Color("Grupo:N", scale=alt.Scale(domain=["Controle", "Deficiente em tiamina"], 
                                                   range=["blue", "red"])),
        tooltip=["Dias", "Peso Médio", "Grupo"]
    )

    # Combinando gráficos
    chart = (area + base).properties(
        title="Peso médio dos animais com faixa de erro",
        width=600,
        height=400
    )

    # Exibindo no Streamlit
    st.altair_chart(chart, use_container_width=True)

def plotar_pesagem_altair(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    """
    Função para plotar o gráfico de linha com erro padrão usando Altair.

    Parameters:
    medias_peso_ct (pd.Series): Médias de peso para os animais da classe Controle.
    erro_padrao_peso_ct (pd.Series): Erro padrão para os animais da classe Controle.
    medias_peso_dt (pd.Series): Médias de peso para os animais da classe Deficiente em Tiamina.
    erro_padrao_peso_dt (pd.Series): Erro padrão para os animais da classe Deficiente em Tiamina.
    """
    # Gerando os dias com base no número de elementos nas médias
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando DataFrame para a classe Controle (CT)
    df_ct = pd.DataFrame({
        'Dias': dias,
        'Peso': medias_peso_ct.values,
        'Erro': erro_padrao_peso_ct.values,
        'Classe': 'Controle'
    })

    # Criando DataFrame para a classe Deficiente em Tiamina (DT)
    df_dt = pd.DataFrame({
        'Dias': dias,
        'Peso': medias_peso_dt.values,
        'Erro': erro_padrao_peso_dt.values,
        'Classe': 'Deficiente em Tiamina'
    })

    # Concatenando os dois DataFrames
    df = pd.concat([df_ct, df_dt])

    # Criando o gráfico de linha com Altair
    chart = alt.Chart(df).mark_line().encode(
        x='Dias:O',
        y='Peso:Q',
        color='Classe:N',
        detail='Classe:N'
    ).properties(
        title="Peso médio dos animais com erro padrão"
    )

    # Adicionando as bandas de erro (intervalos de erro)
    chart = chart + alt.Chart(df).mark_errorbar().encode(
        x='Dias:O',
        y='Peso:Q',
        yError='Erro:Q',
        color='Classe:N'
    )

    chart.show()
    
# Dicionário de funções
plot_funcs = {
    "Plotly": {
        "pesagem": plotar_pesagem,
        "pesagem_area": plotar_pesagem_area,
        "consumo_racao": plotar_consumo_racao
    },
    "Matplotlib": {
        "pesagem": plotar_pesagem_mat,
        "pesagem_area": plotar_pesagem_area_mat,
        "consumo_racao": plotar_consumo_racao_mat
    },
    "Seaborn": {
        "pesagem": plotar_pesagem_seaborn,
        "pesagem_area": plotar_pesagem_area_seaborn,
        "consumo_racao": plotar_consumo_racao_seaborn
    },
    "Altair": {
        "pesagem": plotar_pesagem_altair,
        "pesagem_area": plotar_pesagem_area_altair,
        "consumo_racao": plotar_consumo_racao_seaborn
    }
}

# Streamlit App
st.title("Peso e consumo de ração")
st.markdown("---")

with st.container(border=True):
    uploaded_file = st.file_uploader("Para utilizar, converta a sua planilha para o modelo ou gere uma nova no gerador de planilhas", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)
    resultados_racao = processar_consumo_racao(uploaded_file)

    with st.container(border=True):
        # Cria as abas usando st.radio
        aba_selecionada = st.radio(
            "Selecione uma biblioteca abaixo para navegar entre as opções",
            ("Plotly", "Matplotlib", "Seaborn",)
        )

    # Seleciona as funções de acordo com a biblioteca escolhida
    plotar_funcoes = plot_funcs[aba_selecionada]
    
    st.subheader(f"{aba_selecionada}")

    # Exibe os gráficos correspondentes
    with st.expander("Gráficos - peso médio dos animais e consumo de ração"): 
        with st.container(border=True):
            plotar_funcoes["pesagem"](dados["medias_peso_ct"], dados["erro_padrao_peso_ct"], dados["medias_peso_dt"], dados["erro_padrao_peso_dt"])

        with st.container(border=True):
            plotar_funcoes["pesagem_area"](dados["medias_peso_ct"], dados["erro_padrao_peso_ct"], dados["medias_peso_dt"], dados["erro_padrao_peso_dt"])

        with st.container(border=True):
            plotar_funcoes["consumo_racao"](resultados_racao["medias_racao_ct"], resultados_racao["medias_racao_dt"])


    # Carregar as médias de ração
    racao_processada = carregar_e_processar_excel(uploaded_file)

    st.markdown("---")

    st.subheader ("Tabelas para verificação")
    with st.expander("Dados processados: médias e erro padrão"):
        
        # Dataframe com as medias
        with st.container(border=True):
            df_medias = pd.DataFrame({
                "Grupo CT": dados["medias_peso_ct"],
                "Grupo DT": dados["medias_peso_dt"]
            })
            df_medias = df_medias.T # Transpor para que as métricas fiquem nas linhas e os dias/observações nas colunas
            st.write("Médias de peso")
            st.dataframe(df_medias)

        st.write("")

        # Dataframe com o erro padrão
        with st.container(border=True):
            df_errpadrao = pd.DataFrame({
                "Grupo CT": dados["erro_padrao_peso_ct"],
                "Grupo DT": dados["erro_padrao_peso_dt"]
            })
            df_errpadrao = df_errpadrao.T # Transpor para que as métricas fiquem nas linhas e os dias/observações nas colunas
            st.write("Erro padrão dos pesos")
            st.dataframe(df_errpadrao)

        st.write("")
        
        # Dataframe com as medias do cosumo de ração
        with st.container(border=True):
            df_medias_gerais = pd.DataFrame({
                "Grupo": ["CT", "DT"],
                "Médias de consumo de ração": [
                    resultados_racao["medias_racao_ct"],  # Usando a variável 'dados' para acessar a média
                    resultados_racao["medias_racao_dt"]   # Usando a variável 'dados' para acessar a média
                ]
            })
            st.write("Médias de consumo de ração por grupo")
            df_medias_gerais.set_index("Grupo", inplace=True)
            st.dataframe(df_medias_gerais)

        with st.container(border=True):
            st.write("Médias de consumo de ração por grupo")
            df_racao = pd.concat([resultados_racao["medias_racao_ct"], resultados_racao["medias_racao_dt"]])
            df_racao.set_index("Classe da Caixa", inplace=True)
            st.write(df_racao)
    

    # Dados brutos de peso e consumo de ração em tabelas
    with st.expander("Dados brutos: peso e consumo de ração"):
        with st.container(border=True):
            st.write("Peso dos animais")
            df_peso_animais = pd.concat([dados["df_ct"], dados["df_dt"]])
            df_peso_animais.set_index("Classe do Animal", inplace=True)
            st.write(df_peso_animais)

        with st.container(border=True):
            st.write("Consumo de ração por caixa")
            df_racao = pd.concat([resultados_racao["df_racao_ct"], resultados_racao["df_racao_dt"]])
            df_racao.set_index("Classe da Caixa", inplace=True)
            st.write(df_racao)
            #st.write(pd.concat([dados["df_racao_ct"], dados["df_racao_dt"]]))

        # Dataframe com a media geral do cosumo de ração
        with st.container(border=True):
            df_medias_gerais = pd.DataFrame({
                "Grupo": ["CT", "DT"],
                "Média do consumo de ração": [
                    resultados_racao["media_geral_racao_ct"],  # Usando a variável 'dados' para acessar a média
                    resultados_racao["media_geral_racao_dt"]   # Usando a variável 'dados' para acessar a média
                ]
            })
            st.write("Média geral de consumo de ração por grupo")
            df_medias_gerais.set_index("Grupo", inplace=True)
            st.dataframe(df_medias_gerais)

    # Exibir os valores de forma destacada
    #st.metric(label="Média do consumo CT", value=round(racao_processada["media_geral_racao_ct"], 2))
    #st.metric(label="Média do consumo DT", value=round(racao_processada["media_geral_racao_dt"], 2))
