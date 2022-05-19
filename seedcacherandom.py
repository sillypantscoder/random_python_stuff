coins = "HTTHTHHTHTHTHHHTHTHTHTHHTHTHTHTHTHTHHHTHHTTTHTHTHTHT"

randomcache = [x == "H" for x in coins]
import random
randomcache = [random.choice([True, False]) for x in range(len(coins))]
class RandomGenerator:
	def __init__(self):
		self.orgcache = [*randomcache]
		self.cache = [*self.orgcache]
	def _getRandomBits(self, n):
		bits = [self.cache.pop(0)]
		if self.cache == []: self.cache = [*self.orgcache]
		if len(bits) < n:
			bits += self._getRandomBits(n - len(bits))
		return bits[:n]
	def getRandomBits(self, n):
		b = self._getRandomBits(n)
		return [c for c in b]
	def randint(self, a: int, b: int) -> int:
		return a + self.getRandomBits(b - a).count(True)
	def choice(self, seq: list) -> int:
		return seq[self.randint(0, len(seq) - 1)]
	def random(self) -> float:
		return self.randint(0, 100000) / 100000
		# precision of 1/100000

random = RandomGenerator()
if __name__ == "__main__":
	d = [0 for x in range(10)]
	for i in range(10000): d[random.choice(range(10))] += 1
	print(d)
