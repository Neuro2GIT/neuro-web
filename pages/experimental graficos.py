import pandas as pd
import streamlit as st

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue a planilha Excel", type=["xlsx"])

def calcular_indice_discriminacao(df):
    """Calcula o índice de discriminação para cada animal."""
    df["Índice de Discriminação"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) /
                                      (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])) * 100
    return df

# Configuração do Streamlit
st.title("Cálculo do Índice de Discriminação")

if uploaded_file is not None:
    # Ler o arquivo Excel
    xls = pd.ExcelFile(uploaded_file)
    
    # Criar um dicionário para armazenar os índices de discriminação
    resultados = {}
    
    # Iterar sobre as planilhas (Animais CT e Animais DT)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = calcular_indice_discriminacao(df)
        resultados[sheet_name] = df
    
    # Exibir os resultados
    st.subheader("Resultados do Índice de Discriminação")
    for sheet_name, df in resultados.items():
        st.write(f"### {sheet_name}")
        st.dataframe(df[["ID do animal", "Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar","Índice de Discriminação"]])
