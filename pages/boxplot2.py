import pandas as pd
import streamlit as st

# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    # Carregando os dados da aba "Dados dos animais" do Excel
    dados_animais = pd.read_excel(uploaded_file, sheet_name="Dados dos animais")
    
    # Exibindo as primeiras linhas dos dados para garantir que o arquivo foi carregado corretamente
    #st.write("Primeiras linhas dos dados carregados:")
    #st.dataframe(dados_animais.head())  # Exibindo as primeiras linhas para revisão

    # Se necessário, podemos limpar ou processar os dados. Por exemplo:
    #dados_animais = dados_animais.dropna()  # Remover linhas com valores ausentes

    # Exibindo o DataFrame completo após o processamento
    #st.write("DataFrame completo após processamento:")
    #st.dataframe(dados_animais)  # Exibindo o DataFrame completo

    # Verificando as colunas disponíveis no DataFrame
    #st.write("Colunas dos dados carregados:")
    #st.write(dados_animais.columns)

    return dados_animais

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

        # Criando o DataFrame (não é necessário, já que 'dados' já é um DataFrame)
        df = pd.DataFrame(dados)  # Não precisa, pois 'dados' já é um DataFrame

        # Exibindo o DataFrame completo
        st.write("Exibindo o DataFrame processado:")
        st.dataframe(dados)  # Exibindo o DataFrame completo após o processamento

# Chama a função principal
if __name__ == "__main__":
    main()
