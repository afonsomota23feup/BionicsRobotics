import serial
import time


force= []

def main():
    # Configurar a comunicação serial
    ser = serial.Serial()
    ser.baudrate = 9600

    # Verifique e defina a porta correta
    ser.port = 'COM5' 
    try:
        ser.open()
        print("Serial COM open")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    time.sleep(2)  # Esperar a inicialização da comunicação serial

    def send_movement_vector(x_distance, y_distance, z_distance, force):
        # Construir a string de movimento
        movement_command = f"{x_distance} {y_distance} {z_distance} {force}\n"
        
        # Enviar o comando via serial
        ser.write(movement_command.encode('utf-8'))
        print(f"Sent: {movement_command.strip()}")
        
        
    def real_force(force):
             if force > 1860:
                 if global_force < 14:
                     return 14
                 else:
                     return 0
            
             else: 
                 if global_force > -12:
                     return -12
                 else:
                     return 0
                
    #O valor que seria enviado para esta função seria o valor da força recebido pelo iHandU    
    force_r = real_force(force) #valor recebido do iHandU
    global_force = force_r
    
    # Exemplo de sequência de vetores de movimento (distâncias em cm)
    movement_vectors = [
    [0, 0, 11, 0],
    [-6, 0, 0, 0],
    [0, 0, 0, 14],
    [0, 0, -13, 0],
    [0, -14, 0, 0],
    [0, 0, 6, 0],
    [0, 0, 0, -12],
    ]
        

    # Enviar os vetores de movimento para o Arduino a cada 3 segundos
    for vector in movement_vectors:
        send_movement_vector(*vector)
        time.sleep(3)

    # Fechar a comunicação serial
    ser.close()
    print("Serial COM closed")

if __name__ == "__main__":
    main()
