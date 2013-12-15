import pygame
import pygame.gfxdraw
from consts import *
from worldio import *
from textrect import render_textrect

class World(object):
    def __init__(self,gsize,sp,mh,ml):
        self.gridsize = gsize #Avaliable sizes: 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 32, 36, 48, 64, 72, 96, 144, 192, 288
        self.spawnpoint = sp
        self.grid = []
        for i in xrange(576/gsize):
            self.grid.append([0]*(576/gsize))
        
        self.maxhistory = mh
        self.ticks = 0
        self.maxlives = ml
    
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
        if d != D_NONE:
            nx,ny = self.curpos
            if d == D_UP or d == D_DOWN:
                ny += (d/abs(d))
            elif d == D_RIGHT or d == D_LEFT:
                nx += (d/abs(d))
        
        if d != D_NONE and not self.world.isOpen(nx,ny):
            return False
        else:
            if d != D_NONE:
                self.curpos = (nx,ny)
            
                self.gm.eventManager.call("plrmove",(self,not self.isShadow))
    
            if not self.isShadow:
                self.history.append(d)
                if self.maxhistory != -1 and len(self.history)-1 == self.maxhistory:
                    self.isShadow = True
                
                return True
    
    def draw(self,surf,iscurrent):
        if iscurrent:
            col = COL_PLAYER
        else:
            alpha = 255 - max(30*((self.world.ticks/self.maxhistory) - self.generation),30)
            col = list(COL_PLAYER) + [alpha]
            
        gs = self.world.gridsize
        
        pygame.draw.circle(surf,col,getCenterOfSquare(self.curpos,gs),gs/2)
    
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
        self.surf = pygame.Surface((576, 576),pygame.SRCALPHA)
        self.text = []
        self.eventManager = GameEventManager()
        
        self.levels = levels
        self.worldindex = 0
        
        self.loadLevel()
        
        self.deathflash = 0
        self.deathflashinc = 25
        self.deathflashstate = 0
        
        self.newWorld = False
    
    def move(self,dir):
        if self.deathflashstate:
            return False
            
        move_succeeded = self.curplr.move(dir) 
        if not move_succeeded:
            return False
        
        if self.newWorld:
            self.newWorld = False
            return
            
        self.curworld.tick()
        
        if self.curplr.isShadow:
            oldgen = self.curplr.generation
            if oldgen + 1 == self.curworld.maxlives:
                self.loadLevel()
                return
            
            self.eventManager.call("newlife",(oldgen+1,))
            self.curplr = Player(self.curworld, self,oldgen+1)
            self.players.append(self.curplr)
    
        for plr in self.players:
            plr.sync()
        
        self.eventManager.call("tickdone",(self.curworld,))
        return True
    
    def loadLevel(self, next=False, flash=True):
        self.deathflash = 0
        self.deathflashstate = 1
        
        if next:
            self.worldindex += 1
            
        level = self.levels[self.worldindex]
        
        self.eventManager.clearCallbacks()
        self.curworld = readWorld(level,World,self)
        self.curplr = Player(self.curworld,self)
        self.players = [self.curplr]
        
        self.newWorld = True
        
    def draw(self):
        self.surf.fill((0,0,0))
        self.curworld.draw(self.surf)
        self.eventManager.call("draw",(self.surf,))
        for plr in self.players:
            plr.draw(self.surf,plr is self.curplr)
        
        if self.deathflashstate:
            self.deathflash += self.deathflashinc*self.deathflashstate
            if self.deathflash <= 20 and self.deathflashstate == -1:
                self.deathflashstate = 0
            elif self.deathflash >= 230:
                self.deathflashstate = -1
            
            self.surf.fill((0,0,0,self.deathflash))
        
    def winlevel(self):
        self.loadLevel(True)

class Game(object):
    def __init__(self):
        self.mainfont = pygame.font.SysFont("Verdana", 14)
        self.dayfont = pygame.font.Font(os.path.join(".","Media","ConsolaMono","ConsolaMono-Bold.ttf"), 14)
        self.menufont = pygame.font.Font(os.path.join(".","Media","ConsolaMono","ConsolaMono-Bold.ttf"), 20)
        self.view = VIEW_MAINMENU
        self.gm = None
        self.mainmenu_buttons = {"play":pygame.rect.Rect((100,250),(150,60)),"reset":pygame.rect.Rect((330,330),(150,60))}
    
    def handleEvents(self, events):
        for event in events:
            if self.view == VIEW_MAINMENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in self.mainmenu_buttons:
                        if self.mainmenu_buttons[b].collidepoint(event.pos):
                            self.menuButton(b)
                            
            elif self.view == VIEW_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.gm.move(D_UP)
                    elif event.key == pygame.K_DOWN:
                        self.gm.move(D_DOWN)
                    elif event.key == pygame.K_RIGHT:
                        self.gm.move(D_RIGHT)
                    elif event.key == pygame.K_LEFT:
                        self.gm.move(D_LEFT)
                    elif event.key == pygame.K_SPACE:
                        self.gm.move(D_NONE)
                    elif event.key == pygame.K_e:
                        self.startgame(["First"])
    
    def startgame(self,levels):
        self.view = VIEW_GAME
        self.gm = GameManager(levels)
    
    def menuButton(self,button):
        if button == "play":
            self.startgame(['First','Second','Third','Fourth'])
        
    def draw(self, surf):
        if self.view == VIEW_MAINMENU:
            surf.fill(COL_MENUBG)
            for button in self.mainmenu_buttons:
                if button == "play":
                    col = COL_BPLAY
                    text = "Play!"
                elif button == "reset":
                    col = COL_BRESET
                    text = "Reset\nProgress"
                
                pygame.draw.rect(surf,col,self.mainmenu_buttons[button])
                pygame.draw.rect(surf,(255,255,255),self.mainmenu_buttons[button].inflate(3,3),3)
                pygame.draw.rect(surf,(255,255,255),self.mainmenu_buttons[button].inflate(-8,-8),1)
                
                tsurf = render_textrect(text,self.menufont,self.mainmenu_buttons[button], COL_BTEXT, (0,0,0,0),1)
                surf.blit(tsurf,self.mainmenu_buttons[button])
            
        elif self.view == VIEW_GAME:
            gm = self.gm
            surf.fill(COL_BG)
            gm.draw()
            surf.blit(gm.surf,(0,0))
    
            for i,line in enumerate(gm.text):
                yoffset = i*self.mainfont.get_height() - 4
                surf.blit(self.mainfont.render(line, 0, COL_TEXT),(10,590+yoffset))
    
            if gm.curworld.maxhistory != -1:
                hourleft = gm.curworld.maxhistory-gm.curworld.ticks%gm.curworld.maxhistory -1
                surf.blit(dayfont.render("Hours Left: %d"%hourleft,1,COL_TEXT),(10,10))
            if gm.curworld.maxlives > 0:
                livesleft = gm.curworld.maxlives - gm.curplr.generation-1
                surf.blit(dayfont.render("Lives Left: %d"%livesleft,1,COL_TEXT),(10,25))