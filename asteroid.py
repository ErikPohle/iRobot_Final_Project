import math, random

class Asteroid():

    def __init__(self, xPos, yPos, zPos):
        self.x = xPos
        self.y = yPos
        self.z = zPos
        self.isHit = False
        
    def updatePos(self, xPos, yPos, zPos):
        self.x = xPos
        self.y = yPos
        self.z = zPos

    def getPos(self):
        return [self.x, self.y, self.z]

    def isHit(self):
        return self.isHit