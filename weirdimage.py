#takes

import pygame
import random
import subprocess
import sys
import math

def chop(i: pygame.Surface) -> pygame.Surface:
	r = i.get_rect()
	return pygame.transform.chop(i, pygame.Rect(random.randint(0, r.right // 2), random.randint(0, r.bottom // 2), random.randint(0, r.right // 2), random.randint(0, r.bottom // 2)))

def flip(i: pygame.Surface) -> pygame.Surface:
	return pygame.transform.flip(i, True, True)

def rotate(i: pygame.Surface) -> pygame.Surface:
	b = i.copy()
	b.set_at((0, 0), (0, 0, 0))
	r = pygame.transform.rotate(b, random.randint(0, 360))
	b = pygame.Surface(r.get_size())
	b.fill((0, 0, 0))
	b.blit(r, (0, 0))
	return b

def roll(i: pygame.Surface) -> pygame.Surface:
	r = pygame.Surface(i.get_size())
	offset = (random.randint(0, i.get_width() // 2), random.randint(0, i.get_height() // 2))
	r.blit(i, offset)
	r.blit(i, (offset[0] - i.get_width(), offset[1]))
	r.blit(i, (offset[0], offset[1] - i.get_height()))
	r.blit(i, (offset[0] - i.get_width(), offset[1] - i.get_height()))
	return r.copy()

def negate(i: pygame.Surface) -> pygame.Surface:
	r = pygame.Surface(i.get_size())
	r.fill((255, 255, 255))
	r.blit(i, (0, 0), special_flags=pygame.BLEND_SUB)
	return r

def addborder(i: pygame.Surface) -> pygame.Surface:
	s = random.randint(2, 20)
	r = pygame.Surface((i.get_width() + s + s, i.get_height() + s + s))
	r.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	r.blit(i, (s, s))
	return r

def addline(i: pygame.Surface) -> pygame.Surface:
	r = i.copy()
	frompos = (random.randint(0, r.get_width()), random.randint(0, r.get_height()))
	topos = (random.randint(0, r.get_width()), random.randint(0, r.get_height()))
	pygame.draw.line(r, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), frompos, topos, random.randint(1, 20))
	return r

def negate_random(i: pygame.Surface) -> pygame.Surface:
	ind = [random.choice([False, False, True]), random.choice([False, False, True]), random.choice([False, False, True])]
	r = i.copy()
	for x in range(r.get_width()):
		for y in range(r.get_height()):
			this = [*r.get_at((x, y))]
			this[0] = 255 - this[0] if ind[0] else this[0]
			this[1] = 255 - this[1] if ind[1] else this[1]
			this[2] = 255 - this[2] if ind[2] else this[2]
			r.set_at((x, y), this)
	return r

def shift(i: pygame.Surface) -> pygame.Surface:
	r = i.copy()
	for x in range(20, r.get_width() - 20):
		for y in range(20, r.get_height() - 20):
			this = i.get_at((x, y))
			w = r.get_width()
			z = (w / 2) ** 2
			shiftby = z - math.pow(x - math.sqrt(z), 2)
			endpos = [x, y - round(shiftby / 5000)]
			endpos[0] += random.choice([-1, 0, 0, 1])
			endpos[1] += random.choice([-1, 0, 0, 1])
			r.set_at(endpos, (this[0], this[1], this[2]))
	return r

def edges(i: pygame.Surface) -> pygame.Surface:
	e = pygame.transform.laplacian(i)
	return e

def contrast(i: pygame.Surface) -> pygame.Surface:
	r = i.copy()
	for x in range(r.get_width()):
		for y in range(r.get_height()):
			this = r.get_at((x, y))
			f = random.choice([lambda x: x // 2, lambda x: x * 2])
			cf = lambda x: min(255, max(0, f(x)))
			this = [cf(this[0]), cf(this[1]), cf(this[2])]
			r.set_at((x, y), this)
	return r

def mist(i: pygame.Surface) -> pygame.Surface:
	r = i.copy()
	for x in range(r.get_width()):
		for y in range(r.get_height()):
			this = r.get_at((x, y))
			shift = (random.randint(0, 255), random.randint(0, 255))
			r.set_at((x + shift[0], y + shift[1]), this)
	return r

def swirl(i: pygame.Surface) -> pygame.Surface:
	img = i.copy()
	col0 = 0.5 * (float(img.get_width())  - 1.0)
	row0 = 0.5 * (float(img.get_height()) - 1.0)
	swirlBy = random.randint(2, 50)
	swirlBy *= 100
	# Compute the swirl.
	for orig_col in range(img.get_width()):
		for orig_row in range(img.get_height()):
			# For each pixel:
			rel_col = float(orig_col) - col0
			rel_row = float(orig_row) - row0
			dist = math.sqrt((rel_col * rel_col) + (rel_row * rel_row))
			angle = (math.pi / float(swirlBy)) * dist
			dest_col = int(rel_col * math.cos(angle) - rel_row * math.sin(angle) + col0)
			dest_row = int(rel_col * math.sin(angle) + rel_row * math.cos(angle) + row0)
			# Plot pixel (dest_x, dest_y) the same color as (orig_x, orig_y) if it's
			# in bounds
			if (dest_col >= 0) and (dest_col < img.get_width()) and \
			(dest_row >= 0) and (dest_row < img.get_height()):
				img.set_at((orig_col, orig_row), i.get_at((dest_col, dest_row)))
	return img

transforms = [chop, flip, rotate, roll, negate, addborder, addline, negate_random, shift, edges, contrast, mist, swirl]

if __name__ == "__main__":
	inputfilename = sys.argv[1]
	outputfilename = "weird.png"
	print()
	img = pygame.image.load(inputfilename)
	after = img.copy()
	for f in range(len(transforms)):
		after = random.choice(transforms)(after)
		# Progress bar
		print(u"\u001b[1A\r\u001b[0K" + str(f + 1) + "/" + str(len(transforms)))
	pygame.image.save(after, outputfilename)
	subprocess.Popen(["python3", "imageviewer.py", inputfilename])
	subprocess.run(["python3", "imageviewer.py", outputfilename])
