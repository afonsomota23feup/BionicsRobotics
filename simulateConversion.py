import struct

data_bytes = bytearray(b'\x00\xe0N\xbf\x00\xf0\x88>\x00\xe0\xd3\xbe\x00R\x99B\x00\xce\xaeA\x00_\x02\xc2\x00\x9f\xbaB \x12kB\x00\x8cRB\x80\xa2/DX\xa8\xa4D\x00hX\xbf\x00@\x85>\x00\x80\xed\xbe\xc0\xb4\xadB\x00e\xfeA\x00\x86\xba\xc1\x00\r\xb1B\xa0\xe4cB\xa0\xf7KB\xf0n/D\xc8t\xa4D\x00\x00R\xbf\x00\xc0]>\x00\xd8\x0c\xbf\xc0\x89\xc9B\x80\x97\x03B\x00\x1d\x8d\xc1\x00\xb2\xa2B \xb7\\B@\x9a@B0=0D\x90\x8e\xa4D\x00\xd8S\xbf\x00\xa0;>\x00X\x11\xbf\xc0\xbe\xd5B\x00\xbd\x1cB\x00VB\xc1\x00\r\xb1B\xe0\x84[B\x80\x95FB\xe0\xd70D\xc8t\xa4D\x008N\xbf\x00\xe0%>\x00\xf02\xbf\x80\x86\xeeB\x80x\x1dB\x00\xd4\xad\xc0\x00\x9f\xbaB\x00UWB\xa0\xd38B\x00?1DX\xa8\xa4D')

raw_data_points = []
converted_data_points = []
instants_data = []

data = data_bytes  # Define the "data" variable

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
                            
print(instants_data)


