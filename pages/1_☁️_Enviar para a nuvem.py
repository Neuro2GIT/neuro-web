import streamlit as st

if not st.session_state.get("password_correct", False):
    st.write("Por favor, faça login para acessar a página.")
    # Adicionar formulário ou campo para login aqui (por exemplo, um campo de senha)
    
    senha = st.text_input("Digite a senha", type="password")
    
    if st.button("Entrar"):
        if senha == "sua_senha_aqui":  # Substitua por sua senha real
            st.session_state["password_correct"] = True
            st.success("Login bem-sucedido!")
        else:
            st.error("Senha incorreta. Tente novamente.")
else:
    # Página protegida, acessada após login bem-sucedido
    st.title("Página Protegida")
    st.write("Conteúdo visível apenas para usuários autenticados.")
    
    # Adicione o restante do conteúdo da página protegida aqui
    st.write("Conteúdo adicional da página protegida pode ir aqui.")

def main():
    st.title("🐁Grupo neuroscience")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
