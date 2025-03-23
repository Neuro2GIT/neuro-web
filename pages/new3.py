import streamlit as st
import pandas as pd
import numpy as np

# Funções para processar o peso e o consumo de ração
def processar_peso(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']
    medias_peso_ct = df_ct.iloc[:, 2:].mean()  
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    return {
        "medias_peso_ct": medias_peso_ct, 
        "erro_padrao_peso_ct": erro_padrao_peso_ct, 
        "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt, 
        "erro_padrao_peso_dt": erro_padrao_peso_dt, 
        "df_dt": df_dt
    }

def processar_consumo_racao(uploaded_file):
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']
    medias_racao_ct = df_racao_ct.iloc[:, 2:].mean()
    medias_racao_dt = df_racao_dt.iloc[:, 2:].mean()
    media_geral_racao_ct = medias_racao_ct.mean()
    media_geral_racao_dt = medias_racao_dt.mean()

    return {
        "medias_racao_ct": medias_racao_ct,
        "medias_racao_dt": medias_racao_dt,
        "media_geral_racao_ct": media_geral_racao_ct,
        "media_geral_racao_dt": media_geral_racao_dt,
        "df_racao_ct": df_racao_ct, 
        "df_racao_dt": df_racao_dt
    }

def carregar_e_processar_excel(uploaded_file):
    resultado_peso = processar_peso(uploaded_file)
    resultado_racao = processar_consumo_racao(uploaded_file)
    resultado_completo = {**resultado_peso, **resultado_racao}
    return resultado_completo

# Interface Streamlit
st.title("Análise de Pesagem e Consumo de Ração")

uploaded_file = st.file_uploader("Carregar Arquivo Excel", type=["xlsx"])

if uploaded_file:
    # Processar os dados
    resultado_peso = processar_peso(uploaded_file)
    resultado_racao = processar_consumo_racao(uploaded_file)
    resultado_completo = carregar_e_processar_excel(uploaded_file)

    # Exibir DataFrame com as médias e erros padrão de peso (por classe)
    st.subheader("Resultado - Peso dos Animais")
    st.write("Médias e erro padrão do peso para animais CT:")
    st.dataframe(resultado_peso["df_ct"])

    st.write("Médias e erro padrão do peso para animais DT:")
    st.dataframe(resultado_peso["df_dt"])

    # Exibir DataFrame com o consumo de ração (por classe)
    st.subheader("Resultado - Consumo de Ração")
    st.write("Média de consumo de ração para classe CT:")
    st.dataframe(resultado_racao["df_racao_ct"])

    st.write("Média de consumo de ração para classe DT:")
    st.dataframe(resultado_racao["df_racao_dt"])

    # Exibir resumo das médias gerais
    st.subheader("Médias Gerais de Consumo de Ração")
    st.write(f"Média geral de ração para CT: {resultado_racao['media_geral_racao_ct']}")
    st.write(f"Média geral de ração para DT: {resultado_racao['media_geral_racao_dt']}")

    # Exibir a função principal (resultado completo)
    st.subheader("Resultado Completo - Peso e Consumo de Ração")
    st.write("Médias e erros padrões de peso e consumo de ração combinados:")
    st.dataframe(pd.concat([resultado_completo['df_ct'], resultado_completo['df_dt']]))
