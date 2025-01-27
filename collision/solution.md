### Analysis

The challenge involves bypassing a hashing function in the provided C code. The `check_password` function takes a 20-byte input, treats it as an array of 5 integers (4 bytes each), and sums them. If the sum equals the hardcoded `hashcode` (`0x21DD09EC`), the program prints the flag.

### Exploit

We need to craft a 20-byte input such that the sum of its 5 integer components equals `0x21DD09EC` (568,134,124 in decimal).


1. **Divide the Hashcode**:
   - Split `0x21DD09EC` into 5 parts.
   - Since `568,134,124 / 5 = 113,626,824.8`, we use 4 parts of `113,626,824` and 1 part of `113,626,828` to make the total sum correct.

2. **Convert to Bytes**:
   - Convert the integers to their little-endian byte representation.
   - `113,626,824` in hex is `0x06C5CEC8`.
   - `113,626,828` in hex is `0x06C5CECC`.

3. **Construct the Payload**:
   - Repeat `0x06C5CEC8` four times and append `0x06C5CECC` to form the 20-byte input.

### Solution Code

```python
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
```

### Final Command

Run the following command to exploit the program and retrieve the flag:

```bash
./col "$(python3 -c 'print(b"\xc8\xce\xc5\x06" * 4 + b"\xcc\xce\xc5\x06")')"
```