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
	rooms_to_be_created = np.random.randint(2, 11)
	first_room_center = np.random.randint(2, mapwidth-2), np.random.randint(2, mapheight-2)
	#maximize small starting coordinates between a min value per dimensions and 1, so we're not nulling border row, then minimize the big starting coords so they're not above end.
	#Is there a chance big ones are smaller than small ones? Would it draw too slim rooms per my specs of width 3?
	first_coords = 0,0,0,0
	while (first_coords[3]-first_coords[1] < 3 and first_coords[2]-first_coords[0] < 3):
		first_dimensions = np.random.randint(3, 21), np.random.randint(3, 21) #I should probably check the upper limit values
		first_coords = max(first_room_center[0]-int(first_dimensions[0]/2), 1), max(first_room_center[1]-int(first_dimensions[1]/2), 1), \
			min(first_room_center[0]+int(first_dimensions[0]/2), mapwidth-1), min(first_room_center[1]+int(first_dimensions[1]/2), mapheight-1)
	cave[first_coords[0]:first_coords[2], first_coords[1]:first_coords[3]] = 0
	rooms_created = 1
	for i in range(0, 100):
		room_center = np.random.randint(2, mapwidth-2), np.random.randint(2, mapheight-2)
		dimensions = np.random.randint(3,21), np.random.randint(3,21)
		coords = max(room_center[0]-int(dimensions[0]/2), 1), max(room_center[1]-int(dimensions[1]/2), 1), min(room_center[0]+int(dimensions[0]/2), mapwidth-1), \
			min(room_center[1]+int(dimensions[1]/2), mapheight-1)
		result = np.all(cave[coords[0]:coords[2], coords[1]:coords[3]] == 1)
		if result:
			print("checks out")
			cave[coords[0]:coords[2], coords[1]:coords[3]] = 0
			rooms_created += 1
		if rooms_created == rooms_to_be_created:
			break
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
