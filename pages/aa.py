import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregar as planilhas do arquivo Excel
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Separar dados de consumo por classe
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']

    # Calculo da média do peso e erro padrão para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()  # Calculando a média das colunas de peso
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])  # Calculando o erro padrão

    # Calculo da média do peso e erro padrão para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    # Dicionário com os dados processados
    return {
        "medias_peso_ct": medias_peso_ct, "erro_padrao_peso_ct": erro_padrao_peso_ct,
        "medias_peso_dt": medias_peso_dt, "erro_padrao_peso_dt": erro_padrao_peso_dt
    }

# Interface do Streamlit
st.title('Análise de Pesagem e Consumo de Ração')

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Processar os dados
    dados_processados = carregar_e_processar_excel(uploaded_file)

    # Obter as médias dos pesos
    medias_peso_ct = dados_processados['medias_peso_ct']
    medias_peso_dt = dados_processados['medias_peso_dt']

    # Criar o DataFrame para as médias
    df_resultado = pd.DataFrame({
        "Média Peso CT": medias_peso_ct,
        "Média Peso DT": medias_peso_dt,
    }).T  # Transposta para que as linhas sejam as métricas (Média Peso CT e Média Peso DT)

    # Transformar o DataFrame para um formato longo
    df_resultado_long = df_resultado.reset_index().melt(id_vars=["index"], var_name="Métrica", value_name="Valor")
    df_resultado_long.rename(columns={"index": "Dia"}, inplace=True)

    # Criar o gráfico com Altair
    chart = alt.Chart(df_resultado_long).mark_line().encode(
        x='Dia:O',  # Eixo X (dias), 'O' para ordinal
        y='Valor:Q',  # Eixo Y (valores das médias), 'Q' para quantitativo
        color='Métrica:N',  # Cor para diferenciar as métricas (Peso CT vs Peso DT)
        detail='Métrica:N'  # Detalhes para que o gráfico mostre diferentes linhas para cada métrica
    )

    # Exibir o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)

else:
    st.warning("Por favor, carregue um arquivo Excel para ver o gráfico.")
