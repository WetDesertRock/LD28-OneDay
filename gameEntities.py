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

import pygame
from consts import *
from gameFunctions import *

class Trigger(object):
    def __init__(self,gm,isconstant=False,triggerpos=None,triggerlife=None):
        self.gm = gm
        self.constant = isconstant
        self.triggered = False
        
        if triggerpos:
            self.triggerpos = triggerpos
            self.gm.eventManager.registerCallback("plrmove",self.playermove)
            
        if triggerlife:
            self.triggerlife = triggerlife
            self.gm.eventManager.registerCallback("newlife",self.onnewlife)
        
    
    def playermove(self,player,isCurrent):
        if isCurrent:
            if self.constant or not self.triggered and player.curpos == self.triggerpos:
                self.triggered = True
                self.posTrigger(player,isCurrent)
    
    def onnewlife(self,newgen):
        if self.constant or not self.triggered and newgen == self.triggerlife:
            self.triggered = True
            self.lifeTrigger(newgen)
    
    def posTrigger(p,i):
        #Stub, subclass and redefine to make use of this.
        pass
    
    def lifeTrigger(ng):
        #Stub, subclass and redefine to make use of this.
        pass
        

class LevelFinish(Trigger):
    def __init__(self, gm, pos):
        self.pos = pos
        self.gm = gm
        super(LevelFinish,self).__init__(gm, triggerpos=pos)
        self.gm.eventManager.registerCallback("draw",self.draw)
        self.surf = None
        
    def posTrigger(self,player,isCurrent):
        self.gm.winlevel()
    
    def draw(self, surf):
        gs = self.gm.curworld.gridsize
        if self.surf == None:
            gs = self.gm.curworld.gridsize
            self.surf = pygame.Surface((gs,gs),pygame.SRCALPHA)
            self.surf.fill((0,0,0,0))
            pygame.draw.circle(self.surf,COL_GAMEEND[0],(gs/2,gs/2),int(gs/2.2))
            pygame.draw.circle(self.surf,COL_GAMEEND[1],(gs/2,gs/2),int(gs/2.6))
            pygame.draw.circle(self.surf,COL_GAMEEND[2],(gs/2,gs/2),int(gs/3.6))
        
        surf.blit(self.surf,getSquareRect(self.pos,gs))
    
    
class TriggerText(Trigger):
    def __init__(self, gm, text, isconstant, pos=None, newlife=None):
        super(TriggerText,self).__init__(gm,isconstant,pos,newlife)
        self.text = text
    
    def posTrigger(self,player,isCurrent):
        self.gm.text = self.text
        self.gm.game.sounds['triggertext'].play()
    
    def lifeTrigger(self,newgen):
        self.gm.text = self.text
        self.gm.game.sounds['triggertext'].play()

class TriggerScreenText(Trigger):
    def __init__(self, gm, textblocks, isconstant, pos=None, newlife=None):
        super(TriggerScreenText,self).__init__(gm,isconstant,pos,newlife)
        self.textblocks = textblocks
    
    def posTrigger(self,player,isCurrent):
        self.gm.textblocks = self.textblocks
    
    def lifeTrigger(self,newgen):
        self.gm.textblocks = self.textblocks

class Switch(object):
    def __init__(self, gm, pos, tpos=None, oneuse=False,tposlist=None):
        self.pos = pos
        self.targetposlist = tposlist
        self.targetblock = tpos
        self.gm = gm
        self.state = False
        self.oneuse = oneuse
        self.gm.eventManager.registerCallback("tickdone",self.tickdone)
        self.gm.eventManager.registerCallback("draw",self.draw)
    
    def switchstate(self,state):
        if self.targetblock != None:
            x,y = self.targetblock
            if state:
                self.gm.curworld.grid[x][y] = MAT_EMPTY
            else:
                self.gm.curworld.grid[x][y] = MAT_SOLID
        
        if self.targetposlist != None:
            for pos in self.targetposlist:
                x,y = pos
                if state:
                    self.gm.curworld.grid[x][y] = MAT_EMPTY
                else:
                    self.gm.curworld.grid[x][y] = MAT_SOLID
        
        if state and not self.state:
            self.gm.game.sounds['switch'].play()
            
        self.state = state
    
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