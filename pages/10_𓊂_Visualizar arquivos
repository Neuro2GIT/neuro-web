import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Métodos e técnicas",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={})
st.set_option('client.showErrorDetails', True)

# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
    return st.session_state["google_drive_service"]

def list_files(service, folder_name="neuroscience"):
    """Lista arquivos dentro da pasta especificada (por padrão, 'neuroscience') no Google Drive"""
    try:
        # Busca a pasta 'neuroscience' pelo nome
        query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'"
        results = service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
        folders = results.get('files', [])

        # Se a pasta não for encontrada, retornar um erro
        if not folders:
            st.error(f"Pasta '{folder_name}' não encontrada.")
            return []

        folder_id = folders[0]['id']
        st.write(f"Pasta '{folder_name}' encontrada! Listando arquivos...")

        # Lista os arquivos dentro da pasta 'neuroscience'
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, pageSize=100, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])

        # Criar um DataFrame com os dados dos arquivos
        if items:
            df = pd.DataFrame(items)
            return df
        else:
            st.warning("Nenhum arquivo encontrado na pasta 'neuroscience'.")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return pd.DataFrame()

# Função principal
def main():
    st.title("🐁 Listagem dos Arquivos no Google Drive - Pasta 'neuroscience'")
    
    # Autenticação do Google Drive
    service = authenticate_google_drive()

    # Buscar e exibir os arquivos na pasta 'neuroscience'
    df_files = list_files(service)

    # Exibir o DataFrame com os arquivos
    if not df_files.empty:
        st.write("Arquivos encontrados na pasta 'neuroscience':")
        st.dataframe(df_files)  # Exibe o DataFrame com os arquivos

    # Footer com customização
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
main()

