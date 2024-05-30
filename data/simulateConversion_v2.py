import csv
import struct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


raw_data_points = []
converted_data_points = []
instants_data = []

# time = data['Time (s)'].values
acceleration_x = []
acceleration_y = []
acceleration_z = []
giroscope_x = []
giroscope_y = []
giroscope_z = []
time = []
force = []
velocity_x = []
position_x = []


raw_data_points = []
converted_data_points = []
instants_data = []
unpackedData = []

# 'gyro_data' is your gyroscope data, and 'dt' is the time step
alpha = 0.98  # This is the weight for the gyroscope data. You might need to adjust this.
dt = 1/50



# Carregar os dados do arquivo CSV
dataLoad = pd.read_csv('bytearrays_Hex.csv')

# Extrair os valores de tempo e acelerações
bytearray_strings = dataLoad['column_byte'].values

# List to store the converted data points
converted_data_points = []

# Iterate over each string representing a bytearray
for bytearray_string in bytearray_strings:
    # Convert the hexadecimal string back to a bytearray
    bytearray_data = bytearray.fromhex(bytearray_string)
    if len(bytearray_data) != 220:
        # Unpack the bytearray to extract data points
        unpackedData = struct.unpack('55f', bytearray_data[:220])  # Assuming each data point is a float (4 bytes)

        # Append the unpacked data to the list
        converted_data_points.append(unpackedData)

        #------------------Instant 1------------------
        ax1 = unpackedData[0]   
        ay1 = unpackedData[1]
        az1 = unpackedData[2]
        force11 = unpackedData[9]
        gx1 = unpackedData[3]
        gy1 = unpackedData[4]
        gz1 = unpackedData[5]

        # time = data['Time (s)'].values
        acceleration_x.append(ax1)
        acceleration_y.append(ay1)
        acceleration_z.append(az1)
        force.append(force11)
        giroscope_x.append(gx1)
        giroscope_y.append(gy1)
        giroscope_z.append(gz1)

        velocity_x1 = alpha * (np.cumsum(gx1) * dt) + (1 - alpha) * np.array(ax1)
        velocity_x.append(velocity_x1)
        position_x1 = np.cumsum(velocity_x1) * dt
        position_x.append(position_x1)



        #------------------Instatnt 2------------------

        ax2 = unpackedData[11]
        ay2 = unpackedData[12]
        az2 = unpackedData[13]
        force12 = unpackedData[20]
        gx2 = unpackedData[21]
        gy2 = unpackedData[22]
        gz2 = unpackedData[23]


        # time = data['Time (s)'].values
        acceleration_x.append(ax2)
        acceleration_y.append(ay2)
        acceleration_z.append(az2)
        force.append(force12)

            #------------------Instatnt 3------------------

        ax3 = unpackedData[22]
        ay3 = unpackedData[23]
        az3 = unpackedData[24]
        force13 = unpackedData[31]

        # time = data['Time (s)'].values
        acceleration_x.append(ax3)
        acceleration_y.append(ay3)
        acceleration_z.append(az3)
        force.append(force13)

            #------------------Instatnt 4------------------

        ax4 = unpackedData[33]
        ay4 = unpackedData[34]
        az4 = unpackedData[35]
        force14 = unpackedData[42]

        # time = data['Time (s)'].values
        acceleration_x.append(ax4)
        acceleration_y.append(ay4)
        acceleration_z.append(az4)
        force.append(force14)
        #------------------Instatnt 5------------------
        
        
        ax5 = unpackedData[44]
        ay5 = unpackedData[45]
        az5 = unpackedData[46]
        force15 = unpackedData[53]

    # time = data['Time (s)'].values
        acceleration_x.append(ax5)
        acceleration_y.append(ay5)
        acceleration_z.append(az5)
        force.append(force15)



# print ("Aceleração em X")
# print (acceleration_x)
# print ("Aceleração em Y")
# print (acceleration_y)
# print ("Aceleração em Z")
# print (acceleration_z)

# Assume 'acceleration' is your acceleration data,

#Assume 'acceleration' is your acceleration data,

# velocity_x = alpha * (np.cumsum(giroscope_x) * dt) + (1 - alpha) * np.array(acceleration_x)
# position_x = np.cumsum(velocity_x) * dt

#print(velocity_x)
# print(position_x)



plt.plot(acceleration_x, label='Aceleração em X')
plt.plot(velocity_x, label='Velocidade em X')
plt.plot(position_x, label='Posição em X')

plt.xlabel('Amostra')
plt.title('Aceleração, Velocidade e Posição vs Tempo em X')

plt.legend()  # Show legend with labels

plt.show()