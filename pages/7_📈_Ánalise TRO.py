import pandas as pd
import streamlit as st


def calcular_indice_discriminacao(df):
    """Calcula o índice de discriminação para cada animal."""
    df["Índice de discriminação"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) /
                                      (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]))
    df["Índice de preferência"] = ((df["Tempo no objeto novo"]) /
                                   (df["Tempo no objeto novo"] + df ["Tempo no objeto familiar"]))
                                   
    return df

# Configuração do Streamlit
st.title("Análise do teste comportamental")

with st.expander("Como usar?"):
    st.write("Converta a sua planilha com os resultados do TRO para o modelo ou gere uma nova no gerador de planilhas.")

with st.container(border=True):
    uploaded_file = st.file_uploader("Selecione um arquivo excel (.xlsx)", type=["xlsx"])

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
    with st.container(border=True):
        for sheet_name, df in resultados.items():
            with st.expander():
                st.write(f"### {sheet_name}")
                st.dataframe(df[["ID do animal", "Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência"]])
