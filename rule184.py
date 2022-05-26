#full

import pygame
import random
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def randomStateColor():
	r = round(random.random()) * 255
	return (r, r, r)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([500, 500], pygame.RESIZABLE)
ticks = 0
toScreen = None
shift = 0
def startup():
	global ticks
	global toScreen
	global shift
	screen.fill((255, 255, 255))
	toScreen = pygame.Surface((10000, 1))
	toScreen.fill((255, 255, 255))
	for p in range(toScreen.get_width()):
		toScreen.set_at((p, 0), randomStateColor())
	ticks = screen.get_height()
	shift = 0
startup()

running = True
c = pygame.time.Clock()
while running:
	# EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			# User clicked close button
		elif event.type == pygame.MOUSEBUTTONUP:
			startup()
		elif event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode([event.size[0], 500], pygame.RESIZABLE)
	# SHIFT
	k = pygame.key.get_pressed()
	if k[pygame.K_LEFT]:
		shift += 1
	if k[pygame.K_RIGHT]:
		shift -= 1
	# NEXT FRAME
	if ticks > 0:
		nextFrame = pygame.Surface((toScreen.get_width(), toScreen.get_height() + 1))
		nextFrame.fill((255, 255, 255))
		nextFrame.blit(toScreen, (0, 1))
		# First pixel
		if toScreen.get_at((0, 0))[0] == 255:
			nextFrame.set_at((0, 0), (0, 0, 0))
		else:
			nextFrame.set_at((0, 0), toScreen.get_at((1, 0)))
		# Rest of pixels
		for p in range(1, nextFrame.get_width() - 1):
			if toScreen.get_at((p, 0))[0] == 255:
				nextFrame.set_at((p, 0), toScreen.get_at((p - 1, 0)))
			else:
				nextFrame.set_at((p, 0), toScreen.get_at((p + 1, 0)))
		# Last pixel
		p = nextFrame.get_width() - 1
		if toScreen.get_at((p, 0))[0] == 255:
			nextFrame.set_at((p, 0), toScreen.get_at((p - 1, 0)))
		else:
			nextFrame.set_at((p, 0), (255, 255, 255))
		# Finish
		toScreen = nextFrame
		ticks -= 1
	else:
		c.tick(60)
		if k[pygame.K_LEFT]:
			shift += 3
		if k[pygame.K_RIGHT]:
			shift -= 3
	# SCREEN
	if shift < -(toScreen.get_width() - screen.get_width()): shift = -(toScreen.get_width() - screen.get_width())
	if shift > 0: shift = 0
	screen.fill((255, 255, 255))
	screen.blit(toScreen, (shift, screen.get_height() - toScreen.get_height()))
	barpos = (shift / (screen.get_width() - toScreen.get_width())) * (screen.get_width() - 10)
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(barpos, 0, 10, 10))
	# FLIP
	#c.tick(60)
	pygame.display.flip()

pygame.quit()