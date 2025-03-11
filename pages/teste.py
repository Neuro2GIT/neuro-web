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
    y_pos = np.zeros(len(fases))
    
    for i in range(len(fases)):
        ax.plot([inicio[i], fim[i]], [y_pos[i], y_pos[i]], color=cores[i], linewidth=4, marker='o', markersize=10)
        ax.text((inicio[i] + fim[i]) / 2, y_pos[i] + 0.2, fases[i], ha='center', va='bottom', fontsize=10, color=cores[i])
    
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
