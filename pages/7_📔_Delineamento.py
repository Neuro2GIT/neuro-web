import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_timeline(aclim, trat, teste, disseccao):
    fases = ["Aclimatação", "Tratamento", "Teste Comportamental", "Dissecação"]
    duracoes = [aclim, trat, teste, disseccao]
    cores = ["blue", "green", "orange", "red"]
    
    inicio = np.cumsum([0] + duracoes[:-1])
    fim = np.cumsum(duracoes)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    
    # Criando a linha do tempo no eixo X
    ax.hlines(0, 0, sum(duracoes), color='black', linewidth=2)
    
    # Alternar os textos acima e abaixo da linha do tempo
    text_offsets = [0.5, -0.5]  # Alternância para facilitar leitura
    
    for i in range(len(fases)):
        x_pos = (inicio[i] + fim[i]) / 2
        y_pos = text_offsets[i % 2]
        
        # Marcador no eixo X
        ax.plot(x_pos, 0, 'o', color=cores[i], markersize=8)
        
        # Linha vertical conectando marcador ao texto
        ax.vlines(x_pos, 0, y_pos, color=cores[i], linestyle='dotted')
        
        # Texto da fase
        ax.text(x_pos, y_pos, fases[i], ha='center', va='center', fontsize=10, color=cores[i], fontweight='bold')
    
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, sum(duracoes) + 1, 1))
    ax.set_xlabel("Dias")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

st.title("Delineamento Experimental - Linha do Tempo")

# Entrada do usuário
dias_aclim = st.number_input("Dias de Aclimatação", min_value=1, value=3)
dias_trat = st.number_input("Dias de Tratamento", min_value=1, value=7)
dias_teste = st.number_input("Dias de Teste Comportamental", min_value=1, value=2)
dias_dissec = st.number_input("Dias até a Dissecação", min_value=1, value=1)

if st.button("Gerar Linha do Tempo"):
    plot_timeline(dias_aclim, dias_trat, dias_teste, dias_dissec)

# Usando CSS para definir a cor de fundo
st.markdown(
    """
    <style>
    .custom-container {
        background-color: #ADD8E6;  /* Cor de fundo azul claro */
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #000000;  /* Cor da borda */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Criando o container
with st.container(border=True):
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    st.title('Título dentro do container com fundo colorido!')
    st.write('Aqui está um exemplo de como adicionar um fundo colorido a um container.')
    st.markdown('</div>', unsafe_allow_html=True)
