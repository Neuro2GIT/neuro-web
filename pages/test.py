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
    df_dt_m = df[df['Classe do animal'] == 'DT-F']
    
    df["Discriminação absoluta"] = df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]
    df["Índice de discriminação"] = (df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) / \
                                    (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])
    df["Índice de preferência"] = (df["Tempo no objeto novo"]) / (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]) * 100

    # Calcular as médias de cada índice
    media_discriminacao_absoluta = df["Discriminação absoluta"].mean()
    media_indice_discriminacao = df["Índice de discriminação"].mean()
    media_indice_preferencia = df["Índice de preferência"].mean()

    medias = {
        "Média da Discriminação Absoluta": media_discriminacao_absoluta,
        "Média do Índice de Discriminação": media_indice_discriminacao,
        "Média do Índice de Preferência": media_indice_preferencia
    }

    # Calcular as médias por classe de animal
    medias_por_classe = df.groupby("Classe do animal")[["Discriminação absoluta", "Índice de discriminação", "Índice de preferência"]].mean().reset_index()

    return df, medias, medias_por_classe

# Configuração do Streamlit
st.title("Análise do teste comportamental")

with st.container(border=True):
    uploaded_file = st.file_uploader("Selecione um arquivo excel (.xlsx)", type=["xlsx"])
    
if uploaded_file is not None:
    # Ler o arquivo Excel
    dados = pd.ExcelFile(uploaded_file)
    
    # Criar um dicionário para armazenar os índices
    resultados = {}
    
    # Iterar sobre as planilhas (Animais CT e Animais DT)
    for sheet_name in dados.sheet_names:
        df = pd.read_excel(dados, sheet_name=sheet_name)
        df, medias = calcular_indices(df)
        resultados[sheet_name] = df

    # Exibir os resultados
    for sheet_name, df in resultados.items():
        with st.expander(f"### {sheet_name}"):
            df.set_index("Classe do animal", inplace=True)
            #st.write(f"### {sheet_name}")           
            st.dataframe(df[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta", "ID"]])


    with st.expander("Médias do índice de discriminação"):
        # Para cada planilha, exibe a média do índice de discriminação
        for sheet_name, df in resultados.items():
            st.write(f"Média do índice de discriminação para {sheet_name}: {medias}")
