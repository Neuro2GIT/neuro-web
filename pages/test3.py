import streamlit as st
import pandas as pd

def separar_grupo_subgrupo(df, classe, grupo):
    """
    Função para filtrar o DataFrame com base no grupo e subgrupo.
    
    :param df: DataFrame original
    :param grupo: Valor do grupo ('M' ou 'F')
    :param subgrupo: Valor do subgrupo ('CT' ou 'DT')
    :return: DataFrame filtrado
    """
    return df[(df['Classe do animal'] == classe) & (df['Grupo'] == grupo)]

def calcular_indices(df):
    # Separar dados por classe (M/F) e grupo (CT/DT)
    df_m_ct = separar_grupo_subgrupo(df, 'CT', 'M')  # Machos - Controle
    df_m_dt = separar_grupo_subgrupo(df, 'DT', 'M')  # Machos - Tratamento
    df_f_ct = separar_grupo_subgrupo(df, 'CT', 'F')  # Fêmeas - Controle
    df_f_dt = separar_grupo_subgrupo(df, 'DT', 'F')  # Fêmeas - Tratamento
    
    # Calcular discriminação absoluta para os subgrupos
    df_m_ct["Discriminação absoluta"] = df_m_ct["Tempo no objeto novo"] - df_m_ct["Tempo no objeto familiar"]
    df_m_dt["Discriminação absoluta"] = df_m_dt["Tempo no objeto novo"] - df_m_dt["Tempo no objeto familiar"]
    df_f_ct["Discriminação absoluta"] = df_f_ct["Tempo no objeto novo"] - df_f_ct["Tempo no objeto familiar"]
    df_f_dt["Discriminação absoluta"] = df_f_dt["Tempo no objeto novo"] - df_f_dt["Tempo no objeto familiar"]
    
    # Calcular Índice de Discriminação para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de discriminação"] = df_m_ct["Discriminação absoluta"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])
    df_m_dt["Índice de discriminação"] = df_m_dt["Discriminação absoluta"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])
    df_f_ct["Índice de discriminação"] = df_f_ct["Discriminação absoluta"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])
    df_f_dt["Índice de discriminação"] = df_f_dt["Discriminação absoluta"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])
    
    # Calcular Índice de Preferência para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de preferência"] = (df_m_ct["Tempo no objeto novo"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])) * 100
    df_m_dt["Índice de preferência"] = (df_m_dt["Tempo no objeto novo"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])) * 100
    df_f_ct["Índice de preferência"] = (df_f_ct["Tempo no objeto novo"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])) * 100
    df_f_dt["Índice de preferência"] = (df_f_dt["Tempo no objeto novo"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])) * 100

    # Calcular a média dos índices de discriminação por grupo
    medias_indices_m_ct = df_m_ct["Índice de discriminação"].mean()
    medias_indices_m_dt = df_m_dt["Índice de discriminação"].mean()
    medias_indices_f_ct = df_f_ct["Índice de discriminação"].mean()
    medias_indices_f_dt = df_f_dt["Índice de discriminação"].mean()

    medias_indices = {
        'Macho - Controle': medias_indices_m_ct,
        'Macho - Tratamento': medias_indices_m_dt,
        'Fêmea - Controle': medias_indices_f_ct,
        'Fêmea - Tratamento': medias_indices_f_dt
    }

    # Retornar os dataframes separados
    return df_m_ct, df_m_dt, df_f_ct, df_f_dt, medias_indices

# Streamlit: Interface do usuário
st.title("Cálculo de Índices de Discriminação e Preferência")

# Carregar um arquivo CSV ou Excel
uploaded_file = st.file_uploader("Carregar arquivo CSV ou Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Tentar ler o arquivo dependendo da extensão
    try:
        # Se for um arquivo CSV
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        
        # Se for um arquivo Excel
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # Verificar se as colunas necessárias existem
        if 'Classe do animal' in df.columns and 'Grupo' in df.columns and 'Tempo no objeto novo' in df.columns and 'Tempo no objeto familiar' in df.columns:
            
            # Calcular os índices
            df_m_ct, df_m_dt, df_f_ct, df_f_dt, medias_indices = calcular_indices(df)
            
            # Exibir as tabelas separadas para cada subgrupo
            st.subheader("Resultados - Machos - Controle (M-CT)")
            st.dataframe(df_m_ct)  # Exibe o DataFrame com os índices calculados para Machos - Controle
            
            st.subheader("Resultados - Machos - Tratamento (M-DT)")
            st.dataframe(df_m_dt)  # Exibe o DataFrame com os índices calculados para Machos - Tratamento
            
            st.subheader("Resultados - Fêmeas - Controle (F-CT)")
            st.dataframe(df_f_ct)  # Exibe o DataFrame com os índices calculados para Fêmeas - Controle
            
            st.subheader("Resultados - Fêmeas - Tratamento (F-DT)")
            st.dataframe(df_f_dt)  # Exibe o DataFrame com os índices calculados para Fêmeas - Tratamento
            
            # Exibir as médias dos índices de discriminação por grupo (Tabela separada)
            st.subheader("Média dos Índices de Discriminação por Grupo")
            st.write(medias_indices)  # Exibe a tabela com a média dos índices por grupo

        else:
            st.error("O arquivo não contém as colunas necessárias.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
    
    # Calcular discriminação absoluta para os subgrupos
    df_m_ct["Discriminação absoluta"] = df_m_ct["Tempo no objeto novo"] - df_m_ct["Tempo no objeto familiar"]
    df_m_dt["Discriminação absoluta"] = df_m_dt["Tempo no objeto novo"] - df_m_dt["Tempo no objeto familiar"]
    df_f_ct["Discriminação absoluta"] = df_f_ct["Tempo no objeto novo"] - df_f_ct["Tempo no objeto familiar"]
    df_f_dt["Discriminação absoluta"] = df_f_dt["Tempo no objeto novo"] - df_f_dt["Tempo no objeto familiar"]
    
    # Calcular Índice de Discriminação para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de discriminação"] = df_m_ct["Discriminação absoluta"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])
    df_m_dt["Índice de discriminação"] = df_m_dt["Discriminação absoluta"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])
    df_f_ct["Índice de discriminação"] = df_f_ct["Discriminação absoluta"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])
    df_f_dt["Índice de discriminação"] = df_f_dt["Discriminação absoluta"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])
    
    # Calcular Índice de Preferência para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de preferência"] = (df_m_ct["Tempo no objeto novo"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])) * 100
    df_m_dt["Índice de preferência"] = (df_m_dt["Tempo no objeto novo"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])) * 100
    df_f_ct["Índice de preferência"] = (df_f_ct["Tempo no objeto novo"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])) * 100
    df_f_dt["Índice de preferência"] = (df_f_dt["Tempo no objeto novo"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])) * 100

    # Unir os dataframes de 'M-CT', 'M-DT', 'F-CT' e 'F-DT' novamente
    df_completo = pd.concat([df_m_ct, df_m_dt, df_f_ct, df_f_dt])

    # Calcular a média dos índices de discriminação por grupo
    medias_indices = df_completo.groupby(['Classe do animal', 'Grupo'])['Índice de discriminação'].mean().reset_index()

    return df_completo, medias_indices

# Streamlit: Interface do usuário
st.title("Cálculo de Índices de Discriminação e Preferência")

# Carregar um arquivo CSV ou Excel
uploaded_file = st.file_uploader("Carregar arquivo CSV ou Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Tentar ler o arquivo dependendo da extensão
    try:
        # Se for um arquivo CSV
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        
        # Se for um arquivo Excel
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # Verificar se as colunas necessárias existem
        if 'Classe do animal' in df.columns and 'Grupo' in df.columns and 'Tempo no objeto novo' in df.columns and 'Tempo no objeto familiar' in df.columns:
            
            # Calcular os índices
            df_calculado, medias_indices = calcular_indices(df)
            
            # Exibir a tabela de resultados (dados do animal)
            st.subheader("Resultados por Animal")
            st.dataframe(df_calculado)  # Exibe o DataFrame com os índices calculados
            
            # Exibir as médias dos índices de discriminação por grupo (Tabela separada)
            st.subheader("Média dos Índices de Discriminação por Grupo")
            st.dataframe(medias_indices)  # Exibe a tabela com a média dos índices por grupo
            
            # Exibir algumas métricas (opcional)
            st.subheader("Média Geral dos Índices de Discriminação")
            st.write(f"Média geral dos Índices de Discriminação: {df_calculado['Índice de discriminação'].mean():.2f}")
            
            # Adicionar gráficos para visualização
            st.subheader("Gráfico de Índice de Preferência")
            st.line_chart(df_calculado[['Índice de preferência']])
            
            st.subheader("Gráfico de Discriminação Absoluta")
            st.line_chart(df_calculado[['Discriminação absoluta']])

        else:
            st.error("O arquivo não contém as colunas necessárias.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
