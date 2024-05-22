import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ahrs import Quaternion, Accelerometer, Gyroscope, Madgwick

# Carregar os dados do arquivo CSV
data_acel = pd.read_csv('Accelerometer_v3.csv')
# Extrair os valores de tempo e acelerações
time = data_acel['Time (s)'].values
raw_acceleration_x = data_acel['Acceleration x (m/s^2)'].values
raw_acceleration_y = data_acel['Acceleration y (m/s^2)'].values
raw_acceleration_z = data_acel['Acceleration z (m/s^2)'].values

# Carregar os dados do arquivo CSV
data_gy = pd.read_csv('Gyroscope_v3.csv')
# Extrair os valores de tempo e giros
# Note que o tempo deve ser o mesmo para ambos os arquivos CSV
time = data_gy['Time (s)'].values
raw_gyro_x = data_gy['Gyroscope x (rad/s)'].values
raw_gyro_y = data_gy['Gyroscope y (rad/s)'].values
raw_gyro_z = data_gy['Gyroscope z (rad/s)'].values

# Carregar os dados do arquivo CSV
data_gy = pd.read_csv('Magnetometer_v3.csv')
# Extrair os valores de tempo e giros
# Note que o tempo deve ser o mesmo para ambos os arquivos CSV
time = data_gy['Time (s)'].values
raw_mag_x = data_gy['Magnetometer x (rad/s)'].values
raw_mag_y = data_gy['Magnetometer y (rad/s)'].values
raw_mag_z = data_gy['Magnetometer z (rad/s)'].values

# Criação dos objetos dos sensores
acc = Accelerometer(np.array([raw_acceleration_x, raw_acceleration_y, raw_acceleration_z]).T)
gyro = Gyroscope(np.array([raw_gyro_x, raw_gyro_y, raw_gyro_z]).T)
mag = Magnetometer(np.array([raw_mag_x, raw_mag_y, raw_mag_z]).T)

# Inicialização do filtro de orientação
attitude = Madgwick(acc=acc, gyr=gyro, mag=mag, gain=0.1, frequency=100.0)

# Estimativa da orientação
for i in range(attitude.Q.shape[0]):
    attitude.update()

# Conversão da orientação para matriz de rotação
R = attitude.Q[:, :3].dot(attitude.Q[:, :3].T)

# Cálculo da posição (supondo que a velocidade e o tempo sejam conhecidos)
velocity = np.zeros_like(acc_data)  # Dados da velocidade
time = np.arange(0, len(acc_data))  # Tempo
position = np.cumsum(R.dot(velocity), axis=0)

# Supondo que position seja uma matriz 3xN, onde cada coluna é uma coordenada espacial
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(position[0, :], position[1, :], position[2, :])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()