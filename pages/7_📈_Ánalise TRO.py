import pandas as pd
import streamlit as st


def calcular_indices(df):
    # Calcula os índices de discriminação e de preferencia para cada animal.
    
    df["Discriminação absoluta"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]))
                                    
    df["Índice de discriminação"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) /
                                      (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]))
    df["Índice de preferência"] = ((df["Tempo no objeto novo"]) /
                                   (df["Tempo no objeto novo"] + df ["Tempo no objeto familiar"]))
                                   
    return df

# Configuração do Streamlit
st.title("Análise do teste comportamental")

st.markdown("---")

url = "https://doi.org/10.3791/55718"

with st.expander("Como usar?"):
    st.write("Converta a sua planilha com os resultados do TRO para o modelo ou gere uma nova no gerador de planilhas.")
    st.write("Usando os tempos de exploração, serão calculados: discriminação absoluta, índice de discriminação e índice de preferência/reconhecimento.")
    st.markdown(f"[Leia o artigo base]({url})")

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
        df = calcular_indices(df)
        resultados[sheet_name] = df

    st.markdown("---")
    
    # Exibir os resultados
    for sheet_name, df in resultados.items():
        with st.expander(f"### {sheet_name}"):
            #st.write(f"### {sheet_name}")           
            st.dataframe(df[["ID do animal", "Classe do animal", "Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta"]])
            df.set_index("ID do animal", inplace=True)
            

    # Criar um arquivo Excel com os resultados
    with pd.ExcelWriter("resultados_TRO.xlsx", engine="xlsxwriter") as writer:
        for sheet_name, df in resultados.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()
        
    with open("resultados_TRO.xlsx", "rb") as f:
        st.download_button("Baixar resultados", f, "resultados_TRO.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
