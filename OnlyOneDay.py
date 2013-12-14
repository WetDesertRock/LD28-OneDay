import pygame, time

from consts import *
from gameClasses import *
from worldio import *

pygame.display.init()
screen = pygame.display.set_mode((576, 576))
Clock = pygame.time.Clock()

running = True

# world = World(24,(2,2),10)
world = readWorld("First")
curplr = Player(world)
players = [curplr]

# world.grid[5][4] = MAT_SOLID

def moveCurPlayer(d):
    global curplr, players, world
    move_succeeded = curplr.move(d) 
    if not move_succeeded:
        return False
    
    world.tick()
    pygame.display.set_caption(str(world.ticks))
    
    if curplr.isShadow:
        curplr = Player(world)
        players.append(curplr)
    
    for plr in players:
        plr.sync()
    
    return True

while running:
    Clock.tick(60)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
        
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        
        elif event.key == pygame.K_s:
            stime = time.time()
            pygame.image.save(screen, "Screenshot_%d.png" % stime)
            print "Wrote Screenshot_%d.png" % stime
        
        elif event.key == pygame.K_UP:
            moveCurPlayer(D_UP)
        elif event.key == pygame.K_DOWN:
            moveCurPlayer(D_DOWN)
        elif event.key == pygame.K_RIGHT:
            moveCurPlayer(D_RIGHT)
        elif event.key == pygame.K_LEFT:
            moveCurPlayer(D_LEFT)
    
    screen.fill((0,0,0))
    world.draw(screen)
    for plr in players:
        plr.draw(screen,plr is curplr)
    
    pygame.display.update()