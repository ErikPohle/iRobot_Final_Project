import math, random, asteroid

class Environment():

    def __init__(self, mapDimensions, numAsteroids):

        # need dimensions of map for random asteroid creation
        # need number of asteroids to be generated
        # just assume dimensions are 400 x 400

        self.dictOfAsteroids = {}
        self.mapLength = mapDimensions[0]
        self.mapWidth = mapDimensions[1]
        self.mapHeight = mapDimensions[2]
        self.numAsteroids = numAsteroids
        self.asteroidSpeed = 5
        self.gameOver = False
        
        print("LOG: Environment Succesfully Initialized.")

        # rospy.init_node("Environment")

        # what should I publish to?
        # what am I publishing?
        # publisher = rospy.Publisher("???", PoseStamped, queue_size=10)
        # while publisher.get_num_connections() == 0:
        # 	rospy.sleep(1)

        # publisher.publish(msg)

    # Call after init, while the game is still running if we are out of asteroids from the initial population
    def spawnAsteroids(self):

        # generate x and y positions for asteroids and add them to list
        for i in range(0, self.numAsteroids):
            asteroidX = random.randint(0, self.mapLength)
            asteroidY = random.randint(0, self.mapWidth)
            asteroidZ = random.randint(50, self.mapHeight)
            ast = asteroid.Asteroid(asteroidX, asteroidY, asteroidZ)

            # very hacky but it works...lol
            x = "astr" + str(random.randint(0, 100000))
            while x in self.dictOfAsteroids:
                x = "astr" + str(random.randint(0, 100000))
            self.dictOfAsteroids[x] = ast
        
        print("LOG: Spawned Asteroids Succesfully")

    def asteroidCollision(self):
        # hmmm
        # need Publisher/Subscriber for health (if asteroid hits player) and points (if player destroys asteroid)

        for i in self.dictOfAsteroids:
            pos = self.dictOfAsteroids[i].getPos()
            
            # check if z pos is hitting the ground
            if pos[2] <= 25:
                self.gameOver = True
                return
            
            # if no asteroids have hit the ground yet
            # check if the players bullet hit an asteroid
            # do we need to worry about traveling time of bullet to asteroid?
            # or do we just assume its immediately hitting the asteroid?

            # subscribe to channel, listen for shot
                
    
    def updateAsteroids(self, dt):
        newDict = {}
        for i in self.dictOfAsteroids:
            
            # if hit, just continue, we dont want to update this asteroid and add it to tempList
            # only non-hit asteroids go on tempList
            if self.dictOfAsteroids[i].isHit:
                continue
            
            else:
                pos = self.dictOfAsteroids[i].getPos()
                newDict[i] = self.dictOfAsteroids[i]
                # x,y,z - z represents height from ground each asteroid is
                newDict[i].updatePos(pos[0], pos[1], pos[2] - (self.asteroidSpeed * dt))
        
        self.dictOfAsteroids = newDict

        if len(self.dictOfAsteroids) == 0:
            return -1
        else:
            return 0
            

if __name__ == "__main__":
    initEnv()
    print(listOfAsteroids)

    