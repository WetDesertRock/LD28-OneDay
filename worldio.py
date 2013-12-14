import os, json

from consts import *
from gameEntities import *

WORLDSPATH = os.path.join('.','Worlds')

def readWorld(name, World, gm):
    with open(os.path.join(WORLDSPATH,name,"world.json"),'r') as conf:
        options = json.loads(conf.read())
    
    world = World(options['size'],tuple(options['spawnpoint']),options['maxhistory'])
    
    emptychar = options.get("emptychar","-")
    solidchar = options.get("solidchar","&")
    
    for ent in options["entities"]:
        if ent['type'] == "levelend":
            LevelFinish(gm,tuple(ent['pos']))
    
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