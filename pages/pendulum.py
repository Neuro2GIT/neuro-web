import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros do pêndulo
g = 9.81  # aceleração devido à gravidade (m/s^2)
L = 1.0   # comprimento do pêndulo (m)
theta_0 = np.pi / 4  # ângulo inicial (rad)

# Função para calcular a posição do pêndulo ao longo do tempo
def pendulum(t, theta_0):
    return theta_0 * np.cos(np.sqrt(g / L) * t)

# Criar o gráfico
fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

line, = ax.plot([], [], 'o-', lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(t):
    x = L * np.sin(pendulum(t, theta_0))
    y = -L * np.cos(pendulum(t, theta_0))
    line.set_data([0, x], [0, y])
    return line,

# Animação
ani = FuncAnimation(fig, animate, frames=np.linspace(0, 10, 200),
                    init_func=init, blit=True)

plt.show()
