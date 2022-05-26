from getch import getch
import random
from sys import stdout, argv
from os import environ

input_string = "".join([random.choice("+-<>.,[]") for x in range(100)])
if len(argv) > 1:
	input_string = argv[1]

tape = [0]
pointerIndex = 0
inputAllowed = True
outputLimit = 5000

def moveLeft():
	global pointerIndex
	pointerIndex -= 1
	if pointerIndex < 0:
		pointerIndex = 0
def moveRight():
	global pointerIndex
	pointerIndex += 1
	if pointerIndex >= len(tape):
		tape.append(0)
def increment():
	global tape
	tape[pointerIndex] += 1
	if tape[pointerIndex] > 1114112:
		tape[pointerIndex] = 1114112
def decrement():
	global tape
	tape[pointerIndex] -= 1
	if tape[pointerIndex] < 0:
		tape[pointerIndex] = 0
def inputChar():
	global tape
	global inputAllowed
	if inputAllowed:
		print(" [input]", end="")
		if environ.get("AUTOINPUT") == "1":
			try: g = input_string[pointerIndex]
			except: g = "!"
		else: g = getch()
		print(u"\u001b[8D\u001b[0K", end="") # clear line
		stdout.flush()
	else: g = "\x04"
	if g == "\x1b": # Escape sequence
		tape[pointerIndex] = 0
	if g == "\x04": # Ctrl+D
		inputAllowed = False
		tape[pointerIndex] = 0
	else:
		tape[pointerIndex] = ord(g)
def outputChar():
	global tape
	global outputLimit
	if outputLimit <= 0:
		print("[!] Output limit reached")
		exit()
	c = chr(tape[pointerIndex])
	if c == u'\u001b':
		c = "ESC"
	print(c, end="")
	outputLimit -= 1
	stdout.flush()

def interpretSection(s: str):
	i = 0
	iters = 0
	while i < len(s):
		char = s[i]
		if char == "+":
			increment()
		elif char == "-":
			decrement()
		elif char == ">":
			moveRight()
		elif char == "<":
			moveLeft()
		elif char == ".":
			outputChar()
		elif char == ",":
			inputChar()
			iters += 100
		elif char == "[":
			if tape[pointerIndex] == 0:
				layers = 1
				while layers > 0:
					i += 1
					if i >= len(s):
						exit()
					if s[i] == "[":
						layers += 1
					elif s[i] == "]":
						layers -= 1
		elif char == "]":
			if tape[pointerIndex] != 0:
				layers = 1
				while layers > 0:
					i -= 1
					if i < 0:
						i = 0
						break
					if s[i] == "]":
						layers += 1
					elif s[i] == "[":
						layers -= 1
		# VISUALIZATION
		#print("<" + "|".join([(f"[{tape[x]}]" if x == pointerIndex else f" {tape[x]} ") for x in range(len(tape))]) + ">")
		i += 1
		iters += 1
		if iters > 10000000:
			print("[!] Infinite Loop... keep going? [y/N]", end="")
			if environ.get("AUTOINPUT") == "1":
				g = "n"
				print(u"\u001b[21D\u001b[0K", end="")
			else:
				g = getch()
				print(u"\u001b[38D\u001b[0K", end="") # clear line
			stdout.flush()
			if g != "y": return
			iters = 0

interpretSection(input_string)
print()
