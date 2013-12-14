import os, json

from gameClasses import World
from consts import *

WORLDSPATH = os.path.join('.','Worlds')

def readWorld(name):
    with open(os.path.join(WORLDSPATH,name,"world.json"),'r') as conf:
        options = json.loads(conf.read())
    
    world = World(options['size'],tuple(options['spawnpoint']),options['maxhistory'])
    
    emptychar = options.get("emptychar","-")
    solidchar = options.get("solidchar","&")
    
    with open(os.path.join(WORLDSPATH,name,"grid.txt"),'r') as gridfile:
        for line in gridfile:
            if line.startswith("#"):
                continue
            
            lno,line = line.strip().split(':')
            y = int(lno)
            print line
            line = line.replace(' ','').replace(',','')
            for x,c in enumerate(line):
                print x,y
                if c == emptychar:
                    mat = MAT_EMPTY
                elif c == solidchar:
                    mat = MAT_SOLID
                    
                world.grid[x][y] = mat
    
    return world