import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregando os dados da aba "Dados dos animais" do Excel
    dados_animais = pd.read_excel(uploaded_file, sheet_name="Dados dos animais")
    
    # Exibindo as primeiras linhas dos dados para garantir que o arquivo foi carregado corretamente
    st.write("Primeiras linhas dos dados carregados:")
    st.dataframe(dados_animais.head())  # Exibindo as primeiras linhas para revisão

    # Se necessário, podemos limpar ou processar os dados. Por exemplo:
    dados_animais = dados_animais.dropna()  # Remover linhas com valores ausentes
    
    # Verificando as colunas disponíveis no DataFrame
    st.write("Colunas dos dados carregados:")
    st.write(dados_animais.columns)

    return dados_animais

# Função para calcular as estatísticas para o boxplot
def calc_boxplot_stats(data):
    if len(data) == 0:  # Se não houver dados, retornamos um DataFrame vazio
        return pd.DataFrame({
            'Q1': [None], 'Q3': [None], 'Median': [None],
            'IQR': [None], 'Lower Whisker': [None],
            'Upper Whisker': [None], 'Outliers': [[]]
        })
    
    Q1 = data.quantile(0.25)  # Primeiro Quartil
    Q3 = data.quantile(0.75)  # Terceiro Quartil
    median = data.median()  # Mediana
    IQR = Q3 - Q1  # Intervalo Interquartil
    lower_whisker = Q1 - 1.5 * IQR  # Limite inferior dos bigodes
    upper_whisker = Q3 + 1.5 * IQR  # Limite superior dos bigodes
    outliers = data[(data < lower_whisker) | (data > upper_whisker)]  # Outliers
    
    # Verificando se existem outliers para garantir que o 'Outliers' não seja uma lista vazia
    outliers_list = outliers.tolist() if not outliers.empty else []
    
    # Criando o DataFrame com as estatísticas calculadas
    stats = {
        'Q1': Q1,
        'Q3': Q3,
        'Median': median,
        'IQR': IQR,
        'Lower Whisker': lower_whisker,
        'Upper Whisker': upper_whisker,
        'Outliers': outliers_list  # Convertendo os outliers para lista
    }
    
    return pd.DataFrame(stats, index=[0])  # Retorna um DataFrame com as estatísticas

# Função para gerar o boxplot
def gerar_boxplot(df):
    # Criando o boxplot com Seaborn
    plt.figure(figsize=(10,6))
    
    # Boxplot para os tempos de exploração nos objetos novo e familiar, separados por grupo (Controle vs DT)
    sns.boxplot(x="Classe do Animal", y="Tempo no Objeto Novo (segundos)", data=df)
    
    # Título e labels
    plt.title("Boxplot - Tempo de Exploração no Objeto Novo")
    plt.xlabel("Classe do Animal")
    plt.ylabel("Tempo no Objeto Novo (segundos)")

    # Exibindo o gráfico no Streamlit
    st.pyplot(plt)

    # Repetir para o objeto Familiar
    plt.figure(figsize=(10,6))
    sns.boxplot(x="Classe do Animal", y="Tempo no Objeto Familiar (segundos)", data=df)
    
    # Título e labels
    plt.title("Boxplot - Tempo de Exploração no Objeto Familiar")
    plt.xlabel("Classe do Animal")
    plt.ylabel("Tempo no Objeto Familiar (segundos)")

    # Exibindo o gráfico no Streamlit
    st.pyplot(plt)

# Função principal do Streamlit
def main():
    # Título da aplicação
    st.title("Carregar e Processar Dados do Excel")

    # Caixa para o upload do arquivo Excel
    uploaded_file = st.file_uploader("Carregue o arquivo Excel", type=["xlsx"])

    # Se o arquivo foi carregado
    if uploaded_file is not None:
        # Chamando a função para carregar e processar os dados
        dados = carregar_e_processar_excel(uploaded_file)

        # Criando o DataFrame
        df = pd.DataFrame(dados)

        # Filtrando os dados por grupo e objeto
        controle_novo = df[df['Classe do Animal'] == 'Controle']['Tempo no Objeto Novo (segundos)']
        dt_novo = df[df['Classe do Animal'] == 'DT']['Tempo no Objeto Novo (segundos)']

        controle_familiar = df[df['Classe do Animal'] == 'Controle']['Tempo no Objeto Familiar (segundos)']
        dt_familiar = df[df['Classe do Animal'] == 'DT']['Tempo no Objeto Familiar (segundos)']

        # Calculando as estatísticas para cada grupo e objeto
        controle_novo_stats = calc_boxplot_stats(controle_novo)
        dt_novo_stats = calc_boxplot_stats(dt_novo)

        controle_familiar_stats = calc_boxplot_stats(controle_familiar)
        dt_familiar_stats = calc_boxplot_stats(dt_familiar)

        # Organizando os resultados em um dicionário
        resultados = {
            "controle_novo_stats": controle_novo_stats,
            "dt_novo_stats": dt_novo_stats,
            "controle_familiar_stats": controle_familiar_stats,
            "dt_familiar_stats": dt_familiar_stats,
            "df": df  # DataFrame original
        }

        # Exibindo as estatísticas calculadas em DataFrames no Streamlit
        st.subheader("Estatísticas para o Grupo Controle e DT - Objeto Novo")
        st.write("Controle - Objeto Novo:")
        st.dataframe(controle_novo_stats)  # Exibe o DataFrame com as estatísticas
        st.write("DT - Objeto Novo:")
        st.dataframe(dt_novo_stats)  # Exibe o DataFrame com as estatísticas

        st.subheader("Estatísticas para o Grupo Controle e DT - Objeto Familiar")
        st.write("Controle - Objeto Familiar:")
        st.dataframe(controle_familiar_stats)  # Exibe o DataFrame com as estatísticas
        st.write("DT - Objeto Familiar:")
        st.dataframe(dt_familiar_stats)  # Exibe o DataFrame com as estatísticas

        # Gerando os Boxplots para os tempos de exploração nos objetos
        gerar_boxplot(df)

if __name__ == "__main__":
    main()
