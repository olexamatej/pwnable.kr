# so we know what the answer is
# the issue in original code is that the random number is not seeded and not using any srand() function or so
# so the random number is always the same.

# we can either print it locally or get it from gdb

answer = 0xdeadbeef
random_number = 1804289383

# xor :D 
key = answer ^ random_number
print(f"The key is: {key}")