from math import *



def getAngleBetweenPoints(origin, end):
    xDiff = end[0] - origin[0]
    yDiff =  origin[1] - end[1]

    return degrees(atan2(yDiff, xDiff))
