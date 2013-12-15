import pygame, time, os

from consts import *
from gameClasses import *
from worldio import *

pygame.font.init()

pygame.display.init()
screen = pygame.display.set_mode((576, 650))
Clock = pygame.time.Clock()
mainfont = pygame.font.SysFont("Verdana", 14)
dayfont = pygame.font.Font(os.path.join(".","Media","ConsolaMono","ConsolaMono-Bold.ttf"), 14)


running = True

gm = GameManager(["Third"])
# gm = GameManager(["First","Second","Third"])

while running:
    Clock.tick(30)
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
        elif event.key == pygame.K_SPACE:
            gm.move(D_NONE)
    
    screen.fill(COL_BG)
    gm.draw()
    screen.blit(gm.surf,(0,0))
    
    for i,line in enumerate(gm.text):
        yoffset = i*mainfont.get_height() - 4
        screen.blit(mainfont.render(line, 0, COL_TEXT),(10,590+yoffset))
    
    hourleft = gm.curworld.maxhistory-gm.curworld.ticks%gm.curworld.maxhistory -1
    screen.blit(dayfont.render("Hours Left: %d"%hourleft,1,COL_TEXT),(10,10))
        
    
    pygame.display.update()