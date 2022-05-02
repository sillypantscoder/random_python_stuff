#full

import random
from math import floor

import pygame as pg
import os
from pygame.locals import *

# https://github.com/pygame/pygame/blob/master/examples/aliens.py#L164

pg.init()
size = 500
boardsize = 100
screencellsize = size / (boardsize + 0)  # Need padding?

board = [[False for _ in range(boardsize)] for _ in range(boardsize)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

clock = pg.time.Clock()

stamps = [
    [  # One dot in center
        [False, False, False],
        [False, True, False],
        [False, False, False]
    ],
    [  # Up right glider
        [False, True, False],
        [False, True, True],
        [True, False, True]
    ],
[  # Down left glider
        [True, False, True],
        [True, True, False],
        [False, True, False]
    ],
    [  # Vertical line
        [False, True, False],
        [False, True, False],
        [False, True, False]
    ],
    [  # Block
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]
]
stampsdisplay = """
Choose Stamp:
0 - One dot in center
1 - Up right glider"""
stampnum = 0


def stamp(mode):
    mouse = getmousetilepos()
    for x in range(3):
        for y in range(3):
            if stamps[stampnum][x][y]:
                board[mouse[0] + (y - 1)][mouse[1] + (x - 1)] = mode
                # I don't know why I have to switch the x and y, but it works that way.


def preview_stamp():
    mouse = getmousetilepos()
    for x in range(3):
        for y in range(3):
            if stamps[stampnum][x][y]:
                pg.draw.rect(screen, GRAY, ((mouse[0] + (y - 1)) * screencellsize, (mouse[1] + (x - 1)) *
                                            screencellsize, screencellsize, screencellsize))


def change_stamp():
    global stampnum
    stampnum += 1
    if stampnum >= len(stamps):
        stampnum = 0


def get_cell_state(x, y):
    global board
    count = 0
    for nx in [x-1, x, x+1]:
        for ny in [y - 1, y, y + 1]:
            if nx == x and ny == y:
                continue
            try:
                if board[nx][ny]:
                    count += 1
            except:
                pass
    # print(count, end=" ")
    if board[x][y]:
        return count == 2 or count == 3
    else:
        return count == 3


"""def print_board(b):
    for x in range(boardsize):
        for y in range(boardsize):
            if b[x][y]:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()"""


def getmousetilepos():
    mouse = pg.mouse.get_pos()
    tilex = floor((mouse[0] / size) * boardsize)
    tiley = floor((mouse[1] / size) * boardsize)
    return tilex, tiley


def getlistcopy(ltbc):
    newthing = []
    for a in ltbc:
        newnewthing = []
        for b in a:
            newnewthing.append(b)
        newthing.append(newnewthing)
    return newthing


def update_board():
    global board
    # print_board(board)
    newboard = getlistcopy(board)
    # print_board(newboard)
    for x in range(boardsize):
        for y in range(boardsize):
            # print("{}".format("*" if board[x][y] else "."), end="")
            newboard[x][y] = get_cell_state(x, y)
            # print("{}".format("#" if board[x][y] else "."), end=" ")
        # print()
    board = newboard
    # print_board(newboard)


def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join("data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise FileNotFoundError('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface  # .convert()


def load_sound(file):
    """ because pygame can be be compiled without mixer.
    """
    if not pg.mixer:
        return None
    file = os.path.join("data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


screen = {}


def main():
    global size
    global screen
    # Set the width and height of the screen [width, height]
    screen = pg.display.set_mode((size, size))
    pg.display.set_caption("Game of Life")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                pass
            elif event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    update_board()
                if event.key == K_q:
                    change_stamp()
                if event.key == K_a:
                    for i in range(100):
                        update_board()
                if event.key == K_s:
                    for i in range(500):
                        update_board()
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_z]:
            update_board()
        if pressed_keys[K_r]:
            mouse = getmousetilepos()
            board[mouse[0]][mouse[1]] = random.choice([True, False])
        if pg.mouse.get_pressed()[0]:
            stamp(True)
        if pg.mouse.get_pressed()[2]:
            stamp(False)
        # Update the screen
        screen.fill(WHITE)
        # Background image -------------------------------------------------------------
        # Drawing commands -------------------------------------------------------------
        for x in range(boardsize):
            for y in range(boardsize):
                mouse = getmousetilepos()
                if board[x][y]:
                    pg.draw.rect(screen, BLACK,
                                 (x * screencellsize, y * screencellsize, screencellsize, screencellsize))
                if mouse[0] + 1 == x and mouse[1] + 1 == y:
                    preview_stamp()
        # ------------------------------------------------------------------------------
        pg.display.flip()
        clock.tick(260)


#if __name__ == "__main__":
main()
