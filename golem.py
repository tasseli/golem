import sys, pygame
from pygame.locals import *
import pygcurse
import numpy as np
pygame.init()

mapwidth, mapheight = 80, 40
win = pygcurse.PygcurseWindow(mapwidth, mapheight)
win.autoupdate = False
cave = np.ones((mapwidth, mapheight))

def create_rooms_recursive():
    roomcenters = []
    def binroom(corners, axis):
        #print(repr(corners))
        if np.random.randint(5) < 4 and corners[axis+2] - corners[axis] > 7:
            lim = np.random.randint(corners[axis]+2, corners[axis+2]-2)
            newax = int(not axis)
            newcors1 = [0, 0, 0, 0]
            newcors2 = [0, 0, 0, 0]
            newcors1[newax], newcors1[newax+2] = corners[newax], corners[newax+2]
            newcors1[axis], newcors1[axis+2] = corners[axis], lim
            newcors2[newax], newcors2[newax+2] = corners[newax], corners[newax+2]
            newcors2[axis], newcors2[axis+2] = lim+1, corners[axis+2]
            binroom(newcors1, newax)
            binroom(newcors2, newax)
        else:
            #print('rageg')
            x1 = np.random.randint(corners[0], (corners[2] + corners[0])/2)
            x2 = np.random.randint((corners[2] + corners[0])/2, corners[2])
            y1 = np.random.randint(corners[1], (corners[3] + corners[1])/2)
            y2 = np.random.randint((corners[3] + corners[1])/2, corners[3])
            cave[x1:x2, y1:y2] = 0
            roomcenters.append([int((x1+x2)/2), int((y1+y2)/2)])

    binroom([1, 1, mapwidth, mapheight], 0)

    def erode(x, y):
        cave[x, y] = 0
        for neighbor in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if 0 < neighbor[0] < mapwidth-1 and 0 < neighbor[1] < mapheight-1 and cave[neighbor] == 1 and np.random.randint(4) == 0:
                erode(neighbor[0], neighbor[1])
    for i in range(mapwidth):
        for j in range(mapheight):
            if cave[i,j] == 0:
                erode(i, j)

    roomsconnected = np.zeros(len(roomcenters))
    roomsconnected[np.random.randint(len(roomcenters))] = 1
    while not roomsconnected.all():
        i = np.random.choice(np.where(1 - roomsconnected)[0])
        start = roomcenters[i]
        j = np.random.choice(np.where(roomsconnected)[0])
        end = roomcenters[j]
        coords = [start[0], start[1]]
        while not coords == end:
            axis = np.random.randint(2)
            if coords[axis] < end[axis]:
                coords[axis] += 1
            elif coords[axis] > end[axis]:
                coords[axis] -= 1
            cave[coords[0], coords[1]] = 0
        roomsconnected[i] = 1

create_rooms_recursive()

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
