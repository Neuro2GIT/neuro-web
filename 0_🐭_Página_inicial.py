import hmac
import streamlit as st
import requests
import pickle
import pandas as pd
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit_authenticator as stauth
from datetime import datetime
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

#def check_password():
    #"""Returns `True` if the user had the correct password."""
    #def password_entered():
        #"""Checks whether a password entered by the user is correct."""
        #if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            #st.session_state["password_correct"] = True
            #del st.session_state["password"]  # Don't store the password.
        #else:
            #st.session_state["password_correct"] = False

    # Return True if the password is validated.
    #if st.session_state.get("password_correct", False):
        #return True

    # Show input for password.
    #st.text_input("Password", type="password", on_change=password_entered, key="password")
    #if "password_correct" in st.session_state:
        #st.error("😕 Password incorrect")
    #return False


#if not check_password():
    #st.stop()  # Do not continue if check_password is not True.
    
# Função para gerar a saudação baseada no horário
#def get_greeting():
    # Definir o fuso horário do Acre (GMT-5)
    #timezone = pytz.timezone("America/Rio_Branco")
    
    # Obtém a hora atual no fuso horário do Acre
    #current_time_acre = datetime.now(timezone)
    
    # Extrair a hora ajustada
    #current_hour = current_time_acre.hour
    
    # Definir as saudações com base na hora do dia
    #if current_hour < 12:
        #return "Bom dia!"
    #elif current_hour < 18:
        #return "Boa tarde!"
    #else:
        #return "Boa noite!"


def get_doi_info(doi):
    base_url = "https://api.crossref.org/works/"
    url = base_url + doi
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        title = data['message']['title'][0]
        
        # Safely handle authors, checking if 'given' and 'family' exist
        authors = []
        for author in data['message'].get('author', []):
            given_name = author.get('given', '')
            family_name = author.get('family', '')
            if given_name or family_name:
                authors.append(f"{given_name} {family_name}".strip())
        authors = ", ".join(authors)
        
        # Get the publication year, ensuring the structure is correct
        published_year = data['message']['published']['date-parts'][0][0]
        
        # Get the URL and PDF link (if available)
        url = data['message'].get('URL', '')
        pdf_link = data['message'].get('link', [{}])[0].get('URL', '')
        
        return title, authors, published_year, url, pdf_link
    else:
        return None, None, None, None, None

# Definindo temas e artigos (DOIs) agrupados
themes = {
    "Publicações": [
        "10.22289/2446-922X.V10N1A23"
    ],
    "Introdução": [
        "10.1080/09168451.2016.1224639",
        "10.54038/ms.v1i1.2",
        "10.54038/ms.v2i2.20",
        "10.30574/gscarr.2023.15.3.0167"
    ],
    "Biureto / Bradford e BCA": [
        "10.1016/0003-2697(76)90527-3",
        "10.1590/S0100-40421998000600020",
        "10.1016/0003-2697(85)90442-7",
        "10.1016/S0021-9258(18)57021-6"
    ]
}

# Função de autenticação com Google Drive
#SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

#def authenticate():
    #"""Autenticação com o Google Drive usando as credenciais do Streamlit secrets"""
    #if "google_drive_service" not in st.session_state:
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

        # Testa a autenticação para garantir que está funcionando corretamente
        #test_authentication(service)
        
        # Armazena o serviço no session_state
        #st.session_state["google_drive_service"] = service
    #else:
        #st.write("")

    #return st.session_state["google_drive_service"]

#def test_authentication(service):
    #"""Função de teste para validar a autenticação"""
    #try:
        # Testa a autenticação
        #about = service.about().get(fields="user").execute()
        #st.write(f"Autenticado como: {about['user']['emailAddress']}")
    #except Exception as e:
        #st.error(f"Falha na autenticação: {e}")

##def list_files(service, folder_id=None):
    #"""Lista arquivos do Google Drive"""
    #query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
    #results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
    #items = results.get('files', [])
    #return items

# Função principal para exibir o conteúdo
def main():
    st.title("🧠 Neuroscience Interest Group")

     # Sidebar para navegação e autenticação
    with st.sidebar:
        st.header("Índice")
        opcao_selecionada = st.selectbox("Escolha uma opção", ["Artigos"])

    # Criar as tabs dependendo da seleção da técnica
    if opcao_selecionada == "Artigos":
        tabs = st.tabs(["Publicações", "Introdução", "Artigos de métodos"])

        with tabs[0]:
            st.write("Placeholder - Preparo de ração CT")
        # Iterar pelos temas e artigos
        for theme, dois in themes.items():
            st.subheader(theme)  # Exibir o nome do tema como um subtítulo
            st.markdown("---")  # Linha separadora para melhor organização

            for doi in dois:
                title, authors, published_year, url, pdf_link = get_doi_info(doi)
            
                if title:
                    with st.expander(title):
                        st.markdown(f"**Autores**: {authors}")
                        st.markdown(f"**Publicado em**: {published_year}")
                        st.markdown(f"[Leia o artigo completo]({url})")
                    
                        # Botão para baixar o PDF, se disponível
                        if pdf_link:
                            st.markdown(f"[Baixar PDF]({pdf_link})")
                    
                        # Botão para marcar como lido
                        if st.button(f"Marcar {title} como lido"):
                            if 'read_articles' not in st.session_state:
                                st.session_state.read_articles = []
                            st.session_state.read_articles.append(title)  # Armazena os artigos lidos
                else:
                    st.error(f"Não foi possível recuperar informações para o DOI: {doi}. Verifique o DOI ou tente novamente.")
           
    # Footer
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            Neurogroup
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
