import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values

# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Escolha um valor ímpar para o comprimento da janela
polyorder = 3  # Ordem do polinômio para o ajuste

smoothed_x = savgol_filter(acceleration_x, window_length, polyorder)

# Plotar os gráficos
plt.figure(figsize=(15, 5))

# Primeiro subplot
plt.subplot(1, 1, 1)
plt.plot(time, acceleration_x, linestyle='--', color='b', label='Original')
plt.plot(time, smoothed_x, linestyle='-', color='r', label='Suavizado')
plt.title('Aceleração 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.legend()

plt.show()
