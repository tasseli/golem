import sys, pygame
from pygame.locals import *
import pygcurse
import numpy as np
pygame.init()

mapwidth, mapheight = 80, 40
win = pygcurse.PygcurseWindow(mapwidth, mapheight)
win.autoupdate = False
cave = np.ones((mapwidth, mapheight))

def erode(x, y):
    cave[x, y] = 0
    for neighbor in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
        if 0 < neighbor[0] < mapwidth-1 and 0 < neighbor[1] < mapheight-1 and cave[neighbor] == 1 and np.random.randint(4) == 0:
            erode(neighbor[0], neighbor[1])

def create_rooms_mikae1():
    #randomize amount of rooms
	#draw first room
	#while there's room left, attempt to draw more rooms up to amount
	#connect rooms with corridors

create_rooms_mikae1()

class Creature():
    def __init__(self):
        self.char = '@'
        self.x = 0
        self.y = 0

    def move(self, x, y):
        if cave[self.x+x, self.y+y] == 0:
            self.y += y
            self.x += x


player = Creature()
while cave[player.x, player.y] != 0:
    player.x= np.random.randint(mapwidth)
    player.y = np.random.randint(mapheight)

def draw():
    win.setscreencolors(None, 'black', clear=True)
    for i in range(mapwidth):
        for j in range(mapheight):
            if cave[i,j] == 1:
                win.putchars(' ', x=i, y=j, bgcolor='white')
    win.putchars(player.char, x=player.x, y=player.y, 
                 bgcolor='black', fgcolor='white')
    win.update()

draw()
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player.move(0, -1)
            if event.key == K_DOWN:
                player.move(0, 1)
            if event.key == K_LEFT:
                player.move(-1, 0)
            if event.key == K_RIGHT:
                player.move(1, 0)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            draw()
