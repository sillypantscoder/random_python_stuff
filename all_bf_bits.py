import os
import subprocess
import sys

files = os.listdir(".")
my_env = os.environ.copy()
my_env["AUTOINPUT"] = "1"

for f in files:
	if os.path.isfile(f):
		print("File '" + f + "':", end="")
		sys.stdout.flush()
		subprocess.run(["python3", "bf_bits.py", f], env=my_env)
		print()
