import streamlit as st
import pandas as pd
import numpy as np

def processar_peso(uploaded_file):
    # Carregar os dados de pesagem
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    
    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Garantir que as colunas de peso a partir da 3ª coluna sejam numéricas (ignorando erros)
    #df_ct.iloc[:, 2:] = df_ct.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
    #df_dt.iloc[:, 2:] = df_dt.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')

    # Cálculo da média do peso e erro padrão para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()  # Médias para CT
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])  # Erro padrão para CT

    # Cálculo da média do peso e erro padrão para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()  # Médias para DT
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])  # Erro padrão para DT

    # Dicionário com os resultados do peso
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
    
    # Filtragem dos dados por classe de caixa
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']
    
    # Cálculo da média de consumo para cada dia
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

def carregar_e_processar_excel(uploaded_file):
    resultado_peso = processar_peso(uploaded_file)
    resultado_racao = processar_consumo_racao(uploaded_file)
    consumo_racao = consumo_bruto_racao(uploaded_file)
    resultado_completo = {**resultado_peso, **resultado_racao}
    return resultado_completo

# Interface Streamlit
st.title("Análise de Pesagem e Consumo de Ração")

uploaded_file = st.file_uploader("Carregar Arquivo Excel", type=["xlsx"])

if uploaded_file:
    # Processar os dados
    resultado_peso = processar_peso(uploaded_file)
    resultado_racao = processar_consumo_racao(uploaded_file)
    consumo_racao = consumo_bruto_racao(uploaded_file)

    # Exibir a função principal (resultado completo)
    with st.expander("Peso dos animais"):
        df_peso = pd.concat([resultado_peso["df_ct"], resultado_peso["df_dt"]])
        df_peso.set_index("ID do Animal", inplace=True)
        st.dataframe(df_peso)
    
    # Exibir DataFrame com as médias e erros padrão de peso (por classe)
    #st.subheader("Resultado - Peso dos Animais")
    #st.write("Médias e erro padrão do peso para animais CT:")
    #st.dataframe(resultado_peso["df_ct"])

    #st.write("Médias e erro padrão do peso para animais DT:")
    #st.dataframe(resultado_peso["df_dt"])

    # Exibir resumo das médias gerais usando DataFrame
    st.write("Médias Gerais de Consumo de Ração")
    df_medias_gerais = pd.DataFrame({
        "Grupo": ["CT", "DT"],
        "Média do consumo de ração": [
            resultado_racao["media_geral_racao_ct"],
            resultado_racao["media_geral_racao_dt"]
        ]
    })
    df_medias_gerais.set_index("Grupo", inplace=True)
    st.dataframe(df_medias_gerais)

    # Exibir dados brutos do consumo das caixas
    st.write("Consumo de ração por caixa")
    df_racao = pd.concat([consumo_racao["df_racao_ct"], consumo_racao["df_racao_dt"]])
    df_racao.set_index("Classe da Caixa", inplace=True)
    st.write(df_racao)
    
    #df_media_geral = pd.DataFrame({'Classe': ['CT', 'DT'], 'Média Geral': [media_geral_racao_ct, media_geral_racao_dt]})
    #df_media_geral.set_index("Classe da Caixa", implace=True)
    #st.dataframe(f"Média geral de ração para CT: {resultado_racao['media_geral_racao_ct']}")
