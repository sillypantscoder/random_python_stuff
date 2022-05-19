#full

import pygame
import pygame.camera
import subprocess
import random
from weirdimage import transforms
import threading
import ui
from aspectscale import aspect_scale

pygame.camera.init()

camlist = pygame.camera.list_cameras()
if not camlist: exit("No cameras detected")
cam = pygame.camera.Camera(camlist[0], (640, 480))
cam.start()
camimg = pygame.Surface((0, 0))
filterimg = pygame.Surface((0, 0))

screensize = [640 * 2, 480]
screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
pygame.display.set_caption("Weird Image (Camera)")

pygame.font.init()
ui.init(screen, pygame.font.SysFont("monospace", 12))
filter = ui.menu("Select Transform", [*[x.__name__ for x in transforms], "", "All"])
if filter > len(transforms):
	filter = False
else:
	filter = transforms[filter]

def filterasync():
	global filterimg
	if filter == False:
		t = transforms.copy()
		random.shuffle(t)
		i = camimg.copy()
		for f in t:
			i = f(i)
			filterimg = i.copy()
	else:
		i = camimg.copy()
		filterimg = filter(i)

running = True
c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if ui.uimenu(ui.UI().add(ui.Header("Select Image")).add(ui.Button("Camera Image")).add(ui.Button("Filtered Image"))) == 1:
				pygame.image.save(camimg, "camera_image.png")
			else:
				pygame.image.save(filterimg, "camera_image.png")
			subprocess.Popen(["python3", "imgopen.py", "camera_image.png"])
		elif event.type == pygame.VIDEORESIZE:
			screensize = [*event.size]
			#screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
			# I sure hope you have Pygame 2.0
	# Get images
	c = pygame.time.Clock()
	while cam.query_image():
		camimg = cam.get_image()
	if threading.active_count() < 2: threading.Thread(target=filterasync, name="filter").start()
	err = True
	while err:
		try:
			screen.fill((255, 255, 255))
			imgsize = aspect_scale(camimg, screensize[0] / 2, screensize[1])
			screen.blit(pygame.transform.scale(camimg, imgsize), (0, 0))
			imgsize = aspect_scale(filterimg, screensize[0] / 2, screensize[1])
			imgsize = pygame.transform.scale(filterimg, imgsize)
			screen.blit(imgsize, (screensize[0] - imgsize.get_width(), 0))
			err = False
		except: err = True
	pygame.display.flip()
	c.tick(60)
