import asyncio
from bleak import BleakScanner, BleakClient
import struct

raw_data_points = []
converted_data_points = []
instants_data = []



def callback(sender: int, data: bytearray):
    print(f"Received data from {sender}: {data}")
    raw_data_points.append(data)

def process_data_to_robot():

    for line in converted_data_points:
        divided_line = [line[i:i+11] for i in range(0, len(line), 11)]
        # do something with the divided line
        # e.g. print each instant
        for instant in divided_line:
            print(instant)
    


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
            
            unpackedData = struct.unpack('55f', data[:220])  # 55 unpackedData no total, 4 bytes cada
            converted_data_points.append(unpackedData)

            ax1 = unpackedData[0]
            ay1 = unpackedData[1]
            az1 = unpackedData[2]
            force11 = unpackedData[9]

            instants_data.append([ax1, ay1, az1, force11])

            ax2 = unpackedData[11]
            ay2 = unpackedData[12]
            az2 = unpackedData[13]
            force12 = unpackedData[20]

            instants_data.append([ax2, ay2, az2, force12])

            ax3 = unpackedData[22]
            ay3 = unpackedData[23]
            az3 = unpackedData[24]
            force13 = unpackedData[31]

            instants_data.append([ax3, ay3, az3, force13])

            ax4 = unpackedData[33]
            ay4 = unpackedData[34]
            az4 = unpackedData[35]
            force14 = unpackedData[42]

            instants_data.append([ax4, ay4, az4, force14])

            ax5 = unpackedData[44]
            ay5 = unpackedData[45]
            az5 = unpackedData[46]
            force15 = unpackedData[53]

            instants_data.append([ax5, ay5, az5, force15])
                            

        # save the data in a file
            with open("dataTest.txt", "w") as f:
                for data in raw_data_points:
                    f.write(str(data) + "\n")
            await asyncio.sleep(1)  # pause for a second before reading again

asyncio.run(main())