import pandas as pd
import streamlit as st

def calcular_indices(df):
    # Calcula os índices de discriminação e de preferencia para cada animal.
    df["Discriminação absoluta"] = df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]
    df["Índice de discriminação"] = (df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) / \
                                     (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])
    df["Índice de preferência"] = df["Tempo no objeto novo"] / \
                                  (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"])
    return df

# Camada de exibição para o Streamlit
st.title("Análise do teste comportamental")

with st.container():
    uploaded_file = st.file_uploader("Selecione um arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Ler o arquivo Excel
    try:
        xls = pd.ExcelFile(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
    else:
        # Criar um dicionário para armazenar os índices de discriminação
        resultados = {}

        # Iterar sobre as planilhas (Animais CT e Animais DT)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # Verifica se as colunas necessárias existem
            required_columns = ["ID do animal", "Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar"]
            if not all(col in df.columns for col in required_columns):
                st.warning(f"A planilha '{sheet_name}' não contém todas as colunas necessárias.")
                continue

            # Calcular os índices
            df = calcular_indices(df)
            resultados[sheet_name] = df

        # Exibir os resultados
        st.markdown("---")
        for sheet_name, df in resultados.items():
            with st.expander(f"### {sheet_name}"):
                st.dataframe(df[["ID do animal", "Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar", 
                                 "Índice de discriminação", "Índice de preferência", "Discriminação absoluta"]])

else:
    st.info("Por favor, faça o upload de um arquivo Excel para começar a análise.")
