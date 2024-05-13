import struct

# Dados em bytes
data_bytes = bytearray(b'\x00\xe0N\xbf\x00\xf0\x88>\x00\xe0\xd3\xbe\x00R\x99B\x00\xce\xaeA\x00_\x02\xc2\x00\x9f\xbaB \x12kB\x00\x8cRB\x80\xa2/DX\xa8\xa4D\x00hX\xbf\x00@\x85>\x00\x80\xed\xbe\xc0\xb4\xadB\x00e\xfeA\x00\x86\xba\xc1\x00\r\xb1B\xa0\xe4cB\xa0\xf7KB\xf0n/D\xc8t\xa4D\x00\x00R\xbf\x00\xc0]>\x00\xd8\x0c\xbf\xc0\x89\xc9B\x80\x97\x03B\x00\x1d\x8d\xc1\x00\xb2\xa2B \xb7\\B@\x9a@B0=0D\x90\x8e\xa4D\x00\xd8S\xbf\x00\xa0;>\x00X\x11\xbf\xc0\xbe\xd5B\x00\xbd\x1cB\x00VB\xc1\x00\r\xb1B\xe0\x84[B\x80\x95FB\xe0\xd70D\xc8t\xa4D\x008N\xbf\x00\xe0%>\x00\xf02\xbf\x80\x86\xeeB\x80x\x1dB\x00\xd4\xad\xc0\x00\x9f\xbaB\x00UWB\xa0\xd38B\x00?1DX\xa8\xa4D')

# Decodificação de cada float
unpackedData = struct.unpack('55f', data_bytes[:220])  # 55 unpackedData no total, 4 bytes cada

print(unpackedData)

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


data = []

