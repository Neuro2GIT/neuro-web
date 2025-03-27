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
    
    df["Discriminação absoluta"] = df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]
    df["Índice de discriminação"] = (df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) / \
                                    (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])
    df["Índice de preferência"] = (df["Tempo no objeto novo"]) / (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]) * 100

    return df

# Função para calcular as médias por classe
def calcular_medias(df):
    
    return df.groupby("Classe do animal")[["Índice de discriminação", "Índice de preferência"]].mean().reset_index()
    
# Configuração do Streamlit
st.title("Análise do teste comportamental")

with st.container(border=True):
    uploaded_file = st.file_uploader("Selecione um arquivo excel (.xlsx)", type=["xlsx"])
    
if uploaded_file is not None:
    # Ler o arquivo
    df = pd.read_excel(uploaded_file, sheet_name=None)
    for name, df in dados_excel.items():

   
        # Verifica se as colunas necessárias existem no arquivo
    
        #colunas_necessarias = {"Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar"}
    
        df = calcular_indices(df)
        medias_por_classe = calcular_medias(df)

        # Armazenando os resultados organizados
        resultados = {
            "dados_com_indices": df,
            "medias_por_classe": medias_por_classe
        }

        # Exibir tabelas no Streamlit
        st.subheader("Dados com Índices Calculados")
        df.set_index("Classe do animal", inplace=True)
        st.dataframe(resultados["dados_com_indices"])

        st.subheader("Médias dos Índices por Classe")
        st.dataframe(resultados["medias_por_classe"])
