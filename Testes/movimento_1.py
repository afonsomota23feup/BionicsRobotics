import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, find_peaks

# Carregar os dados do arquivo CSV
data = pd.read_csv('15_05_1.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values

# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Deve ser um número ímpar e maior que polyorder
polyorder = 3
smoothed_acc_x = savgol_filter(acceleration_x, window_length, polyorder)

# Integração para obter a velocidade
velocity_x = np.cumsum(smoothed_acc_x) * (time[1] - time[0])

# Integração para obter a posição
position_x = np.cumsum(velocity_x) * (time[1] - time[0])

# Plotar os gráficos
plt.figure(figsize=(15, 5))

# Primeiro subplot - Aceleração
plt.subplot(3, 1, 1)
plt.plot(time, acceleration_x, linestyle='--', color='b', label='Aceleração Original')
plt.plot(time, smoothed_acc_x, linestyle='-', color='g', label='Aceleração Suavizada')
plt.title('Aceleração')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.legend()

# Segundo subplot - Velocidade
plt.subplot(3, 1, 2)
plt.plot(time, velocity_x, linestyle='-', color='r', label='Velocidade Integrada')
plt.title('Velocidade')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.legend()

# Terceiro subplot - Posição
plt.subplot(3, 1, 3)
plt.plot(time, position_x, linestyle='-', color='purple', label='Posição Integrada')
plt.title('Posição')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.legend()

plt.tight_layout()
plt.show()
