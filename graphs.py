import pygame
import typing

pygame.font.init()
font = pygame.font.SysFont("monospace", 12)

class BarChart:
	def __init__(self, items: "dict[str, int]"):
		self.items = items
		# items is a dict of {name: value}
	def draw(self, width: int = 100, height: int = 100, yscale = 10) -> pygame.Surface:
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		# Draw the lines
		pygame.draw.line(r, (0, 0, 0), (0, height - 1), (width, height - 1))
		pygame.draw.line(r, (0, 0, 0), (0, 0), (0, height))
		# Draw the bars
		bartexts = []
		cum_x = -10
		for name, value in self.items.items():
			bartexts.append(font.render(name, True, (0, 0, 0)))
			cum_x += 20
			pygame.draw.rect(r, (0, 0, 0), pygame.Rect(cum_x, height - (value * yscale), 10, value * yscale))
			cum_x += bartexts[-1].get_width() - 10
		# Draw the text
		padding = font.render("0", True, (0, 0, 0)).get_height()
		_r = pygame.Surface((width, height + padding))
		_r.fill((255, 255, 255))
		_r.blit(r, (0, 0))
		r = _r.copy()
		cum_x = -10
		for text in bartexts:
			cum_x += 20
			r.blit(text, (cum_x, height + padding - text.get_height()))
			cum_x += text.get_width() - 10
		# Finished!
		return r

class LineChart:
	def __init__(self, items: "list[tuple[int, int]]", drawLines: bool = True, drawPoints: bool = True):
		self.items = items
		# items is a list of (x, y) tuples
		self.drawLines = drawLines
		self.drawPoints = drawPoints
	def draw(self, width: int = 100, height: int = 100, xscale = 10, yscale = 10) -> pygame.Surface:
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		# Draw the lines
		pygame.draw.line(r, (0, 0, 0), (0, height - 1), (width, height - 1))
		pygame.draw.line(r, (0, 0, 0), (0, 0), (0, height))
		# Draw the points, if needed
		convertPoint = lambda x, y: (x * xscale, height - y * yscale)
		if self.drawPoints:
			for x, y in self.items:
				pygame.draw.circle(r, (0, 0, 0), convertPoint(x, y), 3)
		# Draw the lines, if needed
		if self.drawLines:
			for i in range(len(self.items) - 1):
				pygame.draw.line(r, (0, 0, 0), convertPoint(*self.items[i]), convertPoint(*self.items[i + 1]), 1)
		# Finished!
		return r

if __name__ == "__main__":
	import ui
	ui.pygame.font.init()
	ui.init(ui.pygame.display.set_mode([500, 500], pygame.RESIZABLE), font)
	# BAR CHART DEMO
	chart = BarChart({"a": 1, "b": 3, "c": 2, "d": 6, "e": 4, "f": 5, "hi there": 4, "z": 3})
	u = ui.UI()
	u.add(ui.Header("Bar Chart"))
	u.add(ui.Image(chart.draw(width=500)))
	u.add(ui.Button("Next"))
	ui.uimenu(u)
	# LINE CHART DEMO
	chart = LineChart([(x, 2 * x) for x in range(10)])
	u = ui.UI()
	u.add(ui.Header("Line Chart"))
	u.add(ui.Image(chart.draw(width=500, xscale=20, yscale=5)))
	u.add(ui.Button("Next"))
	ui.uimenu(u)
	# POINT CHART DEMO
	chart = LineChart([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)], drawLines=False, drawPoints=True)
	u = ui.UI()
	u.add(ui.Header("Point Chart"))
	u.add(ui.Image(chart.draw(width=500, xscale=20, yscale=5)))
	u.add(ui.Button("Exit"))
	ui.uimenu(u)