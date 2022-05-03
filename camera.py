#full

import pygame
import pygame.camera
import subprocess
import random
from weirdimage import transforms
import threading

pygame.camera.init()

camlist = pygame.camera.list_cameras()
if not camlist: exit()
cam = pygame.camera.Camera(camlist[0],(640,480))
cam.start()
camimg = pygame.Surface((0, 0))
filterimg = pygame.Surface((0, 0))

screensize = [640 * 2, 480]
screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)

def filterasync():
	global filterimg
	t = transforms.copy()
	random.shuffle(t)
	filterimg = camimg.copy()
	for f in t: filterimg = f(filterimg)

running = True
c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pygame.image.save(filterimg, "camera_image.png")
			subprocess.run(["python3", "imgopen.py", "camera_image.png"])
		elif event.type == pygame.VIDEORESIZE:
			screensize = [*event.size]
			screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
	# Get images
	c = pygame.time.Clock()
	while cam.query_image(): camimg = cam.get_image()
	try:
		screen.fill((255, 255, 255))
		screen.blit(camimg, (0, 0))
		screen.blit(filterimg, (screensize[0] - filterimg.get_width(), 0))
	except: pass
	if threading.active_count() < 2: threading.Thread(target=filterasync, name="filter").start()
	pygame.display.flip()
	c.tick(60)
