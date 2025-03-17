import streamlit as st
import hmac
import streamlit.components.v1 as components
import io
from io import BytesIO

st.set_page_config(
    page_title="Métodos e técnicas",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="expanded",
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
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Escopos necessários para acessar o Google Drive
#SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

#def authenticate():
    #"""Autenticação com o Google Drive usando as credenciais do Streamlit secrets"""
    
    # A autenticação deve ser feita explicitamente apenas na página inicial
    #if "google_drive_service" not in st.session_state:
        ##st.write("Autenticando.")
        
        #google_secrets = st.secrets["google"]
        #credentials_dict = {
            #"type": "service_account",
            #"project_id": google_secrets["project_id"],
            #"private_key_id": google_secrets["private_key_id"],
            #"private_key": google_secrets["private_key"],
            #"client_email": google_secrets["client_email"],
            #"client_id": google_secrets["client_id"],
            #"auth_uri": google_secrets["auth_uri"],
            #"token_uri": google_secrets["token_uri"],
            #"auth_provider_x509_cert_url": google_secrets["auth_provider_x509_cert_url"],
            #"client_x509_cert_url": google_secrets["client_x509_cert_url"],
            #"universe_domain": google_secrets["universe_domain"]
        #}
        
        #credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
        #service = build('drive', 'v3', credentials=credentials)
        
        # Testa a autenticação (opcional, dependendo do que você deseja verificar)
        #test_authentication(service)
        
        # Salva o serviço autenticado no session_state para uso em outras páginas
        #st.session_state["google_drive_service"] = service
        #st.write("Autenticação concluída com sucesso.")
    
    #else:
        #st.write("Bem vindo.")

    #return st.session_state["google_drive_service"]

# Função para autenticar e obter o serviço do Google Drive
#def authenticate_google_drive():
    #"""Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    #if "google_drive_service" not in st.session_state:
        #st.error("Erro: Acesso não autorizado. Por favor, faça login.")
        #st.stop()
        
    #return st.session_state["google_drive_service"]

# Função para listar arquivos no Google Drive
#def list_files(service, folder_id=None, include_shared=False):
    #"""Lista arquivos e pastas do Google Drive, incluindo arquivos compartilhados"""
    #try:
        #query = "trashed = false"
        
        # Se houver um folder_id, filtra por essa pasta
        #if folder_id:
            #query += f" and '{folder_id}' in parents"

        # Se include_shared for True, buscamos também pastas compartilhadas como 'Neuroscience'
        #if include_shared:
            #query += " or sharedWithMe = true"

        # Realiza a busca usando a API
        #results = service.files().list(q=query, pageSize=50, fields="files(id, name, mimeType)").execute()
        #items = results.get('files', [])
        #return items

    #except Exception as e:
        #st.error(f"Erro ao listar arquivos: {e}")
        #return []

#def upload_to_drive(file_name, file_data, folder_id=None):
    #"""Faz o upload de qualquer tipo de arquivo para o Google Drive sem salvar localmente"""
    #try:
        # Conectar à API do Google Drive
        #service = authenticate_google_drive()
        
        # Determinar o tipo MIME do arquivo baseado na extensão
        #if file_name.endswith('.csv'):
            #mime_type = 'text/csv'
        #elif file_name.endswith('.xlsx'):
            #mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        #elif file_name.endswith('.txt'):
            #mime_type = 'text/plain'
        #else:
            #mime_type = 'application/octet-stream'  # Tipo genérico para outros arquivos
        
        # Cria o arquivo no Google Drive
        #file_metadata = {'name': file_name}
        
        # Se uma pasta foi escolhida, o arquivo será enviado para essa pasta
        #if folder_id:
            #file_metadata['parents'] = [folder_id]
        
        # Lê o arquivo carregado diretamente como um fluxo de bytes
        #file_data_bytes = BytesIO(file_data.read())
        
        # Cria o MediaIoBaseUpload com os dados binários e o tipo MIME correto
        #media = MediaIoBaseUpload(file_data_bytes, mimetype=mime_type)
        
        # Faz o upload para o Google Drive
        #file = service.files().create(
            #body=file_metadata,
            #media_body=media,
            #fields='id'
        #).execute()

        #st.success(f"Arquivo '{file_name}' carregado com sucesso para o Google Drive! ID do arquivo: {file['id']}")
    
    #except Exception as e:
        #st.error(f"Erro ao fazer upload para o Google Drive: {e}")

# Defina o link do iframe
#link_iframe = "https://docs.google.com/forms/d/e/1FAIpQLSdJLX4Df90yj_o0k9VVw72cSpzguJa7jMV3xxRQ7ByXdqThMA/viewform"

# Inserir o iframe no Streamlit
#html_code = f'<iframe src="{link_iframe}" width="800" height="600"></iframe>'

# Upload de novo arquivo
st.title("Faça upload para o drive")
with st.container(border=True):
    uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

#with st.container(border=True):
    # Exibir o iframe
    #components.html(html_code, height=600)

# Função principal que encapsula a lógica de exibição
#def main():

    # Upload de novo arquivo
    #st.title("Faça upload para o drive")
    #uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])
    
    # Autenticação para o Google Drive
    #service = authenticate_google_drive()
    
    # Sidebar para navegação e autenticação
    #with st.sidebar:
        #st.header("Índice")
        
        # Autenticação para o Google Drive
        #service = authenticate_google_drive()

        # Listar arquivos e pastas, incluindo compartilhados, por padrão
        #items = list_files(service, include_shared=True)

        # Separar pastas e arquivos
        #folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        #files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

        # Mostrar pastas na sidebar (Se houver pastas)
        #if folders:
            #selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", [folder['name'] for folder in folders])
            #selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)

            # Se uma pasta for selecionada, listar arquivos dentro dela
            #if selected_folder:
                #selected_folder_id = selected_folder['id']
                #folder_files = list_files(service, folder_id=selected_folder_id, include_shared=True)
                #selected_file_name = st.sidebar.selectbox("Escolha um arquivo dentro da pasta", [file['name'] for file in folder_files])
            #else:
                #selected_file_name = None
        #else:
            #selected_folder = None
            #selected_file_name = st.sidebar.selectbox("Escolha um arquivo na raiz", [file['name'] for file in files])

        # Fetch the selected file
        #if selected_file_name:
            #if selected_folder:
                #selected_file = next(file for file in folder_files if file['name'] == selected_file_name)
            #else:
                #selected_file = next(file for file in files if file['name'] == selected_file_name)

            #file_id = selected_file['id']
            #st.sidebar.write(f"Você selecionou o arquivo: {selected_file['name']}")
            # Aqui você pode implementar a lógica de exibição do conteúdo do arquivo, como no código anterior.
            # Por exemplo, exibir o conteúdo do arquivo .docx ou outro tipo de arquivo conforme necessário.

    # Upload de novo arquivo
    #st.title("Faça upload para o drive")
    #uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

    # Verifique se um arquivo foi carregado antes de tentar fazer upload
    #if uploaded_file is not None:
        #upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)
    
    # Footer com custom background color e fixado no fundo da página
    #st.markdown("""<footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            #LABIBIO 2025 - Biotério & Neuroscience
        #</footer>""", unsafe_allow_html=True)
    
# Chama a função main() para exibir o conteúdo
#if __name__ == "__main__":
#main()
#import pandas as pd
#from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
