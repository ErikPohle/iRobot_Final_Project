import math, random

class Asteroid():

    def __init__(self, xPos, yPos, zPos):
        self.x = xPos
        self.y = yPos
        self.z = zPos
        ranN = random.randint(0, 10)
        if ranN % 2 == 0:
            self.isHit = True
        else:
            self.isHit = True
        
    def updatePos(self, xPos, yPos, zPos):
        self.x = xPos
        self.y = yPos
        self.z = zPos

    def getPos(self):
        return [self.x, self.y, self.z]

    def isHit(self):
        return self.isHit