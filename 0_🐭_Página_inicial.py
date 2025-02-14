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
    menu_items={})
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
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Função de autenticação com Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Autenticação com o Google Drive usando as credenciais do Streamlit secrets"""
    if "google_drive_service" not in st.session_state:
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

        # Testa a autenticação para garantir que está funcionando corretamente
        test_authentication(service)
        
        # Armazena o serviço no session_state
        st.session_state["google_drive_service"] = service
    else:
        st.write("Bem-vindo! Serviço já autenticado.")

    return st.session_state["google_drive_service"]

def test_authentication(service):
    """Função de teste para validar a autenticação"""
    try:
        # Testa a autenticação
        about = service.about().get(fields="user").execute()
        st.write(f"Autenticado como: {about['user']['emailAddress']}")
    except Exception as e:
        st.error(f"Falha na autenticação: {e}")

#def list_files(service, folder_id=None):
    #"""Lista arquivos do Google Drive"""
    #query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
    #results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
    #items = results.get('files', [])
    #return items

# Função principal para exibir o conteúdo
def main():
    st.title("🐁Grupo neuroscience")

    # Obtém o serviço do Google Drive
    service = authenticate()

    # Exemplo de listagem de arquivos na raiz
    #files = list_files(service)
    #st.write(f"Arquivos disponíveis: {files}")

    # Footer
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
