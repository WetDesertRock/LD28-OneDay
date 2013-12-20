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

import pygame, time, os, sys

from consts import *
from gameClasses import *
from worldio import *

# pygame.font.init()
# pygame.display.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()                      #initialize pygame

screen = pygame.display.set_mode((576, 700))
Clock = pygame.time.Clock()

running = True
game = Game()

while running and game.running:
    Clock.tick(30)
    events = pygame.event.get()
    extraevents = []
    for event in events:
        handled = False
        if event.type == pygame.QUIT:
            running = False
            handled = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                stime = time.time()
                pygame.image.save(screen, "Screenshot_%d.png" % stime)
                print "Wrote Screenshot_%d.png" % stime
                handled = True
        
        if not handled:
            extraevents.append(event)
    
    game.handleEvents(extraevents)
    
    game.draw(screen)
    
    pygame.display.update()