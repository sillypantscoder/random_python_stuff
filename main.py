import subprocess
import ui
import os

ui.pygame.font.init()
ui.init(ui.pygame.display.set_mode((500, 500)), ui.pygame.font.SysFont(ui.pygame.font.get_default_font(), 30))

files = [z for z in os.listdir() if z.endswith(".py")]
s = files[ui.menu("Select Python Project", files)]
subprocess.run(["python3", s])
