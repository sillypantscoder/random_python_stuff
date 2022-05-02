# Pygame platformer

#import subprocess
#from types import prepare_class
import pygame
#import requests
import random
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([480, 360], pygame.RESIZABLE)
#screen = pygame.display.set_mode([1000, 1000])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
balls = []
def newBall():
	balls.append({
		"pos": [screen.get_width() / 2, screen.get_height() / 2],
		"v": [random.randint(-10, 10), 0],
		"color": (random.randint(0, 25) * 10, random.randint(0, 25) * 10, random.randint(0, 25) * 10)
	})
for i in range(30):
	newBall()

def hitbox(b):
	return pygame.Rect(int(b["pos"][0]) - 10, int(b["pos"][1]) - 10, 20, 20)

running = True
c = pygame.time.Clock()
while running:
	# EVENTS ----------------------------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			# User clicked close button
		elif event.type == pygame.MOUSEBUTTONUP:
			for i in range(50):
				newBall()
		elif event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode(event.dict["size"], pygame.RESIZABLE)
	pos = pygame.mouse.get_pos()
	# BALLS
	for b in balls:
		b["pos"][0] += b["v"][0]
		b["pos"][1] += b["v"][1]
		if not screen.get_rect().contains(hitbox(b)):
			b["v"][1] = random.randint(0, 4)
			b["v"][0] = random.randint(-4, 4)
		if hitbox(b).colliderect(hitbox({"pos": pos})):
			b["v"][1] += screen.get_height() / 300
		touching = False
		for o in balls:
			if b == o:
				continue
			if hitbox(b).colliderect(hitbox(o)):
				touching = True
				break
		if not touching:
			b["v"][1] -= 0.1
		# Sanity check
		if b["pos"][1] < 0:
			b["pos"][1] = 0
		if b["pos"][0] < 0:
			b["pos"][0] = 0
		if b["pos"][1] > screen.get_height():
			balls.remove(b)
		if b["pos"][0] > screen.get_width():
			b["pos"][0] = screen.get_width()
	# SCREEN
	screen.fill(WHITE)
	for b in balls:
		pygame.draw.circle(screen, b["color"], (int(b["pos"][0]), int(b["pos"][1])), 10)
	# FLIP -----------------------------------------------
	c.tick(60)
	pygame.display.flip()

# Done!
pygame.quit()