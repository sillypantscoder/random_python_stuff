#!/usr/bin/python3

# GETCH ------------------------------------------------------------------------

class _Getch:
	"""Gets a single character from standard input.  Does not echo to the
screen."""
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self): return self.impl()


class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()


getch = _Getch()

# PROGRAM ----------------------------------------------------------------------

import os
import subprocess

def isGameFolder(path):
	try:
		# 1. If it's not a directory, it's not a game folder
		if not os.path.isdir(path):
			return False
		# 2. Must have a .git folder
		if not os.path.isdir(os.path.join(path, ".git")):
			return False
		# 3. Must be by sillypantscoder
		if "sillypantscoder" not in subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=path).decode("utf-8"):
			return False
		# 4. Must have main.py
		if not os.path.isfile(os.path.join(path, "main.py")):
			return False
		# Otherwise:
		return True
	except:
		# Oops
		return False

def getGameFolders(path):
	ret = []
	try:
		for x in os.listdir(path):
			if isGameFolder(os.path.join(path, x)):
				ret.append(x)
			elif os.path.isdir(os.path.join(path, x)):
				ret += getGameFolders(os.path.join(path, x))
	except: pass
	return ret

print(u"\u001b[2J===== GAMES =====")
list_of_games = getGameFolders(os.path.expanduser("~/Documents"))
cursorpos = 0
while True:
	# Writing the games to the screen
	for i in range(len(list_of_games)):
		if i == cursorpos:
			print(u"-> \u001b[7m" + list_of_games[i] + u"\u001b[0m")
		else:
			print("- " + list_of_games[i])
	# Getting the input
	i = getch()
	if i == "\x1b": # Escape sequence
		getch()
		k = getch()
		if k == "A": # Up arrow key
			cursorpos = max(0, cursorpos - 1)
		elif k == "B": # Down arrow key
			cursorpos = min(len(list_of_games) - 1, cursorpos + 1)
	elif i == "\r": # Enter key
		c = os.path.join(os.path.expanduser("~/Documents"), list_of_games[cursorpos])
		subprocess.Popen(["python3", "main.py"], cwd=c, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	elif i == "\x03": # Ctrl+C
		exit()
	# Erasing the games
	for i in range(len(list_of_games)):
		print(u"\r\u001b[1A\r\u001b[2K", end="")
