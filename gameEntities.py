import pygame
from consts import *

class LevelFinish(object):
    def __init__(self, gm, pos):
        self.pos = pos
        self.gm = gm
        self.gm.eventManager.registerCallback("plrmove",self.playermove)
        self.gm.eventManager.registerCallback("draw",self.draw)
    
    def playermove(self,player,isShadow):
        if player.curpos == self.pos:
            self.gm.winlevel()
    
    def draw(self, surf):
        x,y = self.pos
        gs = self.gm.curworld.gridsize
        pygame.draw.rect(surf,COL_GAMEEND,((x*gs,y*gs),(gs,gs)))