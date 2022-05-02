#takes

import subprocess
import ui
import os
import sys

filename = sys.argv[1]

ui.pygame.font.init()
ui.init(ui.pygame.display.set_mode((500, 500)), ui.pygame.font.SysFont(ui.pygame.font.get_default_font(), 30))

def isfull(path):
	if not path.endswith(".py"): return False
	f = open(path, "r")
	r = f.readline()
	f.close()
	if r == "#takes\n": return True
	else: return False

files = [z for z in os.listdir() if isfull(z)]
s = files[ui.menu("Select Image Opener File", files)]
subprocess.run(["python3", s, filename])
