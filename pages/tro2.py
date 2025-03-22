import pandas as pd
import streamlit as st

# Classe simples para armazenar os resultados de cada planilha
class ResultadoAnimal:
    def __init__(self, df, nome_planilha):
        self.df = df
        self.nome_planilha = nome_planilha

# Função para calcular os índices
def calcular_indices(df):
    # Calcula os índices de discriminação e de preferência para cada animal.
    df["Discriminação absoluta"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]))
    df["Índice de discriminação"] = ((df["Tempo no objeto novo"] - df["Tempo no objeto familiar"]) /
                                      (df["Tempo no objeto novo"] + df["Tempo no objeto familiar"]))
    df["Índice de preferência"] = ((df["Tempo no objeto novo"]) / (df["Tempo no objeto novo"] + df ["Tempo no objeto familiar"])) * 100
    return df

# Configuração do Streamlit
st.title("Análise do teste comportamental")

st.markdown("---")

url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5614391/"

with st.expander("Como usar?"):
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

    # Lista para armazenar os objetos de resultados
    resultados = []

    # Iterar sobre as planilhas (Animais CT e Animais DT)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = calcular_indices(df)
        # Criar o objeto ResultadoAnimal e adicionar à lista de resultados
        resultado = ResultadoAnimal(df, sheet_name)
        resultados.append(resultado)

    st.markdown("---")
    
    # Exibir os resultados de forma simples
    for resultado in resultados:
        st.write(f"### {resultado.nome_planilha}")
        st.dataframe(resultado.df[["ID", "Classe do animal", "Tempo no objeto novo", 
                                    "Tempo no objeto familiar", "Índice de discriminação", 
                                    "Índice de preferência", "Discriminação absoluta"]])

    # Criar um arquivo Excel com os resultados
    with pd.ExcelWriter("resultados_TRO.xlsx", engine="xlsxwriter") as writer:
        for resultado in resultados:
            resultado.df.to_excel(writer, sheet_name=resultado.nome_planilha, index=False)

    with open("resultados_TRO.xlsx", "rb") as f:
        st.download_button("Baixar resultados", f, "resultados_TRO.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def grafico_radar(df, animal_id):
    # Selecionar os índices para o animal com ID específico
    animal_data = df[df["ID"] == animal_id][["Índice de discriminação", 
                                               "Discriminação absoluta", 
                                               "Índice de preferência"]].values.flatten()

    # Definir os labels e os valores do gráfico
    categories = ["Índice de discriminação", "Discriminação absoluta", "Índice de preferência"]
    
    # Ajustar o gráfico de radar
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    animal_data = np.concatenate((animal_data, [animal_data[0]]))  # Fechar o gráfico
    angles += angles[:1]  # Fechar o gráfico no final
    
    fig, ax = plt.subplots(figsize=(6, 6), dpi=80, subplot_kw=dict(polar=True))
    ax.fill(angles, animal_data, color='blue', alpha=0.25)
    ax.plot(angles, animal_data, color='blue', linewidth=2)
    
    ax.set_yticklabels([])  # Remove as labels no eixo radial
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    ax.set_title(f"Perfil de {animal_id} nos Índices Comportamentais")
    
    st.pyplot(fig)

# Dentro do loop de visualização de resultados:
for sheet_name, df in resultados.items():
    with st.expander(f"### {sheet_name}"):
        st.dataframe(df[["ID", "Classe do animal", "Tempo no objeto novo", 
                         "Tempo no objeto familiar", "Índice de discriminação", 
                         "Índice de preferência", "Discriminação absoluta"]])
        
        # Exemplo: Adicionar gráfico de radar para o animal com ID específico (por exemplo, 'A01')
        grafico_radar(df, 'A01')
