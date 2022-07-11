import pygame
import random

# Board status constants
EMPTY = 0
BLACKTILE = 1
WHITETILE = 2

# Set up the board
boardsize = 8
class Board:
	def __init__(self, copy: "Board | None" = None):
		if copy != None:
			self.board = [[copy.board[i][j] for j in range(boardsize)] for i in range(boardsize)]
		else:
			self.board = [[EMPTY for x in range(boardsize)] for y in range(boardsize)]
			# Make 4 initial moves
			self.board[boardsize//2 - 1][boardsize//2 - 1] = BLACKTILE
			self.board[boardsize//2 - 1][boardsize//2] = WHITETILE
			self.board[boardsize//2][boardsize//2 - 1] = WHITETILE
			self.board[boardsize//2][boardsize//2] = BLACKTILE
	def makeMove(self, selfTile, x: int, y: int):
		enemyTile = BLACKTILE if selfTile == WHITETILE else WHITETILE
		self.board[x][y] = selfTile
		# Check for captures
		for offset in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
			currentPos = [x + offset[0], y + offset[1]]
			found = 1
			while True:
				# Check if currentPos is outside board
				if currentPos[0] < 0 or currentPos[0] >= boardsize or currentPos[1] < 0 or currentPos[1] >= boardsize:
					break
				if self.board[currentPos[0]][currentPos[1]] == enemyTile:
					if found == -1:
						self.board[currentPos[0]][currentPos[1]] = selfTile
					currentPos[0] += offset[0] * found
					currentPos[1] += offset[1] * found
				elif self.board[currentPos[0]][currentPos[1]] == selfTile:
					# Capture all tiles inbetween
					found *= -1
					currentPos[0] += offset[0] * found
					currentPos[1] += offset[1] * found
				elif self.board[currentPos[0]][currentPos[1]] == EMPTY:
					break
				# Check if currentPos is original position
				if currentPos[0] == x and currentPos[1] == y:
					break
	def isValidMove(self, selfTile, x: int, y: int):
		# Make sure tile is empty
		if self.board[x][y] != EMPTY:
			return False
		# Copy the board, make the move, and check if the move is valid
		boardCopy = Board(self)
		boardCopy.makeMove(selfTile, x, y)
		boardCopy[x][y] = self[x][y]
		return boardCopy != self
	def getValidMoves(self, selfTile):
		moves = []
		for x in range(boardsize):
			for y in range(boardsize):
				if self.isValidMove(selfTile, x, y):
					moves.append([x, y])
		return moves
	def getScore(self, selfTile):
		score = 0
		for x in range(boardsize):
			for y in range(boardsize):
				if self.board[x][y] == selfTile:
					score += 1
		return score
	def __getitem__(self, key: int):
		return self.board[key]
	def __eq__(self, other):
		if other == None: return False
		return self.board == other.board
BOARD = Board()
turn = BLACKTILE

# Set up the colors and screen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)

scale = 100
screen = pygame.display.set_mode((boardsize * scale, boardsize * scale))

# Set up the AIs and players
def AIGetMove_Random(board: Board, selfTile: int):
	# Get a random move
	validMoves = board.getValidMoves(selfTile)
	return random.choice(validMoves)
def AIGetMove_Best(board: Board, selfTile: int):
	# Get the best move
	validMoves = board.getValidMoves(selfTile)
	bestMove = validMoves[0]
	bestScore = -1
	for move in validMoves:
		boardCopy = Board(board)
		boardCopy.makeMove(selfTile, move[0], move[1])
		boardCopy[move[0]][move[1]] = selfTile
		score = boardCopy.getScore(selfTile)
		if score > bestScore:
			bestScore = score
			bestMove = move
	return bestMove
def AIGetMove_Corners(board: Board, selfTile: int):
	# Get the move closest to the corners
	validMoves = board.getValidMoves(selfTile)
	bestMove = validMoves[0]
	bestScore = -1
	for move in validMoves:
		dist = abs(move[0] - boardsize//2) + abs(move[1] - boardsize//2)
		score = dist
		if score > bestScore:
			bestScore = score
			bestMove = move
	return bestMove

playerBlackAI = None
playerWhiteAI = AIGetMove_Best

# Main loop
running = True
c = pygame.time.Clock()
while running:
	# Check for events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Get the position of the mouse click
			x, y = pygame.mouse.get_pos()
			x //= scale
			y //= scale
			# Move
			if BOARD.isValidMove(turn, x, y):
				BOARD.makeMove(turn, x, y)
				turn = BLACKTILE if turn == WHITETILE else WHITETILE
	# Draw the board
	screen.fill(GREEN)
	for x in range(boardsize):
		for y in range(boardsize):
			pygame.draw.rect(screen, DARKGREEN, pygame.Rect(x * scale, y * scale, scale, scale), scale // 10)
			# Draw hints
			if BOARD[x][y] == EMPTY:
				if BOARD.isValidMove(turn, x, y):
					pygame.draw.circle(screen, BLUE, (x * scale + scale // 2, y * scale + scale // 2), scale // 10)
			if BOARD[x][y] == BLACKTILE:
				pygame.draw.circle(screen, (0, 0, 0), (x * scale + (scale / 2), y * scale + (scale / 2)), 50)
			elif BOARD[x][y] == WHITETILE:
				pygame.draw.circle(screen, (255, 255, 255), (x * scale + (scale / 2), y * scale + (scale / 2)), 50)
	pygame.draw.rect(screen, BLACK if turn == BLACKTILE else WHITE, screen.get_rect(), 10)
	# Handle AI
	if len(BOARD.getValidMoves(turn)) == 0:
		turn = BLACKTILE if turn == WHITETILE else WHITETILE
	else:
		if turn == BLACKTILE:
			if playerBlackAI != None:
				x, y = playerBlackAI(BOARD, BLACKTILE)
				BOARD.makeMove(BLACKTILE, x, y)
				turn = WHITETILE
		elif turn == WHITETILE:
			if playerWhiteAI != None:
				x, y = playerWhiteAI(BOARD, WHITETILE)
				BOARD.makeMove(WHITETILE, x, y)
				turn = BLACKTILE
	# Flip the screen
	c.tick(60)
	pygame.display.flip()