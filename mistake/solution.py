# Implementing the same XOR function from mistake.c
def xor(s, xor_key):
    return ''.join(chr(ord(c) ^ xor_key) for c in s)

# Random 10-character string
s = "mamradvlak"
xor_key = 0x01

# XOR the string
result = xor(s, xor_key)

# Print the original and XORed strings
print("Original input:", s)
print("XORed input:   ", result)
