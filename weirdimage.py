#takes

import pygame
import random
import subprocess
import sys

inputfilename = sys.argv[1]
outputfilename = "weird.png"

def chop(i: pygame.Surface):
	r = i.get_rect()
	return pygame.transform.chop(i, pygame.Rect(random.randint(0, r.right // 2), random.randint(0, r.bottom // 2), random.randint(0, r.right // 2), random.randint(0, r.bottom // 2)))

def flip(i: pygame.Surface):
	return pygame.transform.flip(i, True, True)

def rotate(i: pygame.Surface):
	b = i.copy()
	b.set_at((0, 0), (0, 0, 0))
	r = pygame.transform.rotate(b, random.randint(0, 360))
	b = pygame.Surface(r.get_size())
	b.fill((0, 0, 0))
	b.blit(r, (0, 0))
	return b

def roll(i: pygame.Surface):
	r = pygame.Surface(i.get_size())
	offset = (random.randint(0, i.get_width() // 2), random.randint(0, i.get_height() // 2))
	r.blit(i, offset)
	r.blit(i, (offset[0] - i.get_width(), offset[1]))
	r.blit(i, (offset[0], offset[1] - i.get_height()))
	r.blit(i, (offset[0] - i.get_width(), offset[1] - i.get_height()))
	return r.copy()

def negate(i: pygame.Surface):
	r = pygame.Surface(i.get_size())
	r.fill((255, 255, 255))
	r.blit(i, (0, 0), special_flags=pygame.BLEND_SUB)
	return r

def addborder(i: pygame.Surface):
	s = random.randint(2, 20)
	r = pygame.Surface((i.get_width() + s + s, i.get_height() + s + s))
	r.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	r.blit(i, (s, s))
	return r

print()
img = pygame.image.load(inputfilename)
after = img.copy()
transforms = [chop, flip, rotate, roll, negate, addborder]
for f in range(len(transforms) * 2):
	after = random.choice(transforms)(after)
	# Progress bar
	print(u"\u001b[1A\r\u001b[0K" + str(f + 1) + "/" + str(len(transforms) * 2))

subprocess.run(["python3", "imageviewer.py", inputfilename])
pygame.image.save(after, outputfilename)
subprocess.run(["python3", "imageviewer.py", outputfilename])
