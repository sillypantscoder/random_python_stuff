#full

import pygame
import subprocess

pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 12)
fontheight = font.render("0", True, (0, 0, 0)).get_height()

text = ["Minecraft", "is fun!"]

rendered = []
for t in text:
    rendered.append(font.render(t, True, (0, 0, 0)))
ret = pygame.Surface((max([x.get_width() for x in rendered]), fontheight * len(rendered)))
ret.fill((255, 255, 255))
for i, r in enumerate(rendered):
    ret.blit(r, (0, i * fontheight))

pygame.image.save(ret, "textgen.png")
subprocess.run(["python3", "imgopen.py", "textgen.png"])
