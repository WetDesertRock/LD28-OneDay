import pygame, time

from consts import *
from gameClasses import *
from worldio import *

pygame.display.init()
screen = pygame.display.set_mode((576, 576))
Clock = pygame.time.Clock()

running = True

gm = GameManager(["First"])

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
            gm.move(D_UP)
        elif event.key == pygame.K_DOWN:
            gm.move(D_DOWN)
        elif event.key == pygame.K_RIGHT:
            gm.move(D_RIGHT)
        elif event.key == pygame.K_LEFT:
            gm.move(D_LEFT)
    
    gm.draw()
    screen.blit(gm.surf,(0,0))
    
    pygame.display.update()