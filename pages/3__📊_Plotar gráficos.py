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

    # Cálculo da média geral do consumo de ração CT e DT
    media_geral_racao_ct = medias_racao_ct.mean()
    media_geral_racao_dt = medias_racao_dt.mean()

    # Dicionário com o resultado dos dados processados
    return {
        "medias_peso_ct": medias_peso_ct, "erro_padrao_peso_ct": erro_padrao_peso_ct, "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt, "erro_padrao_peso_dt": erro_padrao_peso_dt, "df_dt": df_dt,
        "medias_racao_ct": medias_racao_ct,
        "medias_racao_dt": medias_racao_dt,
        "media_geral_racao_ct": media_geral_racao_ct,
        "media_geral_racao_dt": media_geral_racao_dt,
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

    # Atualizando o layout para ajustar a escala
    fig.update_layout(
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento",
        title_x=(0.5),
        title_xanchor=('center'),
        yaxis_title="Peso (g)",
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center"),
        xaxis=dict(title="Dias", tickmode="array", tickvals=dias),
        #xaxis=dict(title="Dias", range=[dias.min() - 1, dias.max() + 1], scaleanchor="y"),  # Limite do eixo X (dias)
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
        #height=600,
        #width=600
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

# Função para plotar o gráfico de linhas com erro padrão usando Altair
def plotar_pesagem_alt(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)
    
    # Criando os DataFrames para Controle e Deficiente em tiamina
    df_ct = pd.DataFrame({
        'Dia': dias,
        'Peso': medias_peso_ct.values,
        'Erro': erro_padrao_peso_ct.values,
        'Grupo': 'Controle'
    })
    
    df_dt = pd.DataFrame({
        'Dia': dias,
        'Peso': medias_peso_dt.values,
        'Erro': erro_padrao_peso_dt.values,
        'Grupo': 'Deficiente em tiamina'
    })
    
    # Concatenando os dois DataFrames
    df = pd.concat([df_ct, df_dt], ignore_index=True)

     # Exibindo o DataFrame no Streamlit para verificação
    st.write("Dados do gráfico:", df)

    # Definindo a escala para os eixos X e Y
    x_scale = alt.Scale(domain=[df['Dia'].min(), df['Dia'].max()])  # Ajustando o eixo X com base nos dados
    y_scale = alt.Scale(domain=[df['Peso'].min() - df['Erro'].max(), df['Peso'].max() + df['Erro'].max()])  # Ajustando o eixo Y com base nos dados

    # Criação do gráfico de linha
    line_chart = alt.Chart(df).mark_line().encode(
        x='Dia:O',  # Eixo X como ordinal para os dias
        y='Peso:Q',  # Eixo Y com valores quantitativos para o peso
        color='Grupo:N',  # Cor por grupo (Controle e Deficiente em tiamina)
        detail='Grupo:N'  # Detalhamento por grupo para distinguir as linhas
    )
    
    error_bars = alt.Chart(df).mark_errorbar().encode(
    x=alt.X('Dia:O', scale=x_scale),  # Eixo X (dias) com escala ajustada
    y='Peso:Q',  # Eixo Y (peso)
    y2='Peso + Erro:Q',  # Valor final da barra de erro (Peso + Erro)
    color='Grupo:N',  # Cor por grupo
    size=alt.value(10)  # Tamanho da barra de erro
    )
    
    # Adicionando barras de erro para o gráfico
    #error_bars = alt.Chart(df).mark_errorbar().encode(
        #x='Dia:O',  # Eixo X (dias)
        #y='Peso:Q',  # Eixo Y (peso)
        #y2='Peso + Erro:Q',  # Valor final da barra de erro (Peso + Erro)
        #y2='Peso:Q',  # Início da barra de erro
        #color='Grupo:N',  # Cor por grupo
        #size=alt.value(10)  # Tamanho da barra de erro
    #).transform_calculate(
        #y2='datum.Peso + datum.Erro'  # A barra de erro vai de Peso até Peso + Erro
    #)

    # Combina o gráfico de linha com as barras de erro
    chart = (line_chart + error_bars).properties(
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento",
        width=600,
        height=400
    ).configure_scale(
        bandPaddingInner=0.2
    ).interactive()

    # Exibir o gráfico no Streamlit
    st.altair_chart(error_bars, use_container_width=True)

# Função para plotar o gráfico de área sombreada usando Altair
def plotar_pesagem_area_alt(medias_peso_ct, erro_padrao_peso_ct, medias_peso_dt, erro_padrao_peso_dt):
    dias = np.arange(1, len(medias_peso_ct) + 1)

    # Criando DataFrame para CT (Controle)
    df_ct = pd.DataFrame({
        'dias': np.concatenate((dias, dias[::-1])),
        'peso': np.concatenate((medias_peso_ct.values + erro_padrao_peso_ct.values, 
                                (medias_peso_ct.values - erro_padrao_peso_ct.values)[::-1])),
        'grupo': ['CT'] * len(np.concatenate((dias, dias[::-1])))
    })

    # Criando DataFrame para DT (Deficiente em tiamina)
    df_dt = pd.DataFrame({
        'dias': np.concatenate((dias, dias[::-1])),
        'peso': np.concatenate((medias_peso_dt.values + erro_padrao_peso_dt.values, 
                                (medias_peso_dt.values - erro_padrao_peso_dt.values)[::-1])),
        'grupo': ['DT'] * len(np.concatenate((dias, dias[::-1])))
    })

    # Criando DataFrame para os valores médios de CT e DT
    df_valores = pd.DataFrame({
        'dias': dias,
        'medias_ct': medias_peso_ct.values,
        'medias_dt': medias_peso_dt.values,
    })

    # Gráfico de área sombreada para CT
    area_ct = alt.Chart(df_ct).mark_area(
        opacity=0.2,
        line={'color': 'white'}
    ).encode(
        x=alt.X('dias:Q', scale=alt.Scale(domain=[dias.min(), dias.max()])),  # Escala do eixo X (dias)
        y=alt.Y('peso:Q', scale=alt.Scale(domain=[0, medias_peso_ct.max() + 10])),  # Escala do eixo Y (peso)
        color=alt.Color('grupo:N', scale=alt.Scale(domain=['CT'], range=['blue']))
    ).properties(
    )

    # Gráfico de linha para CT
    linha_ct = alt.Chart(df_valores).mark_line(
        color='blue'
    ).encode(
        x='dias:Q',
        y='medias_ct:Q'
    )

    # Gráfico de área sombreada para DT
    area_dt = alt.Chart(df_dt).mark_area(
        opacity=0.2,
        line={'color': 'white'}
    ).encode(
        x='dias:Q',
        y='peso:Q',
        color=alt.Color('grupo:N', scale=alt.Scale(domain=['DT'], range=['red']))
    )

    # Gráfico de linha para DT
    linha_dt = alt.Chart(df_valores).mark_line(
        color='red'
    ).encode(
        x='dias:Q',
        y='medias_dt:Q'
    )

    # Combinando os gráficos
    grafico_final = (area_ct + linha_ct + area_dt + linha_dt).properties(
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento - erro padrão sombreado",
        #title='Peso médio dos animais em 16 dias de experimento - erro padrão sombreado'
        titleAnchor='middle'
    ).configure_title(
        fontSize=16,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    grafico_final = (area_ct + linha_ct + area_dt + linha_dt).properties(
        title=f"Peso médio dos animais em {dias.max() - dias.min() + 1} dias de experimento - erro padrão sombreado",
        #title='Peso médio dos animais em 16 dias de experimento - erro padrão sombreado'
    ).configure_title(
        fontSize=16,
        align='center',  # Ajuste do alinhamento do título
        baseline='middle'  # Ajuste da posição vertical do título
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(grafico_final)


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
        "pesagem": plotar_pesagem_alt,
        "pesagem_area": plotar_pesagem_area_alt
    }
}

# Streamlit App
st.title("Gráficos - Peso e Consumo de Ração")

with st.expander("Como usar?"):
    st.write("Converta a sua planilha para o modelo ou gere uma nova no gerador de planilhas")

with st.container(border=True):
    uploaded_file = st.file_uploader("Selecione um arquivo excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Processa os dados
    dados = carregar_e_processar_excel(uploaded_file)

    # Cria as abas usando st.radio
    aba_selecionada = st.radio(
        "Escolha a biblioteca",
        ("Plotly", "Matplotlib", "Seaborn", "Altair")
    )

    # Seleciona as funções de acordo com a biblioteca escolhida
    plotar_funcoes = plot_funcs[aba_selecionada]

    st.subheader(f"Gráficos com {aba_selecionada}")

    # Exibe os gráficos correspondentes
    with st.container(border=True):
        plotar_funcoes["pesagem"](dados["medias_peso_ct"], dados["erro_padrao_peso_ct"], dados["medias_peso_dt"], dados["erro_padrao_peso_dt"])

    with st.container(border=True):
        plotar_funcoes["pesagem_area"](dados["medias_peso_ct"], dados["erro_padrao_peso_ct"], dados["medias_peso_dt"], dados["erro_padrao_peso_dt"])

    with st.container(border=True):
        plotar_funcoes["consumo_racao"](dados["medias_racao_ct"], dados["medias_racao_dt"])

    # Exibe os gráficos correspondentes de forma dinâmica
    #for nome_grafico, funcao in plotar_funcoes.items():
       # with st.container(border=True):
            # Chama a função de plotagem com os parâmetros corretos
            #funcao(*parametros_por_grafico[nome_grafico])

    # Exibe as tabelas abaixo das abas
    st.subheader("Tabela de peso dos animais CT e DT")
    st.write(pd.concat([dados["df_ct"], dados["df_dt"]]))

    st.subheader("Tabela de consumo de ração das caixas CT e DT")
    st.write(pd.concat([dados["df_racao_ct"], dados["df_racao_dt"]]))

    # Carregar as médias de ração
    #racao_processada = carregar_e_processar_excel(uploaded_file)

    ## Criar DataFrame para consumo geral de ração
    #df_medias_gerais = pd.DataFrame({
        #"Grupo": ["CT", "DT"],
        #"Média do consumo de ração": [racao_processada["media_geral_racao_ct"], racao_processada["media_geral_racao_dt"]]
    #})

    # Criar DataFrame para consumo geral de ração
    df_medias_gerais = pd.DataFrame({
        "Grupo": ["CT", "DT"],
        "Média do consumo de ração": [
            dados["media_geral_racao_ct"],  # Usando a variável 'dados' para acessar a média
            dados["media_geral_racao_dt"]   # Usando a variável 'dados' para acessar a média
        ]
    })

    # Exibir os dados em formato de tabela
    st.write("### Média geral do consumo de ração")
    st.dataframe(df_medias_gerais)

    # st.expander("Clique para mais informações sobre o aplicativo"):

    # Criar gráfico de barras usando dados do DataFrame
    #fig = px.bar(df_medias_gerais, x="Grupo", y="Média do consumo de ração",
                 #title="Média geral de consumo de ração por grupo", text_auto=True)
    #st.plotly_chart(fig)

    # Exibir os valores de forma destacada
    #st.metric(label="Média do consumo CT", value=round(racao_processada["media_geral_racao_ct"], 2))
    #st.metric(label="Média do consumo DT", value=round(racao_processada["media_geral_racao_dt"], 2))
