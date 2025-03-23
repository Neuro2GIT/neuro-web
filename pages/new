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


import pandas as pd
import numpy as np
import streamlit as st

# Função para análise do peso
def analise_do_peso(df):
    colunas_essenciais = {'ID do Animal', 'Classe do Animal'}
    if not colunas_essenciais.issubset(df.columns):
        raise ValueError("Colunas essenciais não encontradas no arquivo Excel")
    
    colunas_peso = [col for col in df.columns if "Peso no Dia" in col]
    
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']
    
    medias_peso_ct = df_ct[colunas_peso].mean()
    erro_padrao_peso_ct = df_ct[colunas_peso].std() / np.sqrt(df_ct.shape[0]) if df_ct.shape[0] > 0 else 0
    
    medias_peso_dt = df_dt[colunas_peso].mean()
    erro_padrao_peso_dt = df_dt[colunas_peso].std() / np.sqrt(df_dt.shape[0]) if df_dt.shape[0] > 0 else 0
    
    df_resultado_peso = pd.DataFrame({
        "Dia": colunas_peso,
        "Média Peso CT": medias_peso_ct.values,
        "Erro Padrão CT": erro_padrao_peso_ct.values,
        "Média Peso DT": medias_peso_dt.values,
        "Erro Padrão DT": erro_padrao_peso_dt.values
    })
    
    return {"df_resultado_peso": df_resultado_peso, "df_ct": df_ct, "df_dt": df_dt}

# Função para análise do consumo de ração
def analise_do_consumo(df_racao):
    colunas_essenciais = {'ID da Caixa', 'Classe da Caixa'}
    if not colunas_essenciais.issubset(df_racao.columns):
        raise ValueError("Colunas essenciais não encontradas no arquivo Excel")
    
    colunas_consumo = [col for col in df_racao.columns if "Consumo no Dia" in col]
    
    df_racao_ct = df_racao[df_racao['Classe da Caixa'] == 'CT']
    df_racao_dt = df_racao[df_racao['Classe da Caixa'] == 'DT']
    
    medias_racao_ct = df_racao_ct[colunas_consumo].mean()
    medias_racao_dt = df_racao_dt[colunas_consumo].mean()
    
    df_resultado_racao = pd.DataFrame({
        "Dia": colunas_consumo,
        "Média Consumo CT": medias_racao_ct.values,
        "Média Consumo DT": medias_racao_dt.values
    })
    
    return {"df_resultado_racao": df_resultado_racao, "df_racao_ct": df_racao_ct, "df_racao_dt": df_racao_dt}

# Função para carregar e processar o arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")
    
    resultado_peso = analise_do_peso(df)
    resultado_racao = analise_do_consumo(df_racao)
    
    return {**resultado_peso, **resultado_racao}

# Interface Streamlit
with st.container(border=True):
    uploaded_file = st.file_uploader("Para utilizar, converta a sua planilha para o modelo ou gere uma nova no gerador de planilhas", type=["xlsx"])

    if uploaded_file is not None:
        # Processar o arquivo
        resultados = carregar_e_processar_excel(uploaded_file)
        
        # Extração do df_resultado_peso do dicionário de resultados
        df_resultado_peso = resultados["df_resultado_peso"]
        
        # Exibir o DataFrame com os resultados de peso
        st.dataframe(df_resultado_peso)

