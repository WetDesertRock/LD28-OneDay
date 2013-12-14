import pygame
from consts import *

class World(object):
    def __init__(self,gsize,sp,mh):
        self.gridsize = gsize #Avaliable sizes: 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 32, 36, 48, 64, 72, 96, 144, 192, 288
        self.spawnpoint = sp
        self.grid = []
        for i in xrange(576/gsize):
            self.grid.append([0]*(576/gsize))
        
        self.maxhistory = mh
        self.ticks = 0
    
    def isOpen(self,x,y):
        if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid):
            return False
            
        if self.grid[x][y] == MAT_EMPTY:
            return True
        else:
            return False
    
    def draw(self,surf):
        for x in xrange(len(self.grid)):
            for y in xrange(len(self.grid)):
                if self.grid[x][y] == MAT_SOLID:
                    col = COL_SOLID
                elif self.grid[x][y] == MAT_EMPTY:
                    col = COL_EMPTY
                pygame.draw.rect(surf,col,((x*self.gridsize,y*self.gridsize),(self.gridsize,self.gridsize)))
        
    def tick(self):
        self.ticks += 1
        
        
class Player(object):
    def __init__(self, world):
        self.world = world
        self.curpos = world.spawnpoint
        self.history = [self.curpos]
        self.maxhistory = self.world.maxhistory
        self.isShadow = False
    
    def move(self,d):
        nx,ny = self.curpos
        if d == D_UP or d == D_DOWN:
            ny += (d/abs(d))
        elif d == D_RIGHT or d == D_LEFT:
            nx += (d/abs(d))
        
        if not self.world.isOpen(nx,ny):
            return False
        else:
            self.curpos = (nx,ny)
            self.history.append(self.curpos)
            if not self.isShadow and len(self.history)-1 == self.maxhistory:
                self.isShadow = True
                
            return True
    
    def draw(self,surf,iscurrent):
        if iscurrent:
            col = COL_PLAYER
        else:
            col = COL_PPLAYER
        cx,cy = self.curpos
        gs = self.world.gridsize
        pygame.draw.rect(surf,col,((cx*gs,cy*gs),(gs,gs)))
    
    def seek(self, i):
        i = min(len(self.history)-1,max(0,i)) #Constrain
        self.curpos = self.history[i]
    
    def sync(self):
        if self.isShadow:
            localtick = self.world.ticks%self.maxhistory
            self.seek(localtick)