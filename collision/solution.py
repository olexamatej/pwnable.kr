# Target hashcode
hex_hash_code = "0x21DD09EC"
dec_hash_code = int(hex_hash_code, 16)  # 568,134,124

# Divide the hashcode into 5 parts
a = dec_hash_code // 5  # 113,626,824
e = dec_hash_code - (a * 4)  # 113,626,828

# Convert to little-endian bytes
a_bytes = a.to_bytes(4, byteorder='little')  # \xc8\xce\xc5\x06
e_bytes = e.to_bytes(4, byteorder='little')  # \xcc\xce\xc5\x06

# Construct the payload
payload = a_bytes * 4 + e_bytes

# Print the payload for use in the command
print(payload)