#full

import pygame
import pygame.camera
import subprocess

pygame.camera.init()

camlist = pygame.camera.list_cameras()
if not camlist: exit()
cam = pygame.camera.Camera(camlist[0],(640,480))
cam.start()
camimg = pygame.Surface((0, 0))

screen = pygame.display.set_mode((640, 480))

running = True
c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pygame.image.save(camimg, "camera_image.png")
			subprocess.run(["python3", "imgopen.py", "camera_image.png"])
	if cam.query_image(): camimg = cam.get_image()
	screen.fill((255, 255, 255))
	screen.blit(camimg, (0, 0))
	pygame.display.flip()
	c.tick(60)
