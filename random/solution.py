# Known values
answer = 0xdeadbeef
random_number = 1804289383  # Predictable random number from unseeded rand()

# Calculate the key
key = answer ^ random_number
print(f"The key is: {key}")