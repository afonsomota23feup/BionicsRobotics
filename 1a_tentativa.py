import numpy as np
from sklearn.preprocessing import MinMaxScaler
    
def process_data(position):
    # Process the data from the iHandU
    # This will depend on the format of the data sent by the iHandU
    # For example, if the data is the position of the hand, you can use the following:
    speed = np.divide(position, 10)
    distance = np.mod(position, 10)

    return position, speed, distance

def interpret_data(position, speed, distance):
    # Interpret the processed data
    # This will depend on the desired behavior of the robotic arm
    # For example, if the position is the x-axis position of the hand, you can use the following:
    if position[0] > 0:
        action_x = "Move right"
        distance_level_x = distance*0.2
    elif position[0] < 0:
        action_x = "Move left"
        distance_level_x = distance*0.2*(-1)
    else:
        action_x = "x Stay still"
        distance_level_x = 0
        
    if position[1] > 0:
        action_y = "Move front"
        distance_level_y = distance*0.2
    elif position[1] < 0:
        action_y = "Move back"
        distance_level_y = distance*0.2*(-1)
    else:
        action_y = "y Stay still"    
        distance_level_y = 0
        
    if position[2] > 0:
        action_z = "Move up"
        distance_level_z = distance*0.2
    elif position[2] < 0:
        action_z = "Move down"
        distance_level_z = distance*0.2*(-1)
    else:
        action_z = "z Stay still"
        distance_level_z = 0
        
 #Pelo que percebi aquilo tem um sensor de força. A pessoa ao abrir e fechar a mão podia ser a pinça e neste caso podiamos colocar so abre e fecha

    return action_x, action_y, action_z, distance_level_x, distance_level_y, distance_level_z
    
#Calibrar o iHandU de modo a perceber onde irá ser o zero para podermos criar um referencial apropriado para cada utilizador
#Temos de definir no controlo que o braço andará de 2 em 2 graus ou milimetros e que o fará com a mesma velocidade que a pessoa


# Example usage
data = np.array([1, 0, 0, 0, 0])

position,speed,distance = process_data(data)

# Initialize filter, calibration, and normalization parameters
filter_window = 5
filter_coeff = np.ones(filter_window)/filter_window
calibration_offset = 0
calibration_gain = 1
    
# Filter the data
filtered_data = np.convolve(data, filter_coeff, mode='same')

# Calibrate the data
calibrated_data = (filtered_data - calibration_offset) * calibration_gain

# Crie um objeto MinMaxScaler
normalization_scaler = MinMaxScaler()

# Treine o objeto MinMaxScaler com os dados de entrada
normalization_scaler.fit(calibrated_data.reshape(-1, 1))

# Normalize the data
normalized_data = normalization_scaler.transform(calibrated_data.reshape(-1, 1))

print("Original data: ", data)
print("Filtered data: ", filtered_data)
print("Calibrated data: ", calibrated_data)
print("Normalized data: ", normalized_data)

x, y, z, distance_x, distance_y, distance_z = interpret_data(position, speed, distance)
print(x, y, z, distance_x, distance_y, distance_z)


#Objetivo: É utilizado um iHandU para se perceber qual é o movimento e como é feito pela mão de uma pessoa para conseguir controlar um braço robótico sem estar ligado ao mesmo. Para isso o iHandU deverá enviar os dados via bluetooth para um programa em python que deverá decifrar os dados, processar-los, interpretar-los e ainda controlar o braço robótico. Deste programa será enviada uma mensagem via cabo para o arduino do braço robótico de modo a controlar o braço. Dependendo da velocidade e da distância percorrida pelo iHandU a resposta do braço robótico deverám ser diferente.
