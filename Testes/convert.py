import struct
import numpy as np
import matplotlib.pyplot as plt

acceleration_x = []
acceleration_y = []
acceleration_z = []
giroscope_x = []
giroscope_y = []
giroscope_z = []
time = []
force = []
data_bytes = []
instants_data = []

# Define a function to read the data from the file and convert it into the desired format
def load_data_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Create a list to store bytearrays
    data_list = []

    # Iterate over each line and convert to bytearray
    for line in lines:
        # Remove unwanted characters and whitespace
        cleaned_line = line.strip().replace('bytearray(b"', '').replace('")', '')

        # Convert the hexadecimal string to bytes
        byte_array = bytearray.fromhex(cleaned_line)

        # Add to the data list
        data_list.append(byte_array)
    
    return data_list

# Load the data from the 'data.txt' file
data = load_data_from_file('data.txt')
data_bytes_list = data

# Print the loaded data to verify the result
for byte_array in data:
    print(byte_array)

# Optionally, you can print the length of the data array to ensure all lines were read
print(f"Total byte arrays loaded: {len(data)}")

# Process each bytearray in the list
for data_bytes in data_bytes_list:
    # Decodificação de cada float
    unpackedData = struct.unpack('55f', data_bytes)  # 55 unpackedData no total, 4 bytes cada

# Iterando sobre cada instante
#recebemos 10 mensagens num segundo
#cada mensagem tem 5 instantes de 11 elementos, ou seja num segundo recebemos 50 instantes 
#os 3 primeiros elementos são o acelerometro x, y e z correspondente
#os 3 elementos seguintes são o giroscopio x, y e z correspondente
#os 3 elementos seguintes são o magnetometro x, y e z correspondente
#o elemento seguinte é a força 1 
#o elemento seguinte é a força 2

# Iterando sobre cada instante
print(f"Instante {1}:")
print(f"   Acelerômetro: ({unpackedData[0]}, {unpackedData[1]}, {unpackedData[2]})")
print(f"   Giroscópio: ({unpackedData[3]}, {unpackedData[4]}, {unpackedData[5]})")
print(f"   Magnetômetro: ({unpackedData[6]}, {unpackedData[7]}, {unpackedData[8]})")
print(f"   Força 1: {unpackedData[9]}")
print(f"   Força 2: {unpackedData[10]}")

print(f"Instante 2:")
print(f"   Acelerômetro: ({unpackedData[11]}, {unpackedData[12]}, {unpackedData[13]})")
print(f"   Giroscópio: ({unpackedData[14]}, {unpackedData[15]}, {unpackedData[16]})")
print(f"   Magnetômetro: ({unpackedData[17]}, {unpackedData[18]}, {unpackedData[19]})")
print(f"   Força 1: {unpackedData[20]}")
print(f"   Força 2: {unpackedData[21]}")

print(f"Instante 3:")
print(f"   Acelerômetro: ({unpackedData[22]}, {unpackedData[23]}, {unpackedData[24]})")
print(f"   Giroscópio: ({unpackedData[25]}, {unpackedData[26]}, {unpackedData[27]})")
print(f"   Magnetômetro: ({unpackedData[28]}, {unpackedData[29]}, {unpackedData[30]})")
print(f"   Força 1: {unpackedData[31]}")
print(f"   Força 2: {unpackedData[32]}")

print(f"Instante 4:")
print(f"   Acelerômetro: ({unpackedData[33]}, {unpackedData[34]}, {unpackedData[35]})")
print(f"   Giroscópio: ({unpackedData[36]}, {unpackedData[37]}, {unpackedData[38]})")
print(f"   Magnetômetro: ({unpackedData[39]}, {unpackedData[40]}, {unpackedData[41]})")
print(f"   Força 1: {unpackedData[42]}")
print(f"   Força 2: {unpackedData[43]}")

print(f"Instante 5:")
print(f"   Acelerômetro: ({unpackedData[44]}, {unpackedData[45]}, {unpackedData[46]})")
print(f"   Giroscópio: ({unpackedData[47]}, {unpackedData[48]}, {unpackedData[49]})")
print(f"   Magnetômetro: ({unpackedData[50]}, {unpackedData[51]}, {unpackedData[52]})")
print(f"   Força 1: {unpackedData[53]}")
print(f"   Força 2: {unpackedData[54]}")

#------------------Instant 1------------------
ax1 = unpackedData[0]   
ay1 = unpackedData[1]
az1 = unpackedData[2]
force11 = unpackedData[9]
gx = unpackedData[3]
gy = unpackedData[4]
gz = unpackedData[5]

        # time = data['Time (s)'].values
acceleration_x.append(ax1)
acceleration_y.append(ay1)
acceleration_z.append(az1)
force.append(force11)
giroscope_x.append(gx)
giroscope_y.append(gy)
giroscope_z.append(gz)


instants_data.append([ax1, ay1, az1, force11])

#------------------Instatnt 2------------------

ax2 = unpackedData[11]
ay2 = unpackedData[12]
az2 = unpackedData[13]
force12 = unpackedData[20]

# time = data['Time (s)'].values
acceleration_x.append(ax2)
acceleration_y.append(ay2)
acceleration_z.append(az2)
force.append(force12)

instants_data.append([ax2, ay2, az2, force12])

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

instants_data.append([ax3, ay3, az3, force13])

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

instants_data.append([ax4, ay4, az4, force14])

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

instants_data.append([ax5, ay5, az5, force15])



plt.plot(acceleration_x, label='Position')
plt.xlabel('Giroscopio')
plt.title('Aceleração vs Time')
plt.show()



