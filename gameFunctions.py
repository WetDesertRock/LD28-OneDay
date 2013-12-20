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

from pygame.rect import Rect
def getSquareRect(pos, gsize, padding=0):
    x,y = pos
    x = x*gsize + padding
    y = y*gsize + padding
    run = gsize-(padding*2)
    return Rect((x,y),(run,run))

def getCenterOfSquare(pos,gsize):
    x,y = pos
    x = x*gsize + gsize/2
    y = y*gsize + gsize/2
    return x,y
