import streamlit as st
import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json

# SCOPES que você já definiu
SCOPES = ['https://www.googleapis.com/auth/drive.files', 'https://www.googleapis.com/auth/drive.metadata.readonly']

# Função para autenticar o usuário usando OAuth 2.0 com os dados do secrets.toml
def authenticate():
    """Autentica o usuário e retorna o serviço da API do Google Drive usando OAuth 2.0."""
    creds = None

    # Carregar as credenciais OAuth 2.0 do secrets.toml
    google_secrets = st.secrets["google"]
    client_id = google_secrets["client_id"]
    client_secret = google_secrets["client_secret"]
    redirect_uris = google_secrets["redirect_uris"]
    credentials_info = json.loads(google_secrets["json_credentials"])

    # O arquivo token.pickle armazena as credenciais de acesso do usuário.
    # Ele é criado automaticamente após a primeira execução do fluxo de autenticação.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se as credenciais não forem válidas ou expiraram, faça o login novamente
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Se não houver credenciais válidas, faz o login com o OAuth
            flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para a próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Cria o serviço da API do Google Drive com as credenciais
    service = build('drive', 'v3', credentials=creds)
    return service

# Função para listar arquivos e pastas do Google Drive
def list_files(service, folder_id='root', page_token=None):
    """Lista arquivos e pastas do Google Drive, dados o folder_id"""
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="nextPageToken, files(id, name, mimeType)",
        pageSize=1000,
        pageToken=page_token
    ).execute()

    return results.get('files', []), results.get('nextPageToken')

# Função para buscar a pasta chamada 'Neuroscience' e obter seu ID
def get_neuroscience_folder_id(service):
    """Busca pela pasta chamada 'Neuroscience' e retorna o ID dela"""
    results = service.files().list(
        q="name = 'Neuroscience' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        fields="files(id, name)"
    ).execute()

    # Se encontrar a pasta, retorna o ID
    if results.get('files', []):
        return results['files'][0]['id']
    else:
        return None

# Função para upload de arquivo para o Google Drive
def upload_file_to_drive(service, file, mime_type):
    """Faz o upload de um arquivo para o Google Drive."""
    file_metadata = {'name': file.name}
    media = MediaFileUpload(file, mimetype=mime_type)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file['id']

# Função principal para o app Streamlit
def main():
    st.title("🐁 Servidor - Biotério e Neurociência")
    
    # Flash messages (em Streamlit podemos usar st.success ou st.error)
    if 'flash_message' in st.session_state:
        st.success(st.session_state['flash_message'])
        del st.session_state['flash_message']
    
    # Autenticar no Google Drive
    service = authenticate()

    # Buscar o ID da pasta "Neuroscience"
    folder_id = get_neuroscience_folder_id(service)
    
    if folder_id is None:
        st.error("A pasta 'Neuroscience' não foi encontrada no Google Drive.")
        return

    # Barra lateral para listar pastas e arquivos
    st.sidebar.title("Google Drive - Navegação")
    
    # Listar pastas e arquivos da pasta "Neuroscience"
    files, next_page_token = list_files(service, folder_id)

    st.sidebar.write("Pastas e Arquivos em 'Neuroscience':")
    for f in files:
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            # Exibir pastas
            st.sidebar.write(f"📂 {f['name']}")
        else:
            # Exibir arquivos
            st.sidebar.write(f"📄 {f['name']}")

    # Navegação para a próxima página de arquivos
    if next_page_token:
        if st.sidebar.button("Carregar mais arquivos"):
            more_files, _ = list_files(service, folder_id, next_page_token)
            files.extend(more_files)
            for f in more_files:
                if f['mimeType'] == 'application/vnd.google-apps.folder':
                    st.sidebar.write(f"📂 {f['name']}")
                else:
                    st.sidebar.write(f"📄 {f['name']}")

    # Fazer upload de arquivos
    uploaded_file = st.file_uploader("Escolha um arquivo (até 2GB)", type=['pdf', 'jpg', 'jpeg', 'png', 'txt', 'mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv'])
    
    if uploaded_file is not None:
        try:
            file_id = upload_file_to_drive(service, uploaded_file, uploaded_file.type)
            st.session_state['flash_message'] = f"Arquivo '{uploaded_file.name}' enviado para o Google Drive com sucesso!"
        except Exception as e:
            st.session_state['flash_message'] = f"Erro ao enviar o arquivo: {str(e)}"
    
    # Rodapé com cor de fundo personalizada
    st.markdown(""" 
        <footer style='text-align: center; background-color: #2C3E50; color: white; padding: 10px;'>
            © 2025 - LABIBIO - Biotério e Neurociência
        </footer>
    """, unsafe_allow_html=True)

# Executar o Streamlit app
if __name__ == "__main__":
    main()
