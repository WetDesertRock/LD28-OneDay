import pygame, time, os, sys

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
game = Game()

# if len(sys.argv) >= 2:
#     gm = GameManager(sys.argv[1:])
# else:
#     gm = GameManager(["First","Second","Third","Fourth"])

while running:
    Clock.tick(30)
    events = pygame.event.get()
    extraevents = []
    for event in events:
        handled = False
        if event.type == pygame.QUIT:
            running = False
            handled = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                handled = True
                
            elif event.key == pygame.K_s:
                stime = time.time()
                pygame.image.save(screen, "Screenshot_%d.png" % stime)
                print "Wrote Screenshot_%d.png" % stime
                handled = True
        
        if not handled:
            extraevents.append(event)
    
    game.handleEvents(extraevents)
    
    game.draw(screen)
    
    pygame.display.update()