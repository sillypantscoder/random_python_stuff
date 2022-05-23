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

if __name__ == "__main__":
	chart = BarChart({"a": 1, "b": 3, "c": 2, "d": 6, "e": 4, "f": 5})
	import ui
	ui.pygame.font.init()
	ui.init(ui.pygame.display.set_mode([500, 500], pygame.RESIZABLE), font)
	u = ui.UI()
	u.add(ui.Header("Bar Chart"))
	u.add(ui.Image(chart.draw(width=500)))
	u.add(ui.Button("Close"))
	ui.uimenu(u)