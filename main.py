import subprocess
import ui
import os

ui.pygame.font.init()
ui.init(ui.pygame.display.set_mode((500, 500)), ui.pygame.font.SysFont(ui.pygame.font.get_default_font(), 30))

def isfull(path):
	if not path.endswith(".py"): return False
	f = open(path, "rb")
	r = f.readline()
	f.close()
	try:
		r = r.decode("utf-8")
	except UnicodeDecodeError:
		return False
	if r == "#full\r\n": return True
	else:
		return False

files = [z for z in os.listdir() if isfull(z)]
s = files[ui.menu("Select Python Project", files)]
subprocess.run(["python3", s])
