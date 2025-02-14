import hmac
import streamlit as st
import pickle
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from st_aggrid import AgGrid, GridOptionsBuilder
from io import StringIO

st.set_page_config(
    page_title="Grupo neuroscience",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
    }
)

st.set_option('client.showErrorDetails', True)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Escopos necessários para acessar o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Autenticação com o Google Drive usando as credenciais do Streamlit secrets"""
    
    # A autenticação deve ser feita explicitamente apenas na página inicial
    if "google_drive_service" not in st.session_state:
        #st.write("Autenticando.")
        
        google_secrets = st.secrets["google"]
        credentials_dict = {
            "type": "service_account",
            "project_id": google_secrets["project_id"],
            "private_key_id": google_secrets["private_key_id"],
            "private_key": google_secrets["private_key"],
            "client_email": google_secrets["client_email"],
            "client_id": google_secrets["client_id"],
            "auth_uri": google_secrets["auth_uri"],
            "token_uri": google_secrets["token_uri"],
            "auth_provider_x509_cert_url": google_secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": google_secrets["client_x509_cert_url"],
            "universe_domain": google_secrets["universe_domain"]
        }
        
        credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        
        # Testa a autenticação (opcional, dependendo do que você deseja verificar)
        test_authentication(service)
        
        # Salva o serviço autenticado no session_state para uso em outras páginas
        st.session_state["google_drive_service"] = service
        #st.write("Autenticação concluída com sucesso.")
    
    #else:
        st.write("Bem vindo.")

    return st.session_state["google_drive_service"]

def test_authentication(service):
    """Função de teste de autenticação (exemplo, pode ser ajustado conforme necessidade)"""
    try:
        # Teste básico para verificar a autenticação
        about = service.about().get(fields="user").execute()
        st.write(f"Autenticado como: {about['user']['emailAddress']}")
    except Exception as e:
        st.error(f"Falha na autenticação: {e}")

def test_authentication(service):
    """Teste simples para verificar se a autenticação foi bem-sucedida"""
    try:
        # Tente listar arquivos como forma de validar a autenticação
        results = service.files().list(pageSize=1).execute()
        if 'files' in results and len(results['files']) > 0:
            st.success("Autenticação bem-sucedida!")
        else:
            st.error("Nenhum arquivo encontrado, mas autenticação bem-sucedida.")
    except Exception as e:
        st.error(f"Erro de autenticação: {e}")

def list_files(service, folder_id=None):
    """Lista arquivos e pastas. Se `folder_id` for passado, lista o conteúdo dessa pasta."""
    query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
    results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    return items

def main():
    st.title("🐁Grupo neuroscience")

    # Adding sidebar
    with st.sidebar:
        st.header("Índice")
        #with st.sidebar:
        st.header("Índice")
        
        # Autenticação para o Google Drive
        service = authenticate_google_drive()

        # Seletor para exibir arquivos compartilhados ou não
        show_shared = st.sidebar.checkbox("Exibir arquivos compartilhados", value=False)

        # Listar arquivos e pastas a partir da raiz ou compartilhados
        items = list_files(service, shared=show_shared)

        # Separar pastas e arquivos
        folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

        # Mostrar pastas na sidebar (Se houver pastas)
        if folders:
            selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", [folder['name'] for folder in folders])
            selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)

            # Se uma pasta for selecionada, listar arquivos dentro dela
            if selected_folder:
                selected_folder_id = selected_folder['id']
                folder_files = list_files(service, folder_id=selected_folder_id, shared=show_shared)
                selected_file_name = st.sidebar.selectbox("Escolha um arquivo dentro da pasta", [file['name'] for file in folder_files])
            else:
                selected_file_name = None
        else:
            selected_folder = None
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo na raiz", [file['name'] for file in files])

        # Fetch the selected file
        if selected_file_name:
            if selected_folder:
                selected_file = next(file for file in folder_files if file['name'] == selected_file_name)
            else:
                selected_file = next(file for file in files if file['name'] == selected_file_name)

            file_id = selected_file['id']
            st.sidebar.write(f"Você selecionou o arquivo: {selected_file['name']}")
            # Aqui você pode implementar a lógica de exibição do conteúdo do arquivo, como no código anterior.
            # Por exemplo, exibir o conteúdo do arquivo .docx ou outro tipo de arquivo conforme necessário.

        # Authentication button (commented out for now)
        # if st.button("Reautenticar"):
        #     service = authenticate()

    # Exibir mensagem de status
    # st.text("Status da autenticação:")
    # st.text("Autenticação: Bem-sucedida")

        # Authentication for Google Drive
        #service = authenticate()

    # Footer with custom background color
    #st.markdown(""" 
        #<footer style='text-align: center; background-color: #2C3E50; color: white; padding: 10px;'>
            #© 2025 - LABIBIO - Biotério & Neuroscience
        #</footer>
    #""", unsafe_allow_html=True)
    #import streamlit as st

    # Footer with custom background color and fixed to the bottom of the page
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)
    
import streamlit as st
if __name__ == "__main__":
    main()

