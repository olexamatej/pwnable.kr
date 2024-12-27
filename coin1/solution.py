from pwn import *
def find_counterfeit(p):
    # reading parameters
    params = p.recvline().decode().split()
    # print('params:', params)
    N = int(params[0].split('=')[1])
    C = int(params[1].split('=')[1])

    # initial range of coins to search through
    left = 0
    right = N - 1

    if C == 0:
        p.sendline(str(left).encode())
        result = p.recvline().decode()
        return result.startswith('Correct')
    
    while C > 0:
        C -= 1
        mid = (left + right) // 2

        # weigh coins from left to mid (left half)
        to_weigh = list(range(left, mid + 1))
        expected_weight = len(to_weigh) * 10

        p.sendline(' '.join(map(str, to_weigh)).encode())
        weight = int(p.recvline().decode().strip())

        # binary search logic
        if weight < expected_weight:
            right = mid  
        else:
            left = mid + 1 

        # if left == right, we have found the counterfeit coin
        if left == right:
            p.sendline(str(left).encode())
            result = p.recvline().decode()
            if result.startswith('Correct'):
                return True
            else:
                # send one additional check after confirming the final coin
                p.sendline(str(left).encode())
                result = p.recvline().decode()
                if result.startswith('Correct'):
                    return True

    return False

def main():
    try:
        # best way to do it is change pwnable.kr to localhost, connect to the server and then run the script locally
        # because i dont have fast enough connection :D
        p = remote('pwnable.kr', 9007)
        print(p.recv().decode())
        
        for _ in range(100):  # Need to solve 100 times
            if not find_counterfeit(p):
                print("Failed to find counterfeit within allowed chances")
                break
        print(p.recv())
        p.close()
    except Exception as e:
        print('Error:', e)
        p.close()

if __name__ == "__main__":
    main()