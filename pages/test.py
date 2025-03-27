import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Análise do TRO",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={})
st.set_option('client.showErrorDetails', True)

# Função para calcular os índices para cada grupo
def calcular_indices(df):

    # Separar dados comportamentais por classe
    df_ct_m = df[df['Classe do animal'] == 'CT-M']
    df_dt_m = df[df['Classe do animal'] == 'DT-M']
    df_ct_f = df[df['Classe do animal'] == 'CT-F']
    df_dt_f= df[df['Classe do animal'] == 'DT-F']
    
    df["Discriminação absoluta"] = df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]
    df["Índice de discriminação"] = (df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) / \
                                    (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])
    df["Índice de preferência"] = (df["Tempo no objeto novo"]) / (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]) * 100

    
    # Calcular a média do índice de discriminação por classe e adicionar ao dataframe inicial
    #df["Média dos índices de discriminação"] = df.groupby("Classe do animal")["Índice de discriminação"].transform("mean")

    medias_por_classe = df.groupby("Classe do animal")[["Índice de discriminação", "Índice de preferência"]].mean().reset_index()

    #st.write("Colunas disponíveis no DataFrame:", df.columns)

    return df, medias_por_classe
    
# Configuração do Streamlit
st.title("Análise do teste comportamental")

with st.container(border=True):
    uploaded_file = st.file_uploader("Selecione um arquivo excel (.xlsx)", type=["xlsx"])
    
if uploaded_file is not None:
    # Ler o arquivo Excel
    dados = pd.ExcelFile(uploaded_file)
    
    # Criar um dicionário para armazenar os índices
    resultados = {}

    # Exibir dados de cada planilha
    for sheet in sheet_names:
        st.write(f"Exibindo dados da planilha: {sheet}")
        df = dados[sheet]

    
