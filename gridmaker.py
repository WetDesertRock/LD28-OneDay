#Copyright 2013 WetDesertRock
#
#     This file is part of Before Night Falls.
# 
#     Before Night Falls is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Before Night Falls is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Before Night Falls.  If not, see <http://www.gnu.org/licenses/>.

import sys

import pygame

from consts import *
from worldio import *
from gameClasses import World

try:
    gs = int(sys.argv[1])
    world = World(gs,None,None,100)
except ValueError:
    world = readWorld(sys.argv[1],World)

pygame.display.init()
screen = pygame.display.set_mode((576, 576))
Clock = pygame.time.Clock()

running = True

while running:
    Clock.tick(60)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
        
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        
        elif event.key == pygame.K_q:
            stime = time.time()
            pygame.image.save(screen, "Screenshot_%d.png" % stime)
            print "Wrote Screenshot_%d.png" % stime
        
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x,y = event.pos
        x /= world.gridsize
        y /= world.gridsize
        if world.grid[x][y] == MAT_SOLID:
            mat = MAT_EMPTY
        else:
            mat = MAT_SOLID
        
        world.grid[x][y] = mat
        
    world.draw(screen)
    
    pygame.display.update()

print writeWorld(world)