import hmac
import streamlit as st
import pytz
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests

st.set_page_config(
    page_title="Grupo neuroscience",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={})
st.set_option('client.showErrorDetails', True)

# Função para gerar a saudação baseada no horário
def get_greeting():
    # Definir o fuso horário do Acre (GMT-5)
    timezone = pytz.timezone("America/Rio_Branco")
    
    # Obtém a hora atual no fuso horário do Acre
    current_time_acre = datetime.now(timezone)
    
    # Extrair a hora ajustada
    current_hour = current_time_acre.hour
    
    # Definir as saudações com base na hora do dia
    if current_hour < 12:
        return "Bom dia"
    elif current_hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

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
    "Publicações do grupo": [
        "10.22289/2446-922X.V10N1A23"
    ],
    "Artigos base": [
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

# Função principal para exibir o conteúdo
def main():
    st.title("🧠 Neuroscience Interest Group")
    
    st.markdown("---")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Conteúdo estático para adicionar a dissertação
    static_themes = {
        "Modelo de Deficiência de Tiamina": {
            "Alterações cognitivas espaciais e parâmetros neuroquímicos cerebrais associados aos processos de morte celular em modelos experimentais de deficiência de tiamina e/ou consumo de etanol.":"",
            "Autor": "Rogério de Freitas Lacerda",
            "Tese de doutorado": "2020",
            "Repositorio UFMG": "http://hdl.handle.net/1843/33624",
            "Baixar PDF": "https://repositorio.ufmg.br/bitstream/1843/33624/1/Tese%20vers%c3%a3o%20FINAL.pdf"
        }
    }

    # Exibindo os temas estáticos em expanders
    for theme, content in static_themes.items():
        with st.expander(theme):
            for section_title, section_content in content.items():
                st.markdown(f"**{section_title}**")
                st.markdown(section_content)
    
    # Iterar pelos temas e artigos
    for theme, dois in themes.items():
        with st.container(border=True):
            st.subheader(theme)  # Exibir o nome do tema como um subtítulo
            #st.markdown("---")  # Linha separadora para melhor organização
        
        st.markdown("<br><br>", unsafe_allow_html=True)
            
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

                         #LINK DA TESE DO PROFESSOR: http://hdl.handle.net/1843/33624 PDF: https://repositorio.ufmg.br/bitstream/1843/33624/1/Tese%20vers%c3%a3o%20FINAL.pdf
                    
                    # Botão para marcar como lido
                    #if st.button(f"Marcar {title} como lido"):
                        #if 'read_articles' not in st.session_state:
                            #st.session_state.read_articles = []
                        #st.session_state.read_articles.append(title)  # Armazena os artigos lidos
            #else:
                #st.error(f"Não foi possível recuperar informações para o DOI: {doi}. Verifique o DOI ou tente novamente.")

    # Footer
    #st.markdown("""
        #<footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            #LABIBIO 2025 - Neurogroup
        #</footer>
    #""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
