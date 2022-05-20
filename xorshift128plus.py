MASK = 0xFFFFFFFFFFFFFFFF
def hash(state0: int, state1: int) -> int:
	s1 = state0 & MASK
	s0 = state1 & MASK
	s1 ^= (s1 << 23) & MASK
	s1 ^= (s1 >> 17) & MASK
	s1 ^= s0 & MASK
	s1 ^= (s0 >> 26) & MASK
	state1 = s1 & MASK
	return state1

def reduce(states: list) -> int:
	s = states.pop(0)
	for i in states:
		s = hash(s, i)
	return s

def double(input: int) -> list:
	second = hash(input, input)
	third = hash(second, input)
	fourth = hash(second, third)
	return [third, fourth]
	#     ┌─────┐    ┌─────┐   ┌─────┐    ┌─────┐
	#     │     ▼    │     ▼   │     ▼    │     ▼
	# input     second     third     fourth     result
	#     │     ▲    │     ▲   │     ▲          ▲
	#     └─────┴──────────┘   └─────│──────────┘
	#                └───────────────┘

def rand(input: int) -> int:
	return hash(*double(input))

class Random:
	def __init__(self, seed: int = None):
		self.state: list[int] = [seed]
		if seed == None:
			import datetime
			self.state = [int(datetime.datetime.now().timestamp())]
		self.state: list[int] = [self.state[0], hash(self.state[0], self.state[0])]
	def rand(self) -> int:
		self.state = [hash(*self.state), rand(reduce([*self.state, *[rand(x) for x in self.state]]))]
		return self.state[0]
	def _getRandomBits(self, n: int) -> str:
		rawBits = bin(self.rand())[2:]
		if len(rawBits) < n:
			rawBits += self._getRandomBits(n - len(rawBits))
		return rawBits
	def getRandomBits(self, n: int) -> "list[bool]":
		rawBits = self._getRandomBits(n)
		return [x == "1" for x in rawBits[:n]]
	def randint(self, a: int, b: int) -> int:
		return a + self.getRandomBits(b - a).count(True)
	def choice(self, seq: list) -> int:
		return seq[self.randint(0, len(seq) - 1)]
	def random(self) -> float:
		return self.randint(0, 100000) / 100000
		# precision of 1/100000

random = Random()

if __name__ == "__main__":
	print("Random numbers:")
	r = [0 for x in range(10)]
	for i in range(1000):
		r[random.choice(range(10))] += 1
	print(r)
