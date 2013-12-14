import pygame
from consts import *
from worldio import *

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
    def __init__(self, world, gamemanager, generation=0):
        self.world = world
        self.curpos = world.spawnpoint
        self.history = [self.curpos]
        self.maxhistory = self.world.maxhistory
        self.isShadow = False
        self.gm = gamemanager
        self.generation = generation
    
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
            
            self.gm.eventManager.call("plrmove",(self,not self.isShadow))
    
            if not self.isShadow:
                self.history.append(d)
                if len(self.history)-1 == self.maxhistory:
                    self.isShadow = True
                
                return True
    
    def draw(self,surf,iscurrent):
        if iscurrent:
            col = COL_PLAYER
        else:
            col = COL_PPLAYER[self.generation%len(COL_PPLAYER)]
        cx,cy = self.curpos
        gs = self.world.gridsize
        pygame.draw.rect(surf,col,((cx*gs,cy*gs),(gs,gs)))
    
    def seek(self, i):
        i = min(len(self.history)-1,max(0,i)) #Constrain
        move = self.history[i]
        if type(move) == tuple:
            self.curpos = move
            self.gm.eventManager.call("plrmove",(self,self==self.gm.curplr))
        else:
            self.move(self.history[i])
            
    def sync(self):
        if self.isShadow:
            localtick = self.world.ticks%self.maxhistory
            self.seek(localtick)

class GameEventManager(object):
    def __init__(self):
        self.eventcallbacks = {}
    
    def call(self, evt, args):
        if evt not in self.eventcallbacks:
            return
            
        for callback in self.eventcallbacks.get(evt,[]):
            callback(*args)
    
    def registerCallback(self, evt, callback):
        if evt not in self.eventcallbacks:
            self.eventcallbacks[evt] = []
        
        self.eventcallbacks[evt].append(callback)
    
    def clearCallbacks(self):
        self.eventcallbacks = {}

class GameManager(object):
    def __init__(self,levels):
        self.surf = pygame.Surface((576, 576))
        self.levels = levels
        self.eventManager = GameEventManager()
        self.curworld = readWorld(levels[0],World,self)
        self.worldindex = 0
        self.curplr = Player(self.curworld,self)
        self.players = [self.curplr]
    
    def move(self,dir):
        move_succeeded = self.curplr.move(dir) 
        if not move_succeeded:
            return False
    
        self.curworld.tick()
        
        if self.curplr.isShadow:
            oldgen = self.curplr.generation
            self.curplr = Player(self.curworld, self,oldgen+1)
            self.players.append(self.curplr)
    
        for plr in self.players:
            plr.sync()
        
        self.eventManager.call("tickdone",(self.curworld,))
        return True
    
    def draw(self):
        self.surf.fill((0,0,0))
        self.curworld.draw(self.surf)
        self.eventManager.call("draw",(self.surf,))
        for plr in self.players:
            plr.draw(self.surf,plr is self.curplr)
        
    def winlevel(self):
        self.eventManager.clearCallbacks()
        self.players = []
        self.worldindex += 1
        self.curworld = readWorld(self.levels[self.worldindex],World,self)
        self.curplr = Player(self.curworld,self)
        self.players = [self.curplr]
        