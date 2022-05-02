#full

import pygame
import os
import subprocess
import ui

pygame.font.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
fontheight = font.render("0", True, (0, 0, 0)).get_height()
imgs = [z for z in os.listdir() if z.endswith(".png") or z.endswith(".jpg") or z.endswith(".jpeg")]
screen = pygame.display.set_mode((500, 500))

ui.init(screen, font)

selectedImage = ui.menu("Select Image File", imgs)
subprocess.run(["python3", "weirdimage.py", imgs[selectedImage]])
