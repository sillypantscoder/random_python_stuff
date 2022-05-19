import hashlib

class RandomGenerator:
	def __init__(self, seed: int = None):
		self.cache = [seed]
		if seed == None:
			import datetime
			self.cache = [int(datetime.datetime.now().timestamp() * 100)]
	def _getRandomBits(self, n):
		h = hashlib.sha256("".join([str(x) for x in self.cache]).encode("utf-8")).hexdigest()
		bits = bin(int(h, 16))[3:]
		self.cache = [x for x in bits]
		if len(bits) < n:
			bits += self._getRandomBits(n - len(bits))
		return bits[:n]
	def getRandomBits(self, n):
		b = self._getRandomBits(n)
		return [c == '1' for c in b]
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
