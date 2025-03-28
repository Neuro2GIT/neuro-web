import streamlit as st
import pandas as pd

# Função para calcular as métricas para cada classe separada
def calcular_metricas_por_classe(df_classe, classe_nome):
    # Calcular as métricas
    discriminacao_absoluta = df_classe['Tempo no objeto novo'] - df_classe['Tempo no objeto familiar']
    indice_discriminacao = (df_classe['Tempo no objeto novo'] - df_classe['Tempo no objeto familiar']) / (df_classe['Tempo no objeto novo'] + df_classe['Tempo no objeto familiar'])
    indice_preferencia = (df_classe['Tempo no objeto novo'] / (df_classe['Tempo no objeto novo'] + df_classe['Tempo no objeto familiar'])) * 100
    
    # Retornar os resultados como um dicionário dinâmico baseado na classe
    resultados = {
        f"discriminacao_absoluta_{classe_nome}": discriminacao_absoluta.mean(),
        f"indice_discriminacao_{classe_nome}": indice_discriminacao.mean(),
        f"indice_preferencia_{classe_nome}": indice_preferencia.mean()
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

        # Verificar as colunas e garantir que o nome da coluna 'Classe do Animal' está correto
        st.write("Colunas do DataFrame:", df.columns)

        # Remover espaços extras e garantir que os nomes das colunas estejam em minúsculas
        df.columns = df.columns.str.strip().str.lower()

        # Verificar se a coluna 'classe' existe após a limpeza
        if 'classe do animal' in df.columns:
            # Filtrar os dados por classe
            df_ct_m = df[df['classe do animal'] == 'CT-M']
            df_dt_m = df[df['classe do animal'] == 'DT-M']
            df_ct_f = df[df['classe do animal'] == 'CT-F']
            df_dt_f = df[df['classe do animal'] == 'DT-F']

            # Calcular as métricas para cada classe
            resultados = {}
            resultados.update(calcular_metricas_por_classe(df_ct_m, 'ct-m'))
            resultados.update(calcular_metricas_por_classe(df_dt_m, 'dt-m'))
            resultados.update(calcular_metricas_por_classe(df_ct_f, 'ct-f'))
            resultados.update(calcular_metricas_por_classe(df_dt_f, 'dt-f'))

            # Exibir os resultados no Streamlit
            st.write("### Resultados Personalizados por Classe", resultados)
        else:
            st.error("Coluna 'classe do animal' não encontrada no DataFrame.")
            
if __name__ == "__main__":
    main()
