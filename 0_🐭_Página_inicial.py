import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Grupo Neuroscience",
    page_icon="🐭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS
st.markdown("""
    <style>
        /* Estilo do cabeçalho */
        .header {
            background-color: #121212;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #27ae60;
        }
        .header-title {
            font-size: 2em;
            font-weight: bold;
            color: white;
        }
        .menu {
            display: flex;
            gap: 20px;
        }
        .menu a {
            color: #27ae60;
            text-decoration: none;
            font-size: 1.1em;
        }
        .menu a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown("""
    <div class="header">
        <div class="header-title">Neuroscience Group</div>
        <div class="menu">
            <a href="?page=Publicacoes">Publicações</a>
            <a href="?page=Introducao_DT">Modelo DT</a>
            <a href="?page=Metodos">Métodos</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Capturar a página selecionada via URL (simulando navegação)
query_params = st.query_params.to_dict()
page = query_params.get("page", "Publicacoes")

# Função para obter informações do DOI
def get_doi_info(doi):
    base_url = "https://api.crossref.org/works/"
    url = base_url + doi
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        title = data['message'].get('title', [''])[0]
        authors = ", ".join([
            f"{author.get('given', '')} {author.get('family', '')}".strip()
            for author in data['message'].get('author', [])
        ])
        published_year = data['message'].get('published', {}).get('date-parts', [[None]])[0][0]
        url = data['message'].get('URL', '')
        return title, authors, published_year, url
    return None, None, None, None

# Definição de categorias e artigos
themes = {
    "Publicacoes": ["10.22289/2446-922X.V10N1A23"],
    "Introducao_DT": [
        "10.1080/09168451.2016.1224639",
        "10.54038/ms.v1i1.2"
    ],
    "Metodos": [
        "10.1016/0003-2697(76)90527-3",
        "10.1590/S0100-40421998000600020"
    ]
}

# Exibição dos artigos da sessão selecionada
if page in themes:
    st.subheader(page.replace("_", " "))  # Título formatado
    for doi in themes[page]:
        title, authors, year, url = get_doi_info(doi)
        if title:
            st.markdown(f"### {title}\n**Autores:** {authors}\n**Publicado:** {year}\n[🔗 Acesse o artigo]({url})")
        else:
            st.warning(f"Não foi possível recuperar informações para o DOI: {doi}")
