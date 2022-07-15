import pygame
import typing

settings = {}

def init(screen, font):
	global settings
	settings = {
		"screen": screen,
		"font": font
	}

def autoinit():
	pygame.font.init()
	init(pygame.display.set_mode([500, 500], pygame.RESIZABLE), pygame.font.SysFont(pygame.font.get_default_font(), 30))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class UIElement:
	"""Base class for an element in a UI. Renders as a 1x1 black pixel."""
	def __init__(self): pass
	def render(self, mouse, width):
		r = pygame.Surface((1, 1))
		r.fill(BLACK)
		return r
	def handleclick(self, pos): pass
	def addclick(self, func): pass
	def __repr__(self): return "UIElement"

class FocasableUIElement(UIElement):
	"""Base class for an element in a UI that can be focused."""
	def __init__(self):
		self.focused = False
	def handleclick(self, pos):
		self.focused = True

class Header(UIElement):
	"""A header for a UI. Renders as a white text against a black background."""
	def __init__(self, text):
		self.text = text
	def render(self, mouse, width):
		retext = settings["font"].render(self.text, True, WHITE)
		r = pygame.Surface((width, retext.get_height()))
		r.fill(BLACK)
		r.blit(retext, (0, 0))
		return r
	def __repr__(self): return f"UIElement (Header \"{self.text}\")"

class Text(UIElement):
	"""A text element. Renders as a white text against a black background. Cannot be clicked."""
	def __init__(self, text):
		self.text = text
	def render(self, mouse, width):
		retext = settings["font"].render(self.text, True, BLACK)
		r = pygame.Surface((width, retext.get_height()))
		r.fill(WHITE)
		r.blit(retext, (0, 0))
		return r
	def __repr__(self): return f"UIElement (Text \"{self.text}\")"

class Option(UIElement):
	"""A clickable text element. Renders as a white text against a black background. When hovered, the text turns white with a black background."""
	def __init__(self, text):
		self.text = text
		self.clickevents = []
	def render(self, mouse, width):
		retext = settings["font"].render(self.text, True, (WHITE if mouse else BLACK))
		r = pygame.Surface((width, retext.get_height()))
		r.fill((BLACK if mouse else WHITE))
		r.blit(retext, (0, 0))
		return r
	def addclick(self, handler):
		self.clickevents.append(handler)
		return self
	def handleclick(self, pos):
		for handler in self.clickevents:
			handler()
	def __repr__(self): return f"UIElement (Option \"{self.text}\")"

class Button(UIElement):
	"""A button. Renders as a white text against a black background. Can be clicked. When hovered, the text turns black with a white background."""
	def __init__(self, text):
		self.text = text
		self.clickevents = []
	def render(self, mouse, width):
		retext = settings["font"].render(self.text, True, (BLACK if mouse else WHITE))
		r = pygame.Surface((width, retext.get_height() + 30))
		r.fill(WHITE)
		pygame.draw.rect(r, BLACK, pygame.Rect(50, 10, width - 100, retext.get_height() + 10), 1 if mouse else 0)
		r.blit(retext, ((width // 2) - (retext.get_width() // 2), 15))
		return r
	def addclick(self, handler):
		self.clickevents.append(handler)
		return self
	def handleclick(self, pos):
		for handler in self.clickevents:
			handler()
	def __repr__(self): return f"UIElement (Button \"{self.text}\")"

class Spacer(UIElement):
	"""A spacer. Renders as a white bar."""
	def __init__(self, height):
		self.height = height
	def render(self, mouse, width):
		r = pygame.Surface((width, self.height))
		r.fill(WHITE)
		return r
	def __repr__(self): return f"UIElement (Spacer)"

class Image(UIElement):
	"""A UI element that displays an image."""
	def __init__(self, image: pygame.Surface):
		self.image = image.copy()
	def render(self, mouse, width):
		return self.image
	def __repr__(self): return f"UIElement (Image {self.image.get_width()}x{self.image.get_height()})"

class KeyboardInput(FocasableUIElement):
	"""A UI element that displays a text box and allows the user to enter text."""
	def __init__(self, text: str, allowedChars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*()-=+[]{}\\|;:'\",.<>/?`~ "):
		super().__init__()
		self.text = text
		self.allowedChars = allowedChars
	def render(self, mouse, width):
		# Render the text box
		retext = settings["font"].render(self.text + ("|" if self.focused else ""), True, BLACK)
		r = pygame.Surface((width - 20, retext.get_height()))
		r.fill(WHITE)
		r.blit(retext, (0, 0))
		# Render the border
		sol = pygame.Surface((width, r.get_height() + 20))
		sol.fill(BLACK)
		if self.focused:
			pygame.draw.rect(sol, (255, 255, 255), (5, 5, width - 10, r.get_height() + 10), 1)
		sol.blit(r, (10, 10))
		return sol
	def __repr__(self): return f"UIElement (KeyboardInput \"{self.text}\")"

class Dropdown(FocasableUIElement):
	"""A UI element that displays a dropdown menu."""
	def __init__(self, options: "list[str]"):
		super().__init__()
		self.options = options
		self.selected = 0
	def getSelected(self):
		return self.options[self.selected]
	def render_all_options(self, width) -> "list[pygame.Surface]":
		optionlist = []
		for item in range(len(self.options)):
			# Render the text box
			retext = settings["font"].render(self.options[item], True, BLACK)
			r = pygame.Surface((width - 20, retext.get_height()))
			r.fill(WHITE)
			r.blit(retext, (0, 0))
			# Render the border
			sol = pygame.Surface((width, r.get_height() + 20))
			sol.fill(WHITE)
			pygame.draw.rect(sol, BLACK, pygame.Rect(0, 0, 10, sol.get_height()))
			sol.blit(r, (10, 10))
			optionlist.append(sol)
		return optionlist
	def render(self, mouse, width):
		# Render the text box
		retext = settings["font"].render(self.getSelected(), True, WHITE)
		r = pygame.Surface((width - 20, retext.get_height()))
		r.fill(BLACK)
		r.blit(retext, (0, 0))
		# Render the border
		sol = pygame.Surface((width, r.get_height() + 20))
		sol.fill(BLACK)
		padding = 10
		arrow = [(padding, padding), (sol.get_height() - (padding * 2), sol.get_height() // 2), (padding, sol.get_height() - padding)]
		if self.focused:
			pygame.draw.rect(sol, WHITE, (5, 5, width - 10, r.get_height() + 10), 1)
			pygame.draw.polygon(sol, WHITE, [rotateC(((sol.get_height() // 4) + (padding // 2), sol.get_height() // 2), p, 90) for p in arrow])
		else:
			# Draw triangle
			pygame.draw.polygon(sol, WHITE, arrow)
		sol.blit(r, (10 + (padding * 1.5), 10))
		# sol is the header
		# Render the options
		if self.focused:
			optionlist = self.render_all_options(width)
			for item in range(len(optionlist)):
				# Extend the surface
				newItem = pygame.Surface((width, sol.get_height() + optionlist[item].get_height()))
				newItem.fill(WHITE)
				newItem.blit(sol, (0, 0))
				newItem.blit(optionlist[item], (0, sol.get_height()))
				sol = newItem.copy()
		return sol
	def handleclick(self, pos):
		super().handleclick(pos)
		# Get the position of the click
		optionlist = self.render_all_options(500)
		y = pos[1] // optionlist[0].get_height()
		if y == 0:
			# clicked on header
			return
		self.selected = y - 1
		self.focused = False
	def __repr__(self): return f"UIElement (Dropdown \"{self.getSelected()}\")"

class UI:
	"""A UI to be drawn to the screen. Contains a list of UIElements."""
	def __init__(self):
		self.items: list[UIElement] = []
		self.scrolloffset = 0
	def add(self, item: UIElement):
		self.items.append(item)
		return self
	def addMultiple(self, items: typing.List[UIElement]):
		for item in items:
			self.add(item)
		return self
	def render(self, mousepos: "tuple[int, int]", mouseclicked: bool) -> pygame.Surface:
		scrn_width, scrn_height = settings["screen"].get_size()
		# Render the items:
		rendered_items = []
		cum_y = 0 - self.scrolloffset
		for item in self.items:
			i = item.render(False, scrn_width)
			if i.get_rect().move(0, cum_y).collidepoint(mousepos):
				i = item.render(True, scrn_width)
			if mouseclicked:
				if i.get_rect().move(0, cum_y).collidepoint(mousepos):
					item.handleclick((mousepos[0], mousepos[1] - cum_y))
				else:
					if isinstance(item, FocasableUIElement):
						item.focused = False
			rendered_items.append(i)
			if i.get_width() > scrn_width:
				scrn_width = i.get_width()
			cum_y += i.get_height()
		# Draw all the items onto the screen
		ret = pygame.Surface((scrn_width, scrn_height))
		ret.fill(WHITE)
		cum_y = 0 - self.scrolloffset
		total_height = 0
		for item in rendered_items:
			ret.blit(item, (0, cum_y))
			cum_y += item.get_height()
			total_height += item.get_height()
		# Fix scroll offset
		if total_height < scrn_height:
			self.scrolloffset = self.scrolloffset // 2
		else:
			if self.scrolloffset < 0:
				self.scrolloffset = self.scrolloffset // 2
			if self.scrolloffset > total_height - scrn_height:
				self.scrolloffset = (total_height - scrn_height) + ((self.scrolloffset - (total_height - scrn_height)) // 2)
		return ret
	def __repr__(self): return f"UI [ {', '.join([str(i) for i in self.items])} ]"

def render_ui(ui: UI):
	"""Renders a UI to the screen, with keyboard input."""
	clicked = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); exit()
			# User clicked close button
		if event.type == pygame.MOUSEBUTTONUP:
			# Detect scrolling
			if event.button in [4, 5]:
				# Scrolling handled later in MOUSEWHEEL
				pass
			elif event.button in [1, 3]:
				# Click or right click
				clicked = True
		if event.type == pygame.VIDEORESIZE:
			settings["screen"] = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				for item in ui.items:
					if isinstance(item, KeyboardInput) and item.focused:
						item.text = item.text[:-1]
			for item in ui.items:
				if isinstance(item, KeyboardInput) and item.focused:
					if event.unicode in item.allowedChars:
						item.text += event.unicode
		if event.type == pygame.MOUSEWHEEL:
			# User is scrolling
			ui.scrolloffset -= event.y * 20
			#print(event.x, event.y)
	m = pygame.mouse.get_pos()
	settings["screen"].blit(ui.render(m, clicked), (0, 0))
	pygame.display.flip()

def menu(header: str, items: "list[str]") -> int:
	"""Displays a menu with the given header and items. Returns the index of the selected item."""
	ui = UI().add(Header(header))
	for i in items:
		if i == "": ui.add(Text(""))
		else: ui.add(Option(i))
	return uimenu(ui) - 1

def listmenu(getitemcallback: "typing.Callable[[function], list[UIElement]]") -> typing.Any:
	"""Displays a UI, with options for each element to return a specific value."""
	ui = UI() # Create the UI
	finished = [False, None] # 1st item stops the mainloop, 2nd item stores the selected item
	def finish(v = None):
		finished[0] = True
		finished[1] = v
	for item in getitemcallback(finish):
		ui.add(item)
	c = pygame.time.Clock()
	while not finished[0]:
		render_ui(ui)
		c.tick(60)
	return finished[1]

def uimenu(ui: UI) -> int:
	"""Displays an already-created UI object, with click handlers."""
	def getitemcallback(finish):
		u: list[UIElement] = [i for i in ui.items] # Create the UI element list
		getclickerfunc = lambda i: (lambda: finish(i))
		index = 0
		for item in u:
			item.addclick(getclickerfunc(index))
			index += 1
		return u
	return listmenu(getitemcallback)
