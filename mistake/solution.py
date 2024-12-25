# So the solution to the mistake.c is, that due to operator precedence, 
# this part ` if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0)` 
# will be evaluated incorrectly and puts 0 into fd 

# this will cause that `if(!(len=read(fd,pw_buf,PW_LEN) > 0))` will wait for a input from stdin (fd, which is 0)

# since password is 10 characters long and saved as 'xor'ed input, we can just
# input the same string twice, but one time it will be 'xor'ed 


# implementing same xor function from mistake.c
def xor(s, xor_key):
    return ''.join(chr(ord(c) ^ xor_key) for c in s)

# random string with length of 10 we will use
s = "mamradvlak"
xor_key = 0x01
result = xor(s, xor_key)
# result
print(result)

