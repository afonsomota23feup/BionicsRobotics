import struct

# Função para extrair valores de ponto flutuante de uma faixa de bytes
def extract_float(byte_array, start_byte, end_byte):
    bytes_data = byte_array[start_byte:end_byte + 1]
    float_value = struct.unpack('<f', bytes_data)[0]
    return float_value

# Sequência de bytes fornecida
byte_data = bytearray(b'\x00\x00\x19\xbd\x00\x00m\xbf\x00@\x0f>\x00%\xdf\xc1\x00\x01\xe5\xc1\x80\xcb$\xc2\x90\x90,E\x11\xdb\xe5D\x00\x00\x00\x00`uOD\xc8\x1e\x91D\x00\x00\x08\xbb\x00xc\xbf\x00`9>\x006\xf1\xc1\x00\x12w\xc1\x00\x19a\xc2\x00\xd4\xf8\xc1\xc0\xb4\xdf\xc1\x80o\xf6A\xb0\xdaND\x908\x91D\x00\x00~=\x00`o\xbf\x00 Z>\x80[\r\xc2\x00\x08O@\x00\xe2\x81\xc2\x00h\xbf\xc1\x80\x82\xde\xc1\x003\x01B\x00@ND\xe0\x9d\x90D\x00\xc0\xf9=\x00Hz\xbf\x00`|>\x80~\x1c\xc2\x004\x9e\xc0\x80\xb0g\xc2\x00\x8c\xd2\xc1@P\xdd\xc1\x80o\xf6Ap\x0cNDh\xe9\x8fD\x00\xc0U>\x00\\\x8f\xbf\x00\xc0\xc8=\x80\x90\x19\xc2\x00k\x00\xc2\x00s\xd2\xc1\x00D\xac\xc1\x00\xb0\xe5\xc1\xc0\x0f\xeeA\xe0\xd8MD0\x03\x90D')

# Definindo as constantes
num_instants = 5
data_per_instant = 44  # Alterado de 45 para 44 para corrigir a lógica

# Iterando sobre cada instante
for i in range(num_instants):
    print(f"Instante {i+1}:")
    # Iterando sobre cada sensor
    for j in range(5):
        print(f"Sensor {j+1}:")
        # Iterando sobre cada elemento
        for k in range(3):
            start_byte = i * data_per_instant + j * 44 + k * 4  # Corrigido de 44 para 4
            end_byte = start_byte + 3
            float_value = extract_float(byte_data, start_byte, end_byte)
            print(f"   Elemento {k+1}: {float_value}")

    # Corrigindo o índice de início e fim para o último elemento do sensor 5
    start_byte = i * data_per_instant + 4 * 44 + 3 * 4
    end_byte = start_byte + 3
    float_value = extract_float(byte_data, start_byte, end_byte)
    print(f"   Elemento 4: {float_value}")
