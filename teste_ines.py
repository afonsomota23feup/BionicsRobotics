import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values
acceleration_y = data['Linear Acceleration y (m/s^2)'].values
acceleration_z= data['Linear Acceleration z (m/s^2)'].values

# Initialize filter
filter_window = 5
filter_coeff = np.ones(filter_window)/filter_window
calibration_offset = 0
calibration_gain = 1
    
# Filter the data
filtered_x = np.convolve(acceleration_x, filter_coeff, mode='same')
# filtered_y = np.convolve(acceleration_y, filter_coeff, mode='same')
# filtered_z = np.convolve(acceleration_z, filter_coeff, mode='same')

#Testar a seguir
# Detectar os picos em cada série temporal
# peaks_acceleration_x, _ = find_peaks(filtered_x)
# peaks_acceleration_y, _ = find_peaks(filtered_y)
# peaks_acceleration_z, _ = find_peaks(filtered_z)

# Definir os valores seguintes aos picos como zero
for peak in peaks_acceleration_x:
    acceleration_x[peak + 1] = 0
# for peak in peaks_acceleration_y:
#     acceleration_y[peak + 1] = 0
# for peak in peaks_acceleration_z:
#     acceleration_z[peak + 1] = 0

# Plotar os gráficos
plt.figure(figsize=(15, 5))

# Primeiro subplot
plt.subplot(1, 3, 1)
plt.plot(time, peaks_acceleration_x, linestyle='--', color='b')
plt.title('Aceleração 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')