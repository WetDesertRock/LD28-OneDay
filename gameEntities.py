import pygame
from consts import *
from gameFunctions import *

class LevelFinish(object):
    def __init__(self, gm, pos):
        self.pos = pos
        self.gm = gm
        self.gm.eventManager.registerCallback("plrmove",self.playermove)
        self.gm.eventManager.registerCallback("draw",self.draw)
    
    def playermove(self,player,isCurrent):
        if player.curpos == self.pos:
            self.gm.winlevel()
    
    def draw(self, surf):
        gs = self.gm.curworld.gridsize
        pygame.draw.circle(surf,COL_GAMEEND[0],getCenterOfSquare(self.pos,gs),int(gs/2.2))
        pygame.draw.circle(surf,COL_GAMEEND[1],getCenterOfSquare(self.pos,gs),int(gs/2.6))
        pygame.draw.circle(surf,COL_GAMEEND[2],getCenterOfSquare(self.pos,gs),int(gs/3.6))

class TriggerText(object):
    def __init__(self, gm, text, isconstant, pos=None, newlife=None):
        self.pos = pos
        self.newlife = newlife
        self.gm = gm
        self.text = text
        self.constant = isconstant
        self.triggered = False
        
        if pos != None:
            self.gm.eventManager.registerCallback("plrmove",self.playermove)
        if newlife != None:
            self.gm.eventManager.registerCallback("newlife",self.onnewlife)
    
    def playermove(self,player,isCurrent):
        if isCurrent:
            if self.constant or not self.triggered and player.curpos == self.pos:
                self.gm.text = self.text
                self.triggered = True
    
    def onnewlife(self,newgen):
        if self.constant or not self.triggered and newgen == self.newlife:
            self.gm.text = self.text
            self.triggered = True

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
        pygame.draw.rect(surf,COL_SWITCH,getSquareRect(self.pos,gs,9))