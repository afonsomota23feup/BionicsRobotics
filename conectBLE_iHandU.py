import asyncio
import struct
from bleak import BleakClient, BleakScanner

import matplotlib.pyplot as plt

DATA_LENGTH = 220 # 4 bytes for each of the 54 values
data_points = []

#------------USAR ESTA PRIMEIRO----------------
#esta é a conexão simples, que guarda os dados raw
async def callback(sender, data):
    data_points.append(data)
    #isto é para organizar os dados caso eles vejam todos seguidos, descomentem se isso acontecer
    #processed_values = process_data(data)

def process_data(data):
    return struct.unpack('<' + 'f' * 54, data)


#esta funcao é o que descompacta os dados, temos de tentar perceber como é
# eles estão a ser enviados para conseguirmos descompactar
# a funcao de simples é a que guarda os dados raw, corram essa para conseguirmos
#decifrar o que nos é enviado 

# async def callback(sender, data):
#     if isinstance(data, str):
#         data = bytes.fromhex(data)
#     if len(data) == DATA_LENGTH:
#         values = struct.unpack('<' + 'f' * 54, data)
#         print(f"First value: {values[0]}")
#         data_points.append(values)
#         processed_values = process_data(data)
#         print(f"Processed values: {processed_values}")

# def process_data(data):
#     return struct.unpack('<' + 'f' * 54, data)

async def connect_to_device(device_id, device_uuid):
    #print all the discover devices
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        
    #connect to the device
    async with BleakClient(device_id) as client:
        try:
            await client.connect()
            #conecta se ao dispositivo
            print(f"Connected to device: {device_id}")

            # Começa o envio dos dados 
            await client.start_notify(device_uuid, callback)

            # Coleta dados por 60 segundos
            await asyncio.sleep(60)

        except Exception as e:
            print(f"Failed to connect to device: {device_uuid}, Error: {e}")



async def main():
    device_id = "60658457-ED22-63A5-86C6-0A3297A1D188"
    device_uuid = "6f30b86e-bb28-48a6-b68d-4ae2e60e512a"

    await asyncio.gather(connect_to_device(device_id, device_uuid))

    # save the data in a file
    with open("data.txt", "w") as f:
        for data in data_points:
            f.write(str(data) + "\n")


asyncio.run(main())

#correr varias vezes de modo a guardar os ficheiros de data com nomes diferentes e na ordem certa
#Enquanto corremos, temos de gravar ao mesmo tempo para perceber que dado é que corresponde a qual coisa
#Quando percebermos que esta a funcionar, descomentar o código acima
#Perguntar ao afonso se é para colocar o codigo que esta, como comentário(???)
