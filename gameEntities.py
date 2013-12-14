import pygame
from consts import *
from gameFunctions import *

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
        gs = self.gm.curworld.gridsize
        pygame.draw.rect(surf,COL_GAMEEND,getSquareRect(self.pos,gs,7))

class Switch(object):
    def __init__(self, gm, pos, tpos, oneuse=False):
        self.pos = pos
        self.targetblock = tpos
        self.gm = gm
        self.state = False
        self.oneuse = oneuse
        self.gm.eventManager.registerCallback("tickdone",self.tickdone)
        self.gm.eventManager.registerCallback("draw",self.draw)
    
    def switchstate(self,state):
        x,y = self.targetblock
        if state:
            self.gm.curworld.grid[x][y] = MAT_EMPTY
        else:
            self.gm.curworld.grid[x][y] = MAT_SOLID
    
    def resetstate(self):
        if self.oneuse:
            return
        else:
            self.switchstate(False)
        
    def tickdone(self,world):
        for plr in self.gm.players:
            if plr.curpos == self.pos:
                self.switchstate(True)
                return
        
        self.resetstate()
    
    def draw(self, surf):
        gs = self.gm.curworld.gridsize
        pygame.draw.rect(surf,COL_SWITCH,getSquareRect(self.pos,gs,5))