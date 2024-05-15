import asyncio
from bleak import BleakScanner, BleakClient
import struct
from datetime import timedelta
from datetime import datetime
import csv
import matplotlib.pyplot as plt


converted_data_points = []
instants_data = []
acceleration_x = []
acceleration_y = []
acceleration_z = []
time = []
force = []



def callback(data: bytearray):
    for i in range(1000):
        # print("O tipo de ficheiro dos dados é", type(data))
        unpackedData = struct.unpack('55f', data[:220])
        timestamp = datetime.now()

        #------------------Instant 1------------------
        ax1 = unpackedData[0]
        ay1 = unpackedData[1]
        az1 = unpackedData[2]
        force11 = unpackedData[9]
        acceleration_x.append(ax1)
        acceleration_y.append(ay1)
        acceleration_z.append(az1)
        force.append(force11)
        timestamp1=timestamp + timedelta(milliseconds=20)
        time.append(timestamp1)

        #------------------Instatnt 2------------------
        ax2 = unpackedData[11]
        ay2 = unpackedData[12]
        az2 = unpackedData[13]
        force12 = unpackedData[20]
        acceleration_x.append(ax2)
        acceleration_y.append(ay2)
        acceleration_z.append(az2)
        force.append(force12)
        timestamp2=timestamp + timedelta(milliseconds=40)
        time.append(timestamp2)

        #------------------Instatnt 3------------------
        ax3 = unpackedData[22]
        ay3 = unpackedData[23]
        az3 = unpackedData[24]
        force13 = unpackedData[31]
        acceleration_x.append(ax3)
        acceleration_y.append(ay3)
        acceleration_z.append(az3)
        force.append(force13)
        timestamp3=timestamp + timedelta(milliseconds=60)
        time.append(timestamp3)

        #------------------Instatnt 4------------------
        ax4 = unpackedData[33]
        ay4 = unpackedData[34]
        az4 = unpackedData[35]
        force14 = unpackedData[42]
        acceleration_x.append(ax4)
        acceleration_y.append(ay4)
        acceleration_z.append(az4)
        force.append(force14)
        timestamp4=timestamp + timedelta(milliseconds=80)
        time.append(timestamp4)

        #------------------Instatnt 5------------------
        ax5 = unpackedData[44]
        ay5 = unpackedData[45]
        az5 = unpackedData[46]
        force15 = unpackedData[53]
        acceleration_x.append(ax5)
        acceleration_y.append(ay5)
        acceleration_z.append(az5)
        force.append(force15)
        timestamp5 = timestamp + timedelta(milliseconds=100)
        
        time.append(timestamp5)

        print(acceleration_x)
        i=i+1

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    device = "84:71:27:AC:20:D2"  # replace with your device's address
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # replace with the UUID of the characteristic you want to read
        characteristic_uuid = "14181dce-eb95-46c5-8431-3b4fe0e0a12d"  
 
        ## imprimir dados primeiros recebidos 

        while client.is_connected:
            print("Connected: {client.is_connected}")
            services = await client.get_services()
            for service in services:
                for characteristic in service.characteristics:
                    if characteristic.uuid == characteristic_uuid:
                        print(characteristic.properties)

            data = await client.start_notify(characteristic_uuid, callback)                            

        # save data to CSV
        dataToSave = zip(time, acceleration_x)
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Acceleration X'])
            writer.writerows(dataToSave)

asyncio.run(main())