import streamlit as st
import pandas as pd

# Função para calcular as métricas para cada grupo de classe
def calcular_metricas(grupo):
    # Calcular as métricas
    discriminacao_absoluta = grupo['Tempo no objeto novo'] - grupo['Tempo no objeto familiar']
    indice_discriminacao = (grupo['Tempo no objeto novo'] - grupo['Tempo no objeto familiar']) / (grupo['Tempo no objeto novo'] + grupo['Tempo no objeto familiar'])
    indice_preferencia = (grupo['Tempo no objeto novo'] / (grupo['Tempo no objeto novo'] + grupo['Tempo no objeto familiar'])) * 100
    
    # Retornar os resultados como um dicionário
    return {
        "Discriminação absoluta": discriminacao_absoluta.mean(),  # Média para representar o valor do grupo
        "Índice de discriminação": indice_discriminacao.mean(),
        "Índice de preferência": indice_preferencia.mean()
    }

# Função principal para o Streamlit
def main():
    # Título da aplicação
    st.title('Cálculos de Discriminação e Preferência por Classe')

    # Carregar arquivo (Excel ou CSV)
    uploaded_file = st.file_uploader("Escolha uma planilha", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Verificar o tipo de arquivo e carregar
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        # Exibir as primeiras linhas dos dados
        st.write("Primeiras linhas dos dados:", df.head())

        # Agrupar por classe e aplicar a função de cálculo
        resultados_por_classe = df.groupby('classe').apply(calcular_metricas).to_dict()

        # Exibir os resultados na interface Streamlit
        st.write("### Resultados por Classe", resultados_por_classe)
            
if __name__ == "__main__":
    main()
