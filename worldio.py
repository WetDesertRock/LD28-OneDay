import os, json

from consts import *
from gameEntities import *

WORLDSPATH = os.path.join('.','Worlds')

def readWorld(name, World, gm=None):
    with open(os.path.join(WORLDSPATH,name,"world.json"),'r') as conf:
        options = json.loads(conf.read())
    
    world = World(options['size'],tuple(options['spawnpoint']),options['maxhistory'])
    
    emptychar = options.get("emptychar","-")
    solidchar = options.get("solidchar","&")

    if gm != None:
        for ent in options["entities"]:
            if ent['type'] == "levelend":
                LevelFinish(gm,tuple(ent['pos']))
            elif ent['type'] == "switch":
                Switch(gm,tuple(ent['pos']),tuple(ent['target']),ent['oneuse'])
    
    with open(os.path.join(WORLDSPATH,name,"grid.txt"),'r') as gridfile:
        for line in gridfile:
            if line.startswith("#"):
                continue
            
            lno,line = line.strip().split(':')
            y = int(lno)
            line = line.replace(' ','').replace(',','')
            for x,c in enumerate(line):
                if c == emptychar:
                    mat = MAT_EMPTY
                elif c == solidchar:
                    mat = MAT_SOLID
                    
                world.grid[x][y] = mat
    
    return world

def writeWorld(world):
    retstr = ""
    for y in xrange(len(world.grid)):
        lno = "%s: "%str(y).rjust(2)
        charlist = []
        for x in xrange(len(world.grid)):
            if world.grid[x][y] == MAT_SOLID:
                charlist.append("&")
            else:
                charlist.append("-")
        
        line = " ".join(charlist)
        
        retstr += lno+line+"\n"
    
    return retstr
            