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

    # Calcular as médias por classe de animal
    medias_por_classe = df.groupby("Classe do animal")[["Discriminação absoluta", "Índice de discriminação", "Índice de preferência"]].mean().reset_index()

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
    
    # Iterar sobre as planilhas (Animais CT e Animais DT)
    for sheet_name in dados.sheet_names:
        df = pd.read_excel(dados, sheet_name=sheet_name)
        df, medias_por_classe = calcular_indices(df)
        resultados[sheet_name] = df

    # Gerar lista de classes únicas no DataFrame
        classes_disponiveis = df['Classe do animal'].unique().tolist()

        # Permitir que o usuário selecione as classes a exibir (usando multiselect ou selectbox)
        classes_para_exibir = st.multiselect("Escolha as classes para exibir:", classes_disponiveis)

        # Se o usuário escolheu classes, filtrar o DataFrame
        if classes_para_exibir:
            df_filtrado = df[df['Classe do animal'].isin(classes_para_exibir)]
        else:
            # Caso não tenha sido selecionada nenhuma classe, mostrar todas
            df_filtrado = df

        # Definindo o índice
        df_filtrado.set_index("Classe do animal", inplace=True)

        # Exibindo os dados filtrados
        st.dataframe(df_filtrado[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", 
                                 "Índice de preferência", "Discriminação absoluta", "ID"]])
    # Exibir os resultados
    #for sheet_name, df in resultados.items():
        #with st.expander(f"### {sheet_name}"):
            #df.set_index("Classe do animal", inplace=True)
            #st.write(f"### {sheet_name}")           
            #st.dataframe(df[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta", "ID"]])


    with st.expander("Médias do índice de discriminação"):
        # Para cada planilha, exibe a média do índice de discriminação
        for sheet_name, df in resultados.items():
            st.write(f"Média do índice de discriminação para {sheet_name}: {medias_por_classe}")
