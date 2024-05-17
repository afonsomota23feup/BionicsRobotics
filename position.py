import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values

# Calcular a velocidade a partir da aceleração
velocity_x = np.cumsum(acceleration_x)

# Calcular a posição a partir da velocidade
position_x = np.cumsum(velocity_x)


# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Deve ser um número ímpar e maior que polyorder
polyorder = 3
smoothed_x = savgol_filter(acceleration_x, window_length, polyorder)

# Detectar os picos nos dados originais
# peaks, _ = find_peaks(acceleration_x, height=2)

# # Definir a largura da janela ao redor dos picos para preservação
# peak_window = 5

# # Restaurar os valores dos picos significativos e seus arredores nos dados suavizados
# smoothed_x_with_peaks = smoothed_x.copy()
# for peak in peaks:
#     start = max(0, peak - peak_window)
#     end = min(len(acceleration_x), peak + peak_window + 1)
#     smoothed_x_with_peaks[start:end] = acceleration_x[start:end]

# # Aplicar amplificação mais agressiva para maximizar os picos
# amplification_factor = np.max(acceleration_x[peaks]) / np.max(smoothed_x_with_peaks[peaks])
# # Ajustar o fator de amplificação para ser mais agressivo
# amplification_factor *= 2.0  # Aumentar o fator para amplificar mais os picos

# smoothed_x_with_peaks *= amplification_factor

# # Plotar os gráficos
# plt.figure(figsize=(15, 5))

# # Primeiro subplot
# plt.subplot(1, 1, 1)
# plt.plot(time, acceleration_x, linestyle='--', color='b', label='Original')
# plt.plot(time, smoothed_x, linestyle='-', color='g', label='Suavizado (Savitzky-Golay)')
# plt.plot(time, smoothed_x_with_peaks, linestyle='-', color='r', label='Suavizado com Picos Restaurados e Amplificados')
# plt.title('Aceleração 1')
# plt.xlabel('Tempo (s)')
# plt.ylabel('Aceleração (m/s^2)')
# plt.legend()

# plt.show()

# Primeiro subplot
plt.subplot(1, 1, 1)
plt.plot(time, position_x, linestyle='--', color='b', label='Original')
plt.plot(time, acceleration_x, linestyle='--', color='b', label='Original')
plt.title('posição 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.legend()

plt.show()

