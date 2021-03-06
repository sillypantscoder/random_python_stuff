#takes

import pygame
import random
import subprocess
import sys
import math

def chop(i: pygame.Surface) -> pygame.Surface:
	"""Chops out a section of the image"""
	r = i.get_rect()
	return pygame.transform.chop(i, pygame.Rect(random.randint(0, r.right // 2), random.randint(0, r.bottom // 2), random.randint(0, r.right // 2), random.randint(0, r.bottom // 2)))

def flip(i: pygame.Surface) -> pygame.Surface:
	"""Flips the image horizontally and vertically"""
	return pygame.transform.flip(i, True, True)

def rotate(i: pygame.Surface) -> pygame.Surface:
	"""Rotates the image"""
	b = i.copy()
	b.set_at((0, 0), (0, 0, 0))
	r = pygame.transform.rotate(b, random.randint(0, 360))
	b = pygame.Surface(r.get_size())
	b.fill((0, 0, 0))
	b.blit(r, (0, 0))
	return b

def roll(i: pygame.Surface) -> pygame.Surface:
	"""Rolls the image by a random amount"""
	r = pygame.Surface(i.get_size())
	offset = (random.randint(0, i.get_width() // 2), random.randint(0, i.get_height() // 2))
	r.blit(i, offset)
	r.blit(i, (offset[0] - i.get_width(), offset[1]))
	r.blit(i, (offset[0], offset[1] - i.get_height()))
	r.blit(i, (offset[0] - i.get_width(), offset[1] - i.get_height()))
	return r.copy()

def negate(i: pygame.Surface) -> pygame.Surface:
	"""Negates the image"""
	r = pygame.Surface(i.get_size())
	r.fill((255, 255, 255))
	r.blit(i, (0, 0), special_flags=pygame.BLEND_SUB)
	return r

def addborder(i: pygame.Surface) -> pygame.Surface:
	"""Adds a randomly colored, randomly sized border to the image"""
	s = random.randint(2, 20)
	r = pygame.Surface((i.get_width() + s + s, i.get_height() + s + s))
	r.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	r.blit(i, (s, s))
	return r

def addline(i: pygame.Surface) -> pygame.Surface:
	"""Adds a line to the image"""
	r = i.copy()
	frompos = (random.randint(0, r.get_width()), random.randint(0, r.get_height()))
	topos = (random.randint(0, r.get_width()), random.randint(0, r.get_height()))
	pygame.draw.line(r, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), frompos, topos, random.randint(1, 20))
	return r

def negate_random(i: pygame.Surface) -> pygame.Surface:
	"""Randomly negates the red, green, or blue channel of the image"""
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
	"""Moves some pixels up"""
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

def highlight(i: pygame.Surface) -> pygame.Surface:
	"""Takes light areas of the image and darkens them"""
	r = i.copy()
	for x in range(r.get_width()):
		for y in range(r.get_height()):
			this = r.get_at((x, y))
			if (this[0] + this[1] + this[2]) / 3 > 128: f = lambda x: x // 2
			else: f = lambda x: x * 2
			cf = lambda x: min(255, max(0, f(x)))
			this = [cf(this[0]), cf(this[1]), cf(this[2])]
			r.set_at((x, y), this)
	return r

def mist(i: pygame.Surface) -> pygame.Surface:
	"""Adds mist to the image"""
	r = i.copy()
	for x in range(r.get_width()):
		for y in range(r.get_height()):
			this = r.get_at((x, y))
			shift = (random.randint(0, 255), random.randint(0, 255))
			r.set_at((x + shift[0], y + shift[1]), this)
	return r

def swirl(i: pygame.Surface) -> pygame.Surface:
	"""Swirls the image"""
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

def amplify(i: pygame.Surface) -> pygame.Surface:
	"""Takes dark areas of the image and makes them brighter"""
	r = i.copy()
	for x in range(i.get_width()):
		for y in range(i.get_height()):
			pixel = i.get_at((x, y))
			if pixel[0] < 127: pixel[0] = 127 - pixel[0]
			if pixel[1] < 127: pixel[1] = 127 - pixel[1]
			if pixel[2] < 127: pixel[2] = 127 - pixel[2]
			r.set_at((x, y), pixel)
	return r

def pixel_lines(i: pygame.Surface) -> pygame.Surface:
	"""Pixelates the image, then draws lines"""
	scale = random.randint(4, 10)
	r = pygame.transform.scale(i, (i.get_width() // scale, i.get_height() // scale))
	currentPixel = [random.randint(0, r.get_width() - 1), random.randint(0, r.get_height() - 1)]
	lastPixel = r.get_at(currentPixel)
	for x in range(50):
		if random.random() < 0.5:
			# Horizontal
			add = random.randint(0, r.get_width())
			for y in range(abs(add)):
				currentPixel[0] += add // abs(add)
				currentPixel[0] %= r.get_width()
				currentPixel[1] %= r.get_height()
				#prev = r.get_at(currentPixel)
				r.set_at(currentPixel, lastPixel)
				#lastPixel = prev
		else:
			# Vertical
			add = random.randint(0, r.get_width())
			for y in range(abs(add)):
				currentPixel[1] += add // abs(add)
				currentPixel[0] %= r.get_width()
				currentPixel[1] %= r.get_height()
				#prev = r.get_at(currentPixel)
				r.set_at(currentPixel, lastPixel)
				#lastPixel = prev
	return pygame.transform.scale(r, (i.get_width(), i.get_height()))

def deform(i: pygame.Surface) -> pygame.Surface:
	"""Deforms the image using a twin dragon curve"""
	def roll(i: pygame.Surface, offset: "tuple[int, int]") -> pygame.Surface:
		"""Rolls the image by some number of pixels"""
		r = pygame.Surface(i.get_size())
		r.blit(i, offset)
		r.blit(i, (offset[0] - i.get_width(), offset[1]                 ))
		r.blit(i, (offset[0]                , offset[1] - i.get_height()))
		r.blit(i, (offset[0] + i.get_width(), offset[1]                 ))
		r.blit(r, (offset[0]                , offset[1] + i.get_height()))
		return r.copy()
	# SETUP
	img_width, img_height = i.get_size()
	num_bands = 4
	shift_by = img_width // 8
	shift_vertical = True
	# EDITING
	for iteration in range(50):
		# 1. Shift the image
		if not shift_vertical:
			band_height = img_height / num_bands
			bands = [i.subsurface(pygame.Rect(0, t * band_height, img_width, band_height)) for t in range(num_bands)]
			shiftedbands: "list[pygame.Surface]" = []
			#u.add(ui.Header("Bands"))
			sh = 1
			for i in bands:
				shiftedbands.append(roll(i, (shift_by * sh, 0)))
				sh *= -1
				#u.add(ui.Image(i))
			#u.add(ui.Header("Rolled Image"))
			#for i in shiftedbands:
				#u.add(ui.Image(i))
				#u.add(ui.Spacer(10))
			i = pygame.Surface((img_width, img_height))
			for t in range(num_bands):
				i.blit(shiftedbands[t], (0, t * band_height))
		else:
			band_width = img_width / num_bands
			bands = [i.subsurface(pygame.Rect(t * band_width, 0, band_width, img_height)) for t in range(num_bands)]
			shiftedbands: "list[pygame.Surface]" = []
			#u.add(ui.Header("Bands"))
			sh = -1
			for i in bands:
				shiftedbands.append(roll(i, (0, shift_by * sh)))
				sh *= -1
				#u.add(ui.Image(i))
			#u.add(ui.Header("Rolled Image"))
			#for i in shiftedbands:
				#u.add(ui.Image(i))
				#u.add(ui.Spacer(10))
			i = pygame.Surface((img_width, img_height))
			for t in range(num_bands):
				i.blit(shiftedbands[t], (t * band_width, 0))
		# 2. Prepare the image for the next step
		num_bands *= 2
		shift_by //= 2
		shift_vertical = not shift_vertical
		if shift_by == 0:
			break
	return i

transforms = [chop, flip, rotate, roll, negate, addborder, addline, negate_random, shift, highlight, mist, swirl, amplify, pixel_lines, deform]

if __name__ == "__main__":
	inputfilename = sys.argv[1]
	outputfilename = "weird.png"
	print()
	img = pygame.image.load(inputfilename)
	after = img.copy()
	for f in range(10):
		after = random.choice(transforms)(after)
		# Progress bar
		print(u"\u001b[1A\r\u001b[0K" + str(f + 1) + "/" + str(len(transforms)))
	pygame.image.save(after, outputfilename)
	subprocess.Popen(["python3", "imageviewer.py", inputfilename])
	subprocess.run(["python3", "imageviewer.py", outputfilename])
