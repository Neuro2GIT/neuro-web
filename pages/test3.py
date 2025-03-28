import streamlit as st
import pandas as pd

def separar_grupo_subgrupo(df, classe, grupo):

    return df[(df['Classe do animal'] == classe) & (df['Grupo'] == grupo)]

def calcular_indices(df):
    # Separar dados por classe (M/F) e grupo (CT/DT)
    df_m_ct = separar_grupo_subgrupo(df, 'CT', 'M')  # Machos - Controle
    df_m_dt = separar_grupo_subgrupo(df, 'DT', 'M')  # Machos - Tratamento
    df_f_ct = separar_grupo_subgrupo(df, 'CT', 'F')  # Fêmeas - Controle
    df_f_dt = separar_grupo_subgrupo(df, 'DT', 'F')  # Fêmeas - Tratamento
    
    # Calcular Índice de Discriminação para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de discriminação"] = df_m_ct["Tempo no objeto novo"] - df_m_ct["Tempo no objeto familiar"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])
    df_m_dt["Índice de discriminação"] = df_m_dt["Tempo no objeto novo"] - df_m_ct["Tempo no objeto familiar"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])
    df_f_ct["Índice de discriminação"] = df_f_ct["Tempo no objeto novo"] - df_f_ct["Tempo no objeto familiar"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])
    df_f_dt["Índice de discriminação"] = df_f_dt["Tempo no objeto novo"] - df_f_dt["Tempo no objeto familiar"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])

    # Concatenar os DataFrames (M-CT, M-DT, F-CT, F-DT)
    df_controle = pd.concat([df_m_ct, df_f_ct], ignore_index=True)  # Concatenando Machos e Fêmeas - Controle
    df_deficiencia = pd.concat([df_m_dt, df_f_dt], ignore_index=True)  # Concatenando Machos e Fêmeas - Deficiência
    
    # Retornar os DataFrames concatenados
    return df_controle, df_deficiencia

st.write(df.columns)

# Streamlit: Interface do usuário
st.title("Cálculo de Índices de Discriminação e Preferência")

# Carregar um arquivo Excel
uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Ler o arquivo Excel
    df = pd.read_excel(uploaded_file)

    # Calcular os índices
    df_controle, df_deficiencia = calcular_indices(df)
    
    # Exibir o DataFrame concatenado de Controle (M-CT e F-CT)
    st.subheader("Resultados de Machos e Fêmeas - Controle (M-CT e F-CT)")
    st.dataframe(df_controle)

    # Exibir o DataFrame concatenado de Deficiência (M-DT e F-DT)
    st.subheader("Resultados de Machos e Fêmeas - Deficiência (M-DT e F-DT)")
    st.dataframe(df_deficiencia)
