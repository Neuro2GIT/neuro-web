import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregar as planilhas do arquivo Excel
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    
    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Calculo da média do peso para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()  # Considerando as colunas de peso
    # Calculo da média do peso para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()

    # Dicionário com o resultado dos dados processados
    return {
        "medias_peso_ct": medias_peso_ct,
        "medias_peso_dt": medias_peso_dt
    }

# Interface do Streamlit
st.title('Análise de Pesagem de Animais')

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Processar os dados
    dados_processados = carregar_e_processar_excel(uploaded_file)

    # Obter as médias dos pesos
    medias_peso_ct = dados_processados['medias_peso_ct']
    medias_peso_dt = dados_processados['medias_peso_dt']

    # Criar o DataFrame para as médias de peso (por classe)
    df_resultado = pd.DataFrame({
        "CT": medias_peso_ct,
        "DT": medias_peso_dt,
    })  # Não precisamos da transposição aqui, pois as classes são as colunas

    # Adicionar a coluna de dias
    df_resultado['Dia'] = df_resultado.index + 1  # Criar a coluna de dias (1, 2, 3,...)

    # Transformar o DataFrame para o formato longo
    df_resultado_long = df_resultado.reset_index().melt(id_vars=["Dia"], var_name="Classe", value_name="Peso")

    # Criar o gráfico com Altair
    chart = alt.Chart(df_resultado_long).mark_line().encode(
        x='Dia:O',  # Eixo X (dias), 'O' para ordinal
        y='Peso:Q',  # Eixo Y (valores dos pesos), 'Q' para quantitativo
        color='Classe:N',  # Cor para diferenciar as classes (CT vs DT)
        detail='Classe:N'  # Detalhes para mostrar linhas separadas para cada classe
    )

    # Exibir o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)

else:
    st.warning("Por favor, carregue um arquivo Excel para ver o gráfico.")
