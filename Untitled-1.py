from struct import pack, unpack

packed = pack('fff', -1, -2, -3)
unpacked = unpack('fff', packed)

print("Packed")
print(packed)

print("Unpacked")
print(unpacked) 