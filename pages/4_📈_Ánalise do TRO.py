import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Análise do TRO",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={})
st.set_option('client.showErrorDetails', True)

def calcular_indices(df):
    # Calcula os índices de discriminação e de preferencia para cada animal.
    
    df["Discriminação absoluta"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]))
                                    
    df["Índice de discriminação"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) /
                                      (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]))
    
    df["Índice de preferência"] = ((df["Tempo no objeto novo"]) / (df["Tempo no objeto novo"] + df ["Tempo no objeto familiar"])) * 100

    df["Média dos índices de discriminação"] = df["Índice de discriminação"].mean()
    
    return df

# Configuração do Streamlit
st.title("Análise do teste comportamental")

st.markdown("---")

url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5614391/"

with st.expander("Como funciona?"):
    st.write("Converta a sua planilha com os resultados do TRO para o modelo ou gere uma nova no gerador de planilhas. Usando os tempos de exploração, serão calculados:")
    st.write("Índice de discriminação: d2 = tnovo - tfamiliar / tnovo + tfamiliar")
    st.write("Discriminação absoluta: d1 = tnovo - tfamiliar")
    st.write("Índice de preferência: d3 = tnovo / tnovo + tfamiliar * 100")
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
            df.set_index("Classe do animal", inplace=True)
            #st.write(f"### {sheet_name}")           
            st.dataframe(df[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta", "ID"]])

    with st.expander("Médias do índice de discriminação"):
        for sheet_name, df in resultados.items():
            df_medias = pd.DataFrame({
                "Grupo CT": resultados["Média dos índices de discriminação"]
            })
            st.dataframe(df["Média dos índices de discriminação"])

    # Criar um arquivo Excel com os resultados
    with pd.ExcelWriter("resultados_TRO.xlsx", engine="xlsxwriter") as writer:
        for sheet_name, df in resultados.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()
        
    with open("resultados_TRO.xlsx", "rb") as f:
        st.download_button("Baixar resultados", f, "resultados_TRO.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
