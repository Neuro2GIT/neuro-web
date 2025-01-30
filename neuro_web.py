import streamlit as st
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Definir as permissões e escopo de acesso
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata.readonly']

# Função para autenticar no Google Drive
def authenticate():
    """Autentica o usuário e retorna o serviço da API do Google Drive."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

# Função para listar arquivos e pastas do Google Drive
def list_files(service, folder_id='root'):
    """Lista arquivos e pastas do Google Drive, dados o folder_id"""
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="nextPageToken, files(id, name, mimeType)",
        pageSize=1000
    ).execute()
    
    return results.get('files', [])

# Função para upload para o Google Drive
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

    # Barra lateral para listar pastas e arquivos
    st.sidebar.title("Google Drive - Navegação")
    folder_id = st.sidebar.text_input('ID da Pasta', value='root')

    # Listar pastas e arquivos da pasta atual
    files = list_files(service, folder_id)
    
    if files:
        st.sidebar.write("Pastas e Arquivos:")
        for f in files:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                # Exibir pastas
                st.sidebar.write(f"📂 {f['name']}")
            else:
                # Exibir arquivos
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

