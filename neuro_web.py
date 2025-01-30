import streamlit as st
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import io

# Configuração do diretório de uploads local
UPLOAD_FOLDER = './uploads'  # Pasta para armazenar os arquivos localmente
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Extensões permitidas
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Autenticação no Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

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

# Função para upload para o Google Drive
def upload_file_to_drive(service, file_path, mime_type):
    """Faz o upload de um arquivo para o Google Drive."""
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file['id']

# Função principal para o app Streamlit
def main():
    st.title("🐁 Servidor - Biotério e Neurociência")
    
    # Exibir mensagens de flash
    if 'flash' in st.session_state:
        st.success(st.session_state.flash)
        del st.session_state.flash

    # Formulário de upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo (até 2GB):", type=list(ALLOWED_EXTENSIONS))
    
    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            # Salvar o arquivo localmente
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Autenticar e fazer o upload para o Google Drive
            service = authenticate()
            file_id = upload_file_to_drive(service, file_path, uploaded_file.type)

            st.session_state.flash = f'Arquivo "{uploaded_file.name}" enviado para o Google Drive com sucesso!'
        else:
            st.session_state.flash = f'Arquivo inválido! Somente arquivos permitidos: {", ".join(ALLOWED_EXTENSIONS)}.'
        
        # Atualiza a página
        st.experimental_rerun()

    # Lista de arquivos para download
    st.subheader("Arquivos disponíveis para download:")
    files = os.listdir(UPLOAD_FOLDER)
    if files:
        for file in files:
            file_link = f'<a href="files/{file}" download>{file}</a>'
            st.markdown(file_link, unsafe_allow_html=True)
    else:
        st.write("Nenhum arquivo disponível para download.")

if __name__ == "__main__":
    main()
