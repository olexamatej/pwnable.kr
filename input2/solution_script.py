# %% [markdown]
# ### stage 1
# ```C
# if(argc != 100) return 0;
# if(strcmp(argv['A'],"\x00")) return 0;
# if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
# printf("Stage 1 clear!\n");```

# %%
import sys
from pwn import * 

args = ['A']*100
args[65] = '\x00'
args[66] = '\x20\x0a\x0d'
args[67] = '4444'

# args = ' '.join(sys.argv)
print(args)



# %% [markdown]
# ### stage 2
# ```C
# char buf[4];
# read(0, buf, 4);
# if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
# read(2, buf, 4);
# if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
# printf("Stage 2 clear!\n");```

# %%
import os

stderr_r, stderr_w = os.pipe()

os.write(stderr_w, b'\x00\x0a\x02\xff')
os.close(stderr_w)

# stdin will be written after creating process 


# %% [markdown]
# ### stage 3
# 
# 
# ```C
# if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
# printf("Stage 3 clear!\n");```

# %%
env = {'\xde\xad\xbe\xef': '\xca\xfe\xba\xbe'}

# %% [markdown]
# ### stage 4
# ```C
# FILE* fp = fopen("\x0a", "r");
# if(!fp) return 0;
# if( fread(buf, 4, 1, fp)!=1 ) return 0;
# if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
# fclose(fp);
# printf("Stage 4 clear!\n");
# ```

# %%
with open(b'\x0a', 'w') as file:
    file.write("\x00\x00\x00\x00")

# %% [markdown]
# ### stage 5
# 
# ```C
#  // network
#         int sd, cd;
#         struct sockaddr_in saddr, caddr;
#         sd = socket(AF_INET, SOCK_STREAM, 0);
#         if(sd == -1){
#                 printf("socket error, tell admin\n");
#                 return 0;
#         }
#         
#         saddr.sin_family = AF_INET;
#         saddr.sin_addr.s_addr = INADDR_ANY;
#         saddr.sin_port = htons( atoi(argv['C']) );
#         if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
#                 printf("bind error, use another port\n");
#                 return 1;
#         }
#         listen(sd, 1);
#         int c = sizeof(struct sockaddr_in);
#         cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
#         if(cd < 0){
#                 printf("accept error, tell admin\n");
#                 return 0;
#         }
#         if( recv(cd, buf, 4, 0) != 4 ) return 0;
#         if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
#         printf("Stage 5 clear!\n");
# 
# ```

# %%
import socket

host = 'localhost'
port = 4444

def get_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        s.sendall(b'\xde\xad\xbe\xef')

        print("Data sent!")

# %%
print(args)
p = process(executable='./code', 
		argv=args, 
        stderr=stderr_r,
        env=env
)

p.stdin.write(b'\x00\x0a\x00\xff')
p.stdin.flush()


get_payload()

print(p.recv())
p.close()


