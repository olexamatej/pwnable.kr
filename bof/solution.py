import sys

sys.stdout.buffer.write(b'\\x01'*52+b'\\xbe\\xba\\xfe\\xca' + b'\\n')

