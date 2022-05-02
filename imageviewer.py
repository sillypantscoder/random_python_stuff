import pygame
import sys
from aspectscale import aspect_scale
import tkinter as tk
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

filename = sys.argv[1]
img = pygame.image.load(filename)

screensize = [*img.get_size()]
if screensize[0] > screen_width: screensize[0] = screen_width
if screensize[1] > screen_height: screensize[1] = screen_height
screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
pygame.display.set_caption(f"Image Viewer ({filename} {img.get_width()}x{img.get_height()})")

running = True
c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			screensize = [*event.size]
			screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
	screen.fill((0, 0, 0))
	screen.blit(aspect_scale(pygame, img, *screensize), (0, 0))
	pygame.display.flip()
	c.tick(60)
