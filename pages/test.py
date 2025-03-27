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

    
    # Calcular a média do índice de discriminação por classe e adicionar ao DataFrame original
    df["Média dos índices de discriminação"] = df.groupby("Classe do animal")["Índice de discriminação"].transform("mean")

    st.write("Colunas disponíveis no DataFrame:", df.columns)

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
        resultados[sheet_name] = {"df": df, "medias_por_classe": medias_por_classe}

    # Exibir os resultados
    for sheet_name, result in resultados.items():
        df = result["df"]
        medias_por_classe = result["medias_por_classe"]
        
        # Exibir os dados de cada planilha
        with st.expander(f"### {sheet_name}"):
            df.set_index("Classe do animal", inplace=True)
            st.dataframe(df[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta", "Média dos índices de discriminação"]])

        # Exibir as médias por classe de animal
        with st.expander(f"Médias por Classe de Animal - {sheet_name}"):
            st.dataframe(medias_por_classe)

            # Exibir as médias de discriminação por classe
            for _, row in medias_por_classe.iterrows():
                st.write(f"Média do índice de discriminação para a classe {row['Classe do animal']}: {row['Índice de discriminação']:.2f}")

            # Exibir gráficos por classe de animal
            st.subheader(f"Gráfico de Índice de Discriminação para {sheet_name}")
            st.bar_chart(medias_por_classe.set_index('Classe do animal')['Índice de discriminação'])

        # Exibir os resultados
    for sheet_name, df in resultados.items():
        with st.expander(f"### {sheet_name}"):
            df.set_index("Classe do animal", inplace=True)
            #st.write(f"### {sheet_name}")           
            st.dataframe(df[["Tempo no objeto novo", "Tempo no objeto familiar", "Índice de discriminação", "Índice de preferência", "Discriminação absoluta", "ID"]])

    with st.expander("Médias do índice de discriminação"):
        # Para cada planilha, exibe a média do índice de discriminação
        for sheet_name, df in resultados.items():
            st.write(f"Média do índice de discriminação para {sheet_name}: {df['Média dos índices de discriminação'].iloc[0]:.2f}")
            
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
