import streamlit as st
import pandas as pd

# Função para calcular as métricas para cada grupo de classe
def calcular_metricas(grupo):
    # Calcular as métricas
    discriminacao_absoluta = grupo['Tempo no objeto novo'] - grupo['Tempo no objeto familiar']
    indice_discriminacao = (grupo['Tempo no objeto novo'] - grupo['Tempo no objeto familiar']) / (grupo['Tempo no objeto novo'] + grupo['Tempo no objeto familiar'])
    indice_preferencia = (grupo['Tempo no objeto novo'] / (grupo['Tempo no objeto novo'] + grupo['Tempo no objeto familiar'])) * 100
    
    # Retornar os resultados como um dicionário dinâmico baseado na classe
    resultados = {
        f"discriminacao_absoluta_{grupo['classe'].iloc[0].lower()}": discriminacao_absoluta.mean(),
        f"indice_discriminacao_{grupo['classe'].iloc[0].lower()}": indice_discriminacao.mean(),
        f"indice_preferencia_{grupo['classe'].iloc[0].lower()}": indice_preferencia.mean()
    }
    
    return resultados

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
        resultados_por_classe = df.groupby('Classe do animal').apply(calcular_metricas)

        # Transformar os resultados em um DataFrame
        resultados_df = pd.DataFrame(resultados_por_classe.tolist(), index=resultados_por_classe.index)

        # Exibir o DataFrame no Streamlit
        st.write("### Resultados Personalizados por Classe", resultados_df)
            
if __name__ == "__main__":
    main()
