import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks
from scipy.integrate import cumtrapz

# Carregar os dados do arquivo CSV
data = pd.read_csv('15_05_1.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_y = data['Linear Acceleration y (m/s^2)'].values

# Initialize filter
filter_window = 5
filter_coeff = np.ones(filter_window) / filter_window

# Filter the data
filtered_y = np.convolve(acceleration_y, filter_coeff, mode='same')

# Substituir valores entre -1 e 1 por zero
filtered_y[(filtered_y >= -1) & (filtered_y <= 1)] = 0

# Integrar a aceleração para obter a velocidade
velocity_y = cumtrapz(filtered_y, time, initial=0)

# Integrar a velocidade para obter a posição
position_y = cumtrapz(velocity_y, time, initial=0)

# Converter a posição de metros para centímetros
position_y_cm = position_y * 100

# Criar a figura e o subplot 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Definir os limites fixos dos eixos
max_range_y_cm = (max(position_y_cm) - min(position_y_cm)) * 0.2  # Reduzindo em 20%
ylim_cm = (min(position_y_cm) + max_range_y_cm, max(position_y_cm) - max_range_y_cm)

# Inicialização da animação (função vazia)
def init():
    ax.set_ylim(ylim_cm)
    # Adicionar a bolinha no centro do referencial
    ax.scatter(0, 0, 0, color='purple', s=50)
    return [ax]

# Função para determinar a cor com base na direção da posição
def get_color(dy):
    if dy > 0:
        return 'g'  # Movimento positivo no eixo y
    elif dy < 0:
        return 'r'  # Movimento negativo no eixo y
    else:
        return 'b'  # Sem movimento

# Função de animação
def update(frame):
    ax.cla()
    ax.set_ylim(ylim_cm)
    for i in range(1, frame):
        color = get_color(position_y_cm[i] - position_y_cm[i-1])
        ax.plot([i-1, i], [position_y_cm[i-1], position_y_cm[i]], color=color)
    
    # Adicionar a bolinha na posição atual
    ax.scatter(frame-1, position_y_cm[frame-1], color='purple', s=50)
    
    ax.set_ylabel('Posição eixo y (cm)')
    return [ax]

# Criar animação
ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True)

plt.show()

