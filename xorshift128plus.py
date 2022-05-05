MASK = 0xFFFFFFFFFFFFFFFF
def xs128p(state0, state1):
	s1 = state0 & MASK
	s0 = state1 & MASK
	s1 ^= (s1 << 23) & MASK
	s1 ^= (s1 >> 17) & MASK
	s1 ^= s0 & MASK
	s1 ^= (s0 >> 26) & MASK 
	state1 = s1 & MASK
	return state1

if __name__ == "__main__":
	print(xs128p(123, 123))
