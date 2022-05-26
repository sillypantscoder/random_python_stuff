import sys
import subprocess

if len(sys.argv) < 2:
	print("Usage: python3 bf_bits.py <input>")
	exit(1)

f = open(sys.argv[1], "rb")
i = f.read()
f.close()

bits = []
for byte in i:
	bits.append((byte & 1) / 1)
	bits.append((byte & 2) / 2)
	bits.append((byte & 4) / 4)
	bits.append((byte & 8) / 8)
	bits.append((byte & 16) / 16)
	bits.append((byte & 32) / 32)
	bits.append((byte & 64) / 64)
	bits.append((byte & 128) / 128)
bits = "".join(["1" if b == 1 else "0" for b in bits])

# Next, split the bits into groups of three
groups = []
for i in range(0, len(bits), 3):
	groups.append(bits[i:i + 3])

# Now, convert to BF
bf = ""
for group in groups:
	if group == "000":   bf += ">"
	elif group == "001": bf += "<"
	elif group == "010": bf += "+"
	elif group == "011": bf += "-"
	elif group == "100": bf += "."
	elif group == "101": bf += ","
	elif group == "110": bf += "["
	elif group == "111": bf += "]"

# And call the interpreter
if len(bf) > 20000:
	# too much for the terminal
	print("Too much BF to run in the terminal, truncating...")
	subprocess.call(["python3", "bf_interpreter.py", bf[:20000]])
else:
	subprocess.call(["python3", "bf_interpreter.py", bf])
