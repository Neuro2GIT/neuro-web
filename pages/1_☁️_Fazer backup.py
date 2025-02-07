import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io

# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
        
    return st.session_state["google_drive_service"]

def list_files(service, folder_id=None):
    """Lista arquivos e pastas do Google Drive"""
    try:
        query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
        results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])
        return items

        # Verificando a estrutura da resposta
        if isinstance(results, dict):
            return results.get('files', [])
        else:
            st.error("A resposta da API não está no formato esperado. A resposta foi: " + str(results))
            return []
    
    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return []

#def list_files(service, folder_id=None):
    #"""Lista arquivos e pastas do Google Drive"""
    #try:
        # Se não for especificado o folder_id, estamos na raiz
        #query = "trashed = false"
        #if folder_id:
            #query = f"'{folder_id}' in parents and trashed = false"  # Filtra por pastas específicas

        #results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
        #items = results.get('files', [])
        #return items
    #except Exception as e:
        #st.error(f"Erro ao listar arquivos: {e}")
        #return []

# Função para upload de arquivo para o Google Drive
def upload_to_drive(file_name, file_data, folder_id=None):
    """Faz o upload do arquivo para o Google Drive"""
    try:
        # Conectar à API do Google Drive
        service = authenticate_google_drive()
        
        # Cria o arquivo no Google Drive
        file_metadata = {'name': file_name}
        
        # Se uma pasta foi escolhida, o arquivo será enviado para essa pasta
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaIoBaseUpload(file_data, mimetype='text/csv')  # Ajuste o mimetype conforme o tipo de arquivo

        # Faz o upload para o Google Drive
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        st.success(f"Arquivo '{file_name}' carregado com sucesso para o Google Drive! ID do arquivo: {file['id']}")
    
    except Exception as e:
        st.error(f"Erro ao fazer upload para o Google Drive: {e}")

# Função principal
def main():
    # Sidebar para navegação e autenticação
    with st.sidebar:
        st.header("Índice")
        #st.text("Escolha uma das opções abaixo para navegar")

        # Authentication for Google Drive
        service = authenticate_google_drive()

        # List files and folders from root
        items = list_files(service)

        # Separate folders and files
        folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

        # Show folders in sidebar
        selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", [folder['name'] for folder in folders] if folders else ["Sem pastas"])
        selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)
        
        # Show files in sidebar
        if selected_folder:
            selected_folder_id = selected_folder['id']
            folder_files = list_files(service, folder_id=selected_folder_id)
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo dentro da pasta", [file['name'] for file in folder_files])
        else:
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo na raiz", [file['name'] for file in files])

        # Fetch the selected file
        if selected_file_name:
            if selected_folder:
                selected_file = next(file for file in folder_files if file['name'] == selected_file_name)
            else:
                selected_file = next(file for file in files if file['name'] == selected_file_name)

            file_id = selected_file['id']

            # Download the file from Google Drive
            #file = service.files().get_media(fileId=file_id).execute()
            #file_path = f"temp_{selected_file_name}.xlsx"
            #with open(file_path, 'wb') as f:
                #f.write(file)

            # Load and display the Excel content with Pandas
            #df = pd.read_excel(file_path)
            #st.write("Conteúdo do arquivo Excel:", df)

            # Allow table editing using st-aggrid
            #gb = GridOptionsBuilder.from_dataframe(df)
            #gb.configure_pagination()  # Enable pagination
            #gb.configure_default_column(editable=True)  # Allow editing
            #grid_options = gb.build()

            # Display editable table with AgGrid
            #edited_df = AgGrid(df, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)

            # Allow uploading the edited file back to Google Drive
            #if st.button("Salvar alterações"):
                #edited_df['data'].to_excel(file_path, index=False)  # Save the edits in the Excel file
                # Upload the edited file back to Google Drive
                #media = MediaIoBaseDownload(io.open(file_path, 'rb'), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                #service.files().update(fileId=file_id, media_body=media).execute()
                #st.success("Alterações salvas no Google Drive!")

    # Upload de novo arquivo
    st.title("Faça upload para o drive")
    uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

    # Verifique se um arquivo foi carregado antes de tentar fazer upload
    #if uploaded_file is not None:
        #upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)
    #else:
        #st.warning("Nenhum arquivo carregado.")

    # Rodapé estilizado para fixar na parte inferior sem sobrepor o conteúdo
    st.markdown("""
        <style>
            body {
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                margin: 0;
            }
            main {
                flex: 1;
            }
            footer {
                text-align: center;
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                width: 100%;
                bottom: 0;
                left: 0;
                position: relative;
            }
        </style>
        <footer>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
main()
